import os

from flask import Flask, render_template, request, flash, redirect, session, g, url_for
# from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError


from models import db, connect_db, User, Recipe, saved_recipes

# CURR_USER_KEY = "curr_user"

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



# import os

# # app.py

# from flask import Flask, render_template, request, redirect, url_for, flash
# from flask_sqlalchemy import SQLAlchemy
# from flask_login import LoginManager

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = (
#     os.environ.get('DATABASE_URL', 'postgresql:///recipes_db'))
# app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")

# db = SQLAlchemy(app)

# login_manager = LoginManager(app)
# login_manager.login_view = 'login'

# # Import your database models
# from models import User, Recipe

# # Define your routes here
# @app.route('/')
# def index():
#     # Your route logic here
#     pass

# # Import your init_db function
# from init_db import init_db

# # Initialize the database
# init_db()

# if __name__ == '__main__':
#     app.run()
# _________________________________________________________________


# from flask import Flask, render_template, request, redirect, url_for, flash
# from flask_sqlalchemy import SQLAlchemy
# from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user
# import requests
# from models import connect_db, init_db


# app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = (
#     os.environ.get('DATABASE_URL', 'postgresql:///recipes_db'))

# app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")

# db = SQLAlchemy(app)

# login_manager = LoginManager(app)
# login_manager.login_view = 'login'

# connect_db(app)
# init_db() 