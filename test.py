#!/usr/bin/env python
import unittest
from app import create_app, db
from app.models import User
from config import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'

class BaseTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()


class TestSourceModel(BaseTest):
    def test_as_dict(self):
        source = Source(title='Title')
        received = source.as_dict()
        expected = {
            'title': 'Title',
            'sphere': None,
            'city': None,
            'state': None,
            'country': None,
            'description': None,
            'official_link': None,
            'treatedLink': None
        }
        self.assertEqual(received, expected)


class UserModelCase(BaseTest):
    def test_password_hashing(self):
        u = User(username='susan')
        u.set_password('cat')
        self.assertFalse(u.check_password('dog'))
        self.assertTrue(u.check_password('cat'))

    def test_avatar(self):
        u = User(username='john', email='john@example.com')
        self.assertEqual(u.avatar(128), ('https://www.gravatar.com/avatar/'
                                         'd4c74594d841139328695756648b6bd6'
                                         '?d=identicon&s=128'))

