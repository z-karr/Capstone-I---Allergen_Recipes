import os

from flask import Flask, render_template, request, flash, redirect, session, g, url_for, jsonify
import requests
# from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError



import json



from models import db, connect_db, User, Recipe, Saved_Recipes
from forms import AddUserForm, LoginForm, SearchForm, BooleanField


apiKey = '5e3f80e8f6f64272a5a29fc9e6c99b74'

CURR_USER_KEY = "curr_user"

valid_allergens = ["dairy", "eggs", "nuts", "peanuts", "carrots", "celery", "wheat", "soy", "fish", "shellfish", "fruit"]


app = Flask(__name__)

# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql:///recipes_db'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")
# toolbar = DebugToolbarExtension(app)





connect_db(app)


# # #   User registration/signup, log-in, logout routes # # #

@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """Handle user registration.
    
        Create new user and add to DB. Redirect to home page.
    
        If form not valid, present form.
    
        If there is already a user with that username: flash message and re-present form.
    """
    form = AddUserForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                email=form.email.data,
                username=form.username.data,
                password=form.password.data,
            )
            db.session.commit()
        
        except IntegrityError:
            flash(("Username already taken", 'danger'))
            return render_template('signup.html', form=form)
        
        do_login(user)

        return redirect("/")
    
    else:
        return render_template('signup.html', form=form)



@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login."""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                form.password.data)
        
        if user:
            do_login(user)
            flash((f"Hello, {user.username}!", "success"))
            return redirect("/")

        flash(("Invalid credentials.", 'danger'))

    return render_template('login.html', form=form)



@app.route('/logout')
def logout():
    # the logout route code
    do_logout()
    flash('Logged out successfully!', 'success')

    return redirect('/login')


# # # Front-end/Spoonacular API routes # # #

@app.route('/', methods=['GET', 'POST'])
def index():
    # Create an instance of the SearchForm
    form = SearchForm()


    # Make a request to the Spoonacular API to fetch random recipes
    url = f'https://api.spoonacular.com/recipes/random?number=5&apiKey={apiKey}'
    response = requests.get(url)

    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        print(data, "********")

        # Extract the list of random recipes
        recipes = data['recipes']

        # Render the template with the form and recipes
        return render_template('index.html', form=form, recipes=recipes)
    else:
        # Handle API request error, e.g., by displaying an error message
        flash(("Error retrieving recipes." 'error'))
        return render_template('index.html')





@app.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()

    recipes = []

    

    if form.validate_on_submit():
        user_input = form.excluded_ingredients.data
        excluded_ingredients = []

        # apiKey = '5e3f80e8f6f64272a5a29fc9e6c99b74'
        number = 10
        excludedIngredients = ','.join(excluded_ingredients)
        start = 0

        # Split user input by commas and trim whitespace from each ingredient
        user_ingredients = [ingredient.strip() for ingredient in user_input.split(',')]

        # Check if user-entered ingredients are valid (valid_allergens defined at top of script^^)
        for ingredient in user_ingredients:
            if ingredient in valid_allergens:
                excluded_ingredients.append(ingredient)
            else:
                flash(f"Invalid allergen: {ingredient}", "danger")
        
        # If there are invalid allergens, show an error message
        if len(excluded_ingredients) == 0:
            flash("No valid allergens entered.", "danger")
        else:
            # Send a request to the Spoonacular API to search for recipes
            params = {
                'apiKey': apiKey,
                'number': number,
                'excludedIngredients': ','.join(excluded_ingredients),
                'addRecipeInformation': 'true',
            }

            response = requests.get(
                f"https://api.spoonacular.com/recipes/complexSearch?apiKey={apiKey}&excludeIngredients={excludedIngredients}&number={number}&offset={start}&addRecipeInformation=true", params=params
                )

            if response.status_code == 200:
                data = response.json()
                recipes = data.get('results', [])
                print(data, "******************")

                

            else:
                recipes = []

            return render_template('search.html', form=form, recipes=recipes)

    return render_template('search.html', form=form, recipes=None)



####### General User Recipe routes routes ########

@app.route('/profile/<int:user_id>')
def user_profile(user_id):
    # Route takes user_id as a parameter, retrieves user info from SQLAlchemy db
    user = User.query.get(user_id)
    if user:
        return render_template('profile.html', user=user)
    else:
        return "User not found", 404



####### Save/Saved Recipe routes ########

@app.route('/recipe/<int:recipe_id>/save', methods=['POST'])
def save_recipe(recipe_id):
    """Get and Store API id in db here"""

    if not g.user:
        # flash("You must be logged in to save recipes.", 'danger')
        return redirect('/login')
    
    # recipe_id = requests.get(f'https://api.spoonacular.com/recipes/{id}/information')
    
    api_url = f'https://api.spoonacular.com/recipes/{recipe_id}/information'
    params = {
        'apiKey': apiKey
    }

    try:
        response = requests.get(api_url, params=params)

        if response.status_code == 200:
        # Extract the 'id' from the API response
            recipe_info = response.json()
            recipe_api_id = recipe_info.get('id')

        # Check if a recipe with the given API 'id' already exists in your database
            recipe = Recipe.query.filter_by(spoonacular_id=recipe_api_id).first()

            if recipe is None:
            # Recipe with this API 'id' doesn't exist, create a new recipe record
                new_recipe = Recipe(spoonacular_id=recipe_api_id)
                db.session.add(new_recipe)
                db.session.commit()
                recipe = new_recipe


            if recipe in g.user.saved_recipes:
                g.user.saved_recipes.remove(recipe)
            else:
                save = Saved_Recipes(user=g.user, recipe=recipe)
                db.session.add(save)
                db.session.commit()
                return jsonify({"message": "***Recipe saved successfully.***"})
    
        else: 
            return jsonify({"error": "API request failed with status code " + str(response.status_code)})
    except Exception as e:
            return jsonify({"error": "An exception occurred: " + str(e)})

    # else: 
    #     return redirect(url_for('index'))




if __name__ == '__main__':
    app.run(debug=True)


# Fetch API data
# @app.route('/fetch-spoonacular-data', methods=['GET'])
# def fetch_spoonacular_data():
    
#     # Get the data parameter sent from the AJAX request and parse it as JSON
#     data = request.args.get('data')
#     data_dict = json.loads(data)  # Parse the JSON data

#     # Now, we can work with data_dict as a Python dictionary
#     # For example, can access data_dict['key'] to get specific values
    
#     # can return a JSON response if needed
#     response_data = {'message': 'Data received successfully', 'data': data_dict}
#     return jsonify(response_data)
