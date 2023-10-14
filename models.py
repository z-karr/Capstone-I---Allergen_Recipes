


from flask_bcrypt import Bcrypt, generate_password_hash
from flask_sqlalchemy import SQLAlchemy



bcrypt = Bcrypt()
db = SQLAlchemy()

"""Many Users can save many Recipes, and many Recipes can be saved by many Users"""


# Create an association table for the many-to-many relationship between users and recipes
saved_recipes_association = db.Table('saved_recipes',
    db.Column('user_id', db.Integer, db.ForeignKey('User.id')),
    db.Column('recipe_id', db.Integer, db.ForeignKey('Recipe.id'))
)


class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    user_recipes = db.relationship("Recipe", secondary=saved_recipes_association)

   

    
    
    


    def __repr__(self):
        return f"<User #{self.id}: {self.username}, {self.email}>"
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)
    
    @classmethod
    def signup(cls, email, username, password):
        """Register/signup user.
        
        Hashes password and adds user to system
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            email=email, 
            username=username,
            password=hashed_pwd,
        )

        db.session.add(user)
        return user
    
    @classmethod
    def authenticate(cls, username, password):
        """Find user with 'username' and 'password'.
        
        This is a class method (call it on the class, not individual user).
        It searches for a user whose password hash matches this password and, if it finds such a user, returns that user object.
        
        If can't find matching user( or if password is wrong), returns False.
        """ 

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user
            
        return False

class Recipe(db.Model):
    __tablename__ = 'Recipe'

    # auto increment field
    id = db.Column(db.Integer, primary_key=True, autoincrement=True) 
    #Spoonacular API id field
    spoonacular_id = db.Column(db.Integer, unique=True)


def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    db.app = app
    db.init_app(app)