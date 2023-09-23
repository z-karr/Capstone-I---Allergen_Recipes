from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FieldList, FormField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional
from wtforms.widgets import CheckboxInput

class SearchForm(FlaskForm):
    excluded_ingredients = StringField('Excluded Ingredients (comma-separated)')
    submit = SubmitField('Search Recipes')


# class SearchForm(FlaskForm):
#     dairy = BooleanField('Dairy')
#     eggs = BooleanField('Eggs')
#     nuts = BooleanField('Nuts')
#     peanuts = BooleanField('Peanuts')
#     carrots = BooleanField('Carrots')
#     celery = BooleanField('Celery')
#     wheat = BooleanField('Wheat')
#     soy = BooleanField('Soy')
#     fish = BooleanField('Fish')
#     shellfish = BooleanField('Shellfish')
#     fruit = BooleanField('Fruit')
    
#     submit = SubmitField('Search Recipes')

# class SearchForm(FlaskForm):   ######## Redo this without using selectmultiplefields  
    # allergens = SelectMultipleField('Select Allergens', choices=[
    #     ('dairy', 'Dairy', False),
    #     ('eggs', 'Eggs', False),
    #     ('nuts', 'Nuts', False),
    #     ('peanuts', 'Peanuts', False),
    #     ('carrots', 'Carrots', False),
    #     ('celery', 'Celery', False),
    #     ('wheat', 'Wheat', False),
    #     ('soy', 'Soy', False),
    #     ('fish', 'Fish', False),
    #     ('shellfish', 'Shellfish', False),
    #     ('fruit', 'Fruit', False),
    # ])
    # submit = SubmitField('Search Recipes')
    # allergens = {
    #     'dairy': BooleanField('Dairy'),
    #     'eggs': BooleanField('Eggs'),
    #     'nuts': BooleanField('Nuts'),
    #     'peanuts': BooleanField('Peanuts'),
    #     'carrots': BooleanField('Carrots'),
    #     'celery': BooleanField('Celery'),
    #     'wheat': BooleanField('Wheat'),
    #     'soy': BooleanField('Soy'),
    #     'fish': BooleanField('Fish'),
    #     'shellfish': BooleanField('Shellfish'),
    #     'fruit': BooleanField('Fruit')
    # }

    # submit = SubmitField('Search Recipes')

    # def selected_allergens(self):
    #     # Create a list of selected allergens
    #     allergens = []
    #     for field_name, field in self._fields.items():
    #         if field.data:
    #             allergens.append(field_name)
    #     return allergens
    
 



class AddUserForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])