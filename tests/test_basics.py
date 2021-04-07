import unittest
from flask import current_app
from app import create_app, db
from app.models import User


class BasicsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_app_exists(self):
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])

    def test_user_model(self):
        u = User()
        u.username = 'Winking face 😉'   # Test for unicode
        u.password = 'cat'
        self.assertEqual(u.username, 'Winking face 😉')
        self.assertTrue(u.verify_password('cat'))
        self.assertFalse(u.verify_password('dog'))
        with self.assertRaises(AttributeError):
            password = u.password
        u2 = User
        u2.password = 'cat'
        self.assertFalse(u.password_hash == u2.password_hash)

    def test_user_login(self):
        u = User()
        with self.assertRaises(AttributeError):
            u.is_authenticated = True
        with self.assertRaises(AttributeError):
            u.is_active = True
        with self.assertRaises(AttributeError):
            u.is_anonymous = False
        self.assertTrue(u.is_authenticated)
        self.assertTrue(u.is_active)
        self.assertFalse(u.is_anonymous)
