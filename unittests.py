import unittest
from app import app, db, User, Recipe

class MyAppTests(unittest.TestCase):
    def setUp(self):
        """Set up the test environment."""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///test_db'
        app.config['SQLALCHEMY_ECHO'] = False
        self.client = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        """Clean up the test environment."""
        with app.app_context():
            db.drop_all()

    def test_index_route(self):
        """Test the index route."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_signup_route(self):
        """Test the signup route."""
        response = self.client.post('/signup', data={
            'email': 'test@example.com',
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 200)
        user = User.query.filter_by(username='testuser').first()
        self.assertIsNotNone(user)

    def test_login_route(self):
        """Test the login route."""
        response = self.client.post('/login', data={
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 200)

    def test_logout_route(self):
        """Test the logout route."""
        response = self.client.get('/logout')
        self.assertEqual(response.status_code, 302)  # Should redirect to login page

    def test_search_route(self):
        """Test the search route."""
        response = self.client.post('/search', data={
            'excluded_ingredients': 'dairy,eggs'
        })
        self.assertEqual(response.status_code, 200)

    def test_save_recipe_route(self):
        """Test the save recipe route."""
        user = User(email='test@example.com', username='testuser', password='testpassword')
        db.session.add(user)
        db.session.commit()
        recipe = Recipe(spoonacular_id=123)
        db.session.add(recipe)
        db.session.commit()
        with app.test_client(session={'curr_user': user.id}) as client:
            response = client.post('/recipes/123/save')
            self.assertEqual(response.status_code, 200)

    def test_saved_route(self):
        """Test the saved recipes route."""
        user = User(email='test@example.com', username='testuser', password='testpassword')
        db.session.add(user)
        db.session.commit()
        recipe = Recipe(spoonacular_id=123)
        user.user_recipes.append(recipe)
        db.session.commit()
        with app.test_client(session={'curr_user': user.id}) as client:
            response = client.get('/saved')
            self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
