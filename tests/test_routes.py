import unittest
from app import app, db
from app.models import User, Post

class TestRoutes(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        cls.app = app.test_client()

        with app.app_context():
            db.create_all()

    @classmethod
    def tearDownClass(cls):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def setUp(self):
        self.client = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        self.clear_users()  

    def tearDown(self):
        self.app_context.pop()

    def clear_users(self):
        with app.app_context():
            User.query.delete()
            db.session.commit()

    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        
    def test_login_page(self):
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)
        
    def test_registration_page(self):
        response = self.client.get('/register')
        self.assertEqual(response.status_code, 200)
        
    def test_edit_profile_page(self):
        response = self.client.get('/edit')
        self.assertEqual(response.status_code, 302)  # Redirects to login if not authenticated
        
        
    def test_database_interactions(self):
        user = User(username='test_user', email='test@example.com')
        db.session.add(user)
        db.session.commit()

        post = Post(body='Test post', author=user)
        db.session.add(post)
        db.session.commit()

        self.assertTrue(Post.query.filter_by(body='Test post').first())

if __name__ == '__main__':
    unittest.main()
