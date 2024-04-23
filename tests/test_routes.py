import unittest
from app import app, db
from app.models import User, Post

class TestRoutes(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Set up the Flask app and database for testing
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        db.create_all()

    @classmethod
    def tearDownClass(cls):
        # Clean up after testing
        db.session.remove()
        db.drop_all()

    def setUp(self):
        # Create a test client and push a test context
        self.client = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()

    def tearDown(self):
        # Pop the test context
        self.app_context.pop()

    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        # Add more assertions as needed for the home page

    def test_login_page(self):
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)
        # Add assertions for the login page

    def test_registration_page(self):
        response = self.client.get('/register')
        self.assertEqual(response.status_code, 200)
        # Add assertions for the registration page

    def test_edit_profile_page(self):
        # Assuming the route for editing profile is '/edit'
        response = self.client.get('/edit')
        self.assertEqual(response.status_code, 302)  # Redirects to login if not authenticated
        # Add assertions for authenticated user's access to edit profile page

    def test_user_authentication(self):
        # Test user registration
        response = self.client.post('/register', data={'username': 'test_user', 'email': 'test@example.com', 'password': 'password', 'password2': 'password'})
        self.assertEqual(response.status_code, 302)  # Redirects to login page after successful registration
        
        # Test user login
        response = self.client.post('/login', data={'username': 'test_user', 'password': 'password'}, follow_redirects=True)
        self.assertIn(b'Logged in successfully', response.data)

        # Test user logout
        response = self.client.get('/logout', follow_redirects=True)
        self.assertIn(b'You have been logged out', response.data)
        
    def test_database_interactions(self):
        # Test database interactions (assuming you have a User and Post model)
        user = User(username='test_user', email='test@example.com')
        db.session.add(user)
        db.session.commit()

        post = Post(body='Test post', author=user)
        db.session.add(post)
        db.session.commit()

        # Check if the post is present in the database
        self.assertTrue(Post.query.filter_by(body='Test post').first())

if __name__ == '__main__':
    unittest.main()
