#!/usr/bin/python3
'''states test module'''
from api.v1.views import states
from api.v1.app import app
import inspect
from models.state import State
import unittest
import pep8


class TestStatesDocs(unittest.TestCase):
    '''Tests to check the documentation and style of states module'''
    @classmethod
    def setUpClass(cls):
        '''Set up for the doc tests'''
        cls.states_f = inspect.getmembers(states, inspect.isfunction)

    def test_pep8_conformance_states(self):
        '''Test that states conforms to PEP8.'''
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['api/v1/views/states.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_states(self):
        '''Test that tests/test_states.py conforms to PEP8.'''
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(
            ['tests/test_api/test_v1/test_views/test_states.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_states_module_docstring(self):
        '''Test for the states.py module docstring'''
        self.assertIsNot(states.__doc__, None,
                         "states.py needs a docstring")
        self.assertTrue(len(states.__doc__) >= 1,
                        "states.py needs a docstring")

    def test_states_func_docstrings(self):
        '''Test for the presence of docstrings in states functions'''
        for func in self.states_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestStates(unittest.TestCase):
    '''Test class for states view'''
    def test_states(self):
        '''Test the states route'''
        with app.test_client() as c:
            resp = c.get('/api/v1/states')
            self.assertEqual(resp.status_code, 200)
            self.assertIsInstance(resp.get_json(), list)
            for state in resp.get_json():
                self.assertIsInstance(state, dict)
                self.assertIn('id', state)
                self.assertIn('created_at', state)
                self.assertIn('updated_at', state)
                self.assertIn('__class__', state)
                self.assertEqual(state['__class__'], 'State')

    def test_states_id(self):
        '''Test states with id'''
        with app.test_client() as c:
            state = State(name='Alabama')
            state.save()
            resp = c.get('/api/v1/states/{}'.format(state.id))
            resp_state = resp.get_json()
            self.assertEqual(resp.status_code, 200)
            self.assertIsInstance(resp.get_json(), dict)
            self.assertIn('id', resp_state)
            self.assertIn('name', resp_state)
            self.assertIn('created_at', resp_state)
            self.assertIn('updated_at', resp_state)
            self.assertIn('__class__', resp_state)
            self.assertEqual(resp_state['__class__'], 'State')
            self.assertEqual(resp_state['name'], 'Alabama')
            self.assertEqual(resp_state['id'], state.id)

    def test_states_wrong_id(self):
        '''Test states with wrong id'''
        with app.test_client() as c:
            resp = c.get('/api/v1/states/123456')
            self.assertEqual(resp.status_code, 404)

    def test_delete_state(self):
        '''Test delete state'''
        with app.test_client() as c:
            state = State(name='Alabama')
            state.save()
            resp = c.delete('/api/v1/states/{}'.format(state.id))
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.get_json(), {})

    def test_delete_wrong_id(self):
        '''Test delete with wrong id'''
        with app.test_client() as c:
            resp = c.delete('/api/v1/states/123456')
            self.assertEqual(resp.status_code, 404)

    def test_create_state(self):
        '''Test create state'''
        with app.test_client() as c:
            resp = c.post('/api/v1/states', json={'name': 'Alabama'})
            self.assertEqual(resp.status_code, 201)
            self.assertIsInstance(resp.get_json(), dict)
            self.assertIn('id', resp.get_json())
            self.assertIn('name', resp.get_json())
            self.assertIn('created_at', resp.get_json())
            self.assertIn('updated_at', resp.get_json())
            self.assertIn('__class__', resp.get_json())
            self.assertEqual(resp.get_json()['name'], 'Alabama')
            self.assertEqual(resp.get_json()['__class__'], 'State')

    def test_create_state_no_json(self):
        '''Test create state no json'''
        with app.test_client() as c:
            resp = c.post('/api/v1/states')
            self.assertEqual(resp.status_code, 400)
            self.assertEqual(resp.get_json(), {'error': 'Not a JSON'})

    def test_create_state_no_name(self):
        '''Test create state no name'''
        with app.test_client() as c:
            resp = c.post('/api/v1/states', json={'notname': 'Alabama'})
            self.assertEqual(resp.status_code, 400)
            self.assertEqual(resp.get_json(), {'error': 'Missing name'})

    def test_update_state(self):
        '''Test update state'''
        with app.test_client() as c:
            state = State(name='Alabama')
            state.save()
            resp = c.put('/api/v1/states/{}'.format(state.id),
                         json={'name': 'New York'})
            self.assertEqual(resp.status_code, 200)
            self.assertIsInstance(resp.get_json(), dict)
            self.assertEqual(resp.get_json()['name'], 'New York')

    def test_update_state_no_json(self):
        '''Test update state no json'''
        with app.test_client() as c:
            state = State(name='Alabama')
            state.save()
            resp = c.put('/api/v1/states/{}'.format(state.id))
            self.assertEqual(resp.status_code, 400)
            self.assertEqual(resp.get_json(), {'error': 'Not a JSON'})

    def test_update_state_wrong_id(self):
        '''Test update state wrong id'''
        with app.test_client() as c:
            resp = c.put('/api/v1/states/123456')
            self.assertEqual(resp.status_code, 404)
