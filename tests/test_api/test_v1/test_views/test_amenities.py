#!/usr/bin/python3
'''Test amenities'''
from api.v1.views import amenities
from api.v1.app import app
import inspect
from models.amenity import Amenity
from models import storage
import unittest
import pep8


class TestAmenitiesDocs(unittest.TestCase):
    '''Tests to check the documentation and style of amenities module'''
    @classmethod
    def setUpClass(cls):
        '''Set up for the doc tests'''
        cls.amenities_f = inspect.getmembers(amenities, inspect.isfunction)

    def test_pep8_conformance_amenities(self):
        '''Test that amenities conforms to PEP8.'''
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['api/v1/views/amenities.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_amenities(self):
        '''Test that tests/test_amenities.py conforms to PEP8.'''
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(
            ['tests/test_api/test_v1/test_views/test_amenities.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_amenities_module_docstring(self):
        '''Test for the amenities.py module docstring'''
        self.assertIsNot(amenities.__doc__, None,
                         "amenities.py needs a docstring")
        self.assertTrue(len(amenities.__doc__) >= 1,
                        "amenities.py needs a docstring")

    def test_amenities_func_docstrings(self):
        '''Test for the presence of docstrings in amenities functions'''
        for func in self.amenities_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestAmenities(unittest.TestCase):
    '''Test class for amenities api'''
    def setUp(self):
        '''Set up for the tests'''
        self.amenity = Amenity(name='wifi')
        self.amenity.save()

    def test_get_amenities(self):
        '''Test to get all amenities'''
        with app.test_client() as c:
            rv = c.get('/api/v1/amenities')
            resp = rv.get_json()
            self.assertEqual(rv.status_code, 200)
            self.assertIsInstance(resp, list)
            self.assertIn(self.amenity.to_dict(), resp)
            for amenity in resp:
                self.assertIsInstance(amenity, dict)
                self.assertIn('id', amenity)
                self.assertIn('created_at', amenity)
                self.assertIn('updated_at', amenity)
                self.assertIn('__class__', amenity)
                self.assertEqual(amenity['__class__'], 'Amenity')

    def test_amenities_id(self):
        '''Test to get amenities by id'''
        with app.test_client() as c:
            rv = c.get('/api/v1/amenities/{}'.format(self.amenity.id))
            resp = rv.get_json()
            self.assertEqual(rv.status_code, 200)
            self.assertIsInstance(resp, dict)
            self.assertEqual(self.amenity.to_dict(), resp)

    def test_amenities_id_invalid(self):
        '''Test to get amenities by invalid id'''
        with app.test_client() as c:
            rv = c.get('/api/v1/amenities/{}'.format('12345'))
            self.assertEqual(rv.status_code, 404)

    def test_delete_amenities_id(self):
        '''Test to delete amenities by id'''
        with app.test_client() as c:
            rv = c.delete('/api/v1/amenities/{}'.format(self.amenity.id))
            resp = rv.get_json()
            self.assertEqual(rv.status_code, 200)
            self.assertEqual(resp, {})

    def test_delete_amenities_id_invalid(self):
        '''Test to delete amenities by invalid id'''
        with app.test_client() as c:
            rv = c.delete('/api/v1/amenities/{}'.format('12345'))
            self.assertEqual(rv.status_code, 404)

    def test_create_amenity(self):
        '''Test to create a new amenity'''
        with app.test_client() as c:
            rv = c.post('/api/v1/amenities', json={'name': 'pool'})
            resp = rv.get_json()
            self.assertEqual(rv.status_code, 201)
            self.assertIsInstance(resp, dict)
            self.assertIn('id', resp)
            self.assertIn('created_at', resp)
            self.assertIn('updated_at', resp)
            self.assertIn('name', resp)
            self.assertEqual(resp['name'], 'pool')

    def test_create_amenity_no_json(self):
        '''Test to create a new amenity with no json'''
        with app.test_client() as c:
            rv = c.post('/api/v1/amenities')
            self.assertEqual(rv.status_code, 400)
            self.assertEqual(rv.get_json(), {'error': 'Not a JSON'})

    def test_create_amenity_no_name(self):
        '''Test to create a new amenity with no name'''
        with app.test_client() as c:
            rv = c.post('/api/v1/amenities', json={})
            self.assertEqual(rv.status_code, 400)
            self.assertEqual(rv.get_json(), {'error': 'Missing name'})

    def test_update_amenity(self):
        '''Test to update an amenity'''
        with app.test_client() as c:
            rv = c.put('/api/v1/amenities/{}'.format(self.amenity.id),
                       json={'name': 'pool'})
            resp = rv.get_json()
            self.assertEqual(rv.status_code, 200)
            self.assertIsInstance(resp, dict)
            self.assertIn('id', resp)
            self.assertIn('created_at', resp)
            self.assertIn('updated_at', resp)
            self.assertIn('name', resp)
            self.assertEqual(resp['name'], 'pool')

    def test_update_amenity_invalid_id(self):
        '''Test to update an amenity with invalid id'''
        with app.test_client() as c:
            rv = c.put('/api/v1/amenities/{}'.format('12345'),
                       json={'name': 'pool'})
            self.assertEqual(rv.status_code, 404)

    def test_update_amenity_no_json(self):
        '''Test to update an amenity with no json'''
        with app.test_client() as c:
            rv = c.put('/api/v1/amenities/{}'.format(self.amenity.id))
            self.assertEqual(rv.status_code, 400)
            self.assertEqual(rv.get_json(), {'error': 'Not a JSON'})
