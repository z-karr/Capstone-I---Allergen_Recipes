
# from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# app = Flask(__name__)
db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    saved_recipes = db.relationship('Recipe', secondary='saved_recipes', backref=db.backref('users', lazy='dynamic'))

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    ingredients = db.Column(db.String(200))
    instructions = db.Column(db.Text)
    image = db.Column(db.String(200))

saved_recipes = db.Table('saved_recipes',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('recipe_id', db.Integer, db.ForeignKey('recipe.id'))
)

# def init_db():
#     """Create the database tables."""
#     with app.app_context():
#         db.create_all()

# def connect_db(app):
#     """Connect this database to provided Flask app."""
#     db.app = app
#     db.init_app(app)

def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    db.app = app
    db.init_app(app)