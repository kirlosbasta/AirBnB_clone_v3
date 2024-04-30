#!/usr/bin/python3
'''Test users'''
from api.v1.views import users
from api.v1.app import app
import inspect
from models.user import User
from models import storage
import unittest
import pep8


class TestUsersDocs(unittest.TestCase):
    '''Tests to check the documentation and style of users module'''
    @classmethod
    def setUpClass(cls):
        '''Set up for the doc tests'''
        cls.users_f = inspect.getmembers(users, inspect.isfunction)

    def test_pep8_conformance_users(self):
        '''Test that users conforms to PEP8.'''
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['api/v1/views/users.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_users(self):
        '''Test that tests/test_users.py conforms to PEP8.'''
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(
            ['tests/test_api/test_v1/test_views/test_users.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_users_module_docstring(self):
        '''Test for the users.py module docstring'''
        self.assertIsNot(users.__doc__, None,
                         "users.py needs a docstring")
        self.assertTrue(len(users.__doc__) >= 1,
                        "users.py needs a docstring")

    def test_users_func_docstrings(self):
        '''Test for the presence of docstrings in users functions'''
        for func in self.users_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestUsers(unittest.TestCase):
    '''Test class for users api'''
    def setUp(self):
        '''Set up for the tests'''
        self.user = User(email='JohnDoe@gmail.com', password='1234',
                         first_name='John', last_name='Doe')
        self.user.save()

    def test_get_users(self):
        '''Test to get all users'''
        with app.test_client() as c:
            rv = c.get('/api/v1/users')
            json_response = rv.get_json()
            self.assertEqual(rv.status_code, 200)
            self.assertIsInstance(json_response, list)
            self.assertIn(self.user.to_dict(), json_response)

    def test_user_id(self):
        '''Test to get user by id'''
        with app.test_client() as c:
            rv = c.get('/api/v1/users/{}'.format(self.user.id))
            json_response = rv.get_json()
            self.assertEqual(rv.status_code, 200)
            self.assertEqual(self.user.to_dict(), json_response)

    def test_user_invalid_id(self):
        '''Test to get user by invalid id'''
        with app.test_client() as c:
            rv = c.get('/api/v1/users/{}'.format('12345'))
            self.assertEqual(rv.status_code, 404)

    def test_delete_user(self):
        '''Test to delete user'''
        with app.test_client() as c:
            rv = c.delete('/api/v1/users/{}'.format(self.user.id))
            self.assertEqual(rv.status_code, 200)
            self.assertEqual(rv.get_json(), {})

    def test_delete_invalid_user(self):
        '''Test to delete invalid user'''
        with app.test_client() as c:
            rv = c.delete('/api/v1/users/{}'.format('12345'))
            self.assertEqual(rv.status_code, 404)

    def test_create_user(self):
        '''Test to create user'''
        with app.test_client() as c:
            rv = c.post('/api/v1/users', json={'email': 'JohnDoe@gmail.com',
                                               'password': '1234',
                                               'first_name': 'John',
                                               'last_name': 'Doe'})
            json_response = rv.get_json()
            self.assertEqual(rv.status_code, 201)
            self.assertIsInstance(json_response, dict)
            self.assertIn('id', json_response)
            self.assertIn('created_at', json_response)
            self.assertIn('updated_at', json_response)
            self.assertIn('email', json_response)
            self.assertIn('password', json_response)
            self.assertIn('first_name', json_response)
            self.assertIn('last_name', json_response)
            self.assertEqual(json_response['email'], 'JohnDoe@gmail.com')
            self.assertEqual(json_response['password'], '1234')
            self.assertEqual(json_response['first_name'], 'John')
            self.assertEqual(json_response['last_name'], 'Doe')

    def test_create_user_no_json(self):
        '''Test to create user with no json'''
        with app.test_client() as c:
            rv = c.post('/api/v1/users')
            self.assertEqual(rv.status_code, 400)
            self.assertEqual(rv.get_json(), {'error': 'Not a JSON'})

    def test_create_user_no_email(self):
        '''Test to create user with no email'''
        with app.test_client() as c:
            rv = c.post('/api/v1/users', json={'password': '1234',
                                               'first_name': 'John',
                                               'last_name': 'Doe'})
            self.assertEqual(rv.status_code, 400)
            self.assertEqual(rv.get_json(), {'error': 'Missing email'})

    def test_create_user_no_password(self):
        '''Test to create user with no password'''
        with app.test_client() as c:
            rv = c.post('/api/v1/users', json={'email': 'JohnDoe@gmail.com',
                                               'first_name': 'John',
                                               'last_name': 'Doe'})
            self.assertEqual(rv.status_code, 400)
            self.assertEqual(rv.get_json(), {'error': 'Missing password'})

    def test_update_user(self):
        '''Test to update user'''
        with app.test_client() as c:
            rv = c.put('/api/v1/users/{}'.format(self.user.id),
                       json={'first_name': 'Jane', 'last_name': 'Air'})
            json_response = rv.get_json()
            self.assertEqual(rv.status_code, 200)
            self.assertIsInstance(json_response, dict)
            self.assertIn('id', json_response)
            self.assertIn('created_at', json_response)
            self.assertIn('updated_at', json_response)
            self.assertIn('email', json_response)
            self.assertIn('password', json_response)
            self.assertIn('first_name', json_response)
            self.assertIn('last_name', json_response)
            self.assertEqual(json_response['email'], self.user.email)
            self.assertEqual(json_response['password'], self.user.password)
            self.assertEqual(json_response['first_name'], 'Jane')
            self.assertEqual(json_response['last_name'], 'Air')

    def test_update_user_invalid_id(self):
        '''Test to update user with invalid id'''
        with app.test_client() as c:
            rv = c.put('/api/v1/users/{}'.format('12345'),
                       json={'first_name': 'Jane', 'last_name': 'Air'})
            self.assertEqual(rv.status_code, 404)

    def test_update_user_no_json(self):
        '''Test to update user with no json'''
        with app.test_client() as c:
            rv = c.put('/api/v1/users/{}'.format(self.user.id))
            self.assertEqual(rv.status_code, 400)
            self.assertEqual(rv.get_json(), {'error': 'Not a JSON'})
