import os

from flask import Flask, render_template, request, flash, redirect, session, g, url_for, jsonify
import requests
import random
# from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError



import json



from models import db, connect_db, User, Recipe
from forms import AddUserForm, LoginForm, SearchForm
from flask_wtf.csrf import CSRFProtect, CSRFError



apiKey = '5e3f80e8f6f64272a5a29fc9e6c99b74'

CURR_USER_KEY = "curr_user"

valid_allergens = ["dairy", "eggs", "nuts", "peanuts", "carrots", "celery", "wheat", "soy", "fish", "shellfish", "fruit"]


app = Flask(__name__)

csrf = CSRFProtect(app)

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
            # flash(("Username already taken", 'danger'))
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
            # flash((f"Hello, {user.username}!", "success"))
            return redirect("/")

        # flash(("Invalid credentials.", 'danger'))

    return render_template('login.html', form=form)



@app.route('/logout')
def logout():
    
    do_logout()
    # flash('Logged out successfully!', 'success')

    return redirect('/login')


# # # Front-end/Spoonacular API routes # # #

@app.route('/', methods=['GET', 'POST'])
def index():
    """Handle landing page.
    
        Generate search form.
        
        Request and generate random recipes from Spoonacular API.
    """

    # Create an instance of the SearchForm
    form = SearchForm()


    # Make a request to the Spoonacular API to fetch random recipes
    url = f'https://api.spoonacular.com/recipes/random?number=5&apiKey={apiKey}'
    response = requests.get(url)

    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        # print response data
        print(data, "********")

        # Extract the list of random recipes
        recipes = data['recipes']

        # Render the template with the form and recipes
        return render_template('index.html', form=form, recipes=recipes)
    else:
        return render_template('index.html', form=form)





@app.route('/search', methods=['GET', 'POST'])
def search():
    """Request recipes from API excluding user-entered allergens/ingredient(s).

        Return recipes, shuffled for randomization.
    """
    
    form = SearchForm()

    recipes = []
    excluded_ingredients = []

    offset = int(request.args.get('offset', 0))  # Get the offset value from the query string or default to 0
 

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
                'offset': offset,  # Pass the offset parameter to the API 
            }

            response = requests.get(
                f"https://api.spoonacular.com/recipes/complexSearch?apiKey={apiKey}&excludeIngredients={excludedIngredients}&number={number}&offset={start}&addRecipeInformation=true", params=params
                )

            if response.status_code == 200:
                data = response.json()
                recipes = data.get('results', [])
                print(data, "******************")
                random.shuffle(recipes)

            else:
                recipes = []

            return render_template('search.html', form=form, recipes=recipes, excluded_ingredient=excluded_ingredients)

    return render_template('search.html', form=form, recipes=None, excluded_ingredients=excluded_ingredients)
    


@app.route('/recipes/<int:recipe_id>/save', methods=['POST'])
def save_recipe(recipe_id):
    """save/unsave functionality for button on recipe"""

    if not g.user:
        return redirect('/login')

    

    try:
        
        api_url = f'https://api.spoonacular.com/recipes/{recipe_id}/information'
        print("API URL:", api_url)
        params = {
            'apiKey': apiKey  # 'apiKey' is defined at top of script
        }

        response = requests.get(api_url, params=params)

        if response.status_code == 200:
            recipe_info = response.json()
            spoonacular_id = recipe_info.get('id')

            recipe = Recipe.query.filter_by(spoonacular_id=spoonacular_id).first()

            print(recipe, "**********")
            print(recipe in g.user.user_recipes)
            print(g.user.user_recipes)

            if recipe is None:
                new_recipe = Recipe(spoonacular_id=spoonacular_id)
                db.session.add(new_recipe)
                db.session.commit()
                g.user.user_recipes.append(new_recipe)
                db.session.commit()
                
                return jsonify({"message": "*** Recipe saved successfully.***"})
            
            if recipe in g.user.user_recipes:
                g.user.user_recipes.remove(recipe)  # Remove from User.user_recipes relationship
                db.session.commit()

                db.session.delete(recipe)  # Delete from the Recipe table
                db.session.commit()
                
                return jsonify({"message": "***Recipe removed successfully.***"})
            
                

        return jsonify({"error": "API request failed with status code " + str(response.status_code)}), 400
    
    except CSRFError:
        return jsonify({"error": str(e)}), 400

    except Exception as e:
        return jsonify({"error": "An exception occurred: " + str(e)}), 500
    


@app.route('/recipes/<int:recipe_id>/save_status', methods=['GET'])
def check_save_status(recipe_id):
    """If User is logged in, check if the recipe is saved for the current user,
      so button on page reflects correct save/unsave state.
    """

    if not g.user:
        return jsonify({"saved": False})

    # Retrieve the recipe from the database based on recipe_id
    recipe = Recipe.query.filter_by(spoonacular_id=recipe_id).first()

    if recipe and recipe in g.user.user_recipes:
        return jsonify({"saved": True})
    else:
        return jsonify({"saved": False})
    

@app.route('/load_more', methods=['GET'])
def load_more():
    """Load more recipes based on the offset."""
    
    offset = request.args.get('offset', default=0, type=int)  # Get the offset from the query parameters
    number = 10  # Number of recipes to load

    # Perform a request to Spoonacular API to fetch more recipes based on the offset
    params = {
        'apiKey': apiKey,
        'number': number,
        'offset': offset,  # Use the received offset to get the next set of recipes
        'addRecipeInformation': 'true',
    }

    response = requests.get("https://api.spoonacular.com/recipes/complexSearch", params=params)

    if response.status_code == 200:
        data = response.json()
        results = data.get('results', [])
        return jsonify({'results': results})  # Return the fetched recipes as JSON
    else:
        return jsonify({'error': 'Failed to load more recipes'}), 500  # Return an error response if the request fails


    


@app.route('/saved', methods=['GET'])
def saved():
    """Show user saved recipes on a page"""

    if not g.user:
        return redirect('/login')
    
     # Retrieve all saved recipes for the current user
    user_recipes = g.user.user_recipes

     # List to store detailed recipe information
    detailed_recipes = []

    # Fetch detailed information for each saved recipe from the API
    for recipe in user_recipes:
        api_url = f'https://api.spoonacular.com/recipes/{recipe.spoonacular_id}/information'
        params = {
            'apiKey': apiKey  # apiKey defined at top of script
        }

        response = requests.get(api_url, params=params)

        if response.status_code == 200:
            detailed_recipe_info = response.json()
            detailed_recipes.append(detailed_recipe_info)
        else:
            # Handle API request error (e.x., log the error, skip the recipe, etc.)
            pass

    # Pass the detailed recipes to the template
    return render_template("saved.html", detailed_recipes=detailed_recipes)
    




if __name__ == '__main__':
    app.run(debug=True)


