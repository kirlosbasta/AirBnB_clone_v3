#!/usr/bin/python3
'''Test Cities'''
from api.v1.views import cities
from api.v1.app import app
import inspect
from models.state import State
from models.city import City
from models import storage
import unittest
import pep8


class TestCitiesDocs(unittest.TestCase):
    '''Tests to check the documentation and style of cities module'''
    @classmethod
    def setUpClass(cls):
        '''Set up for the doc tests'''
        cls.cities_f = inspect.getmembers(cities, inspect.isfunction)

    def test_pep8_conformance_cities(self):
        '''Test that cities conforms to PEP8.'''
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['api/v1/views/cities.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_cities(self):
        '''Test that tests/test_cities.py conforms to PEP8.'''
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(
            ['tests/test_api/test_v1/test_views/test_cities.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_cities_module_docstring(self):
        '''Test for the cities.py module docstring'''
        self.assertIsNot(cities.__doc__, None,
                         "cities.py needs a docstring")
        self.assertTrue(len(cities.__doc__) >= 1,
                        "cities.py needs a docstring")

    def test_cities_func_docstrings(self):
        '''Test for the presence of docstrings in cities functions'''
        for func in self.cities_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestCities(unittest.TestCase):
    '''Test class for cities'''
    def setUp(self):
        '''Set up for the tests'''
        self.cal = State(name='California')
        self.cal.save()
        self.ala = State(name='Alabama')
        self.ala.save()
        self.cal_c1 = City(name='San Francisco', state_id=self.cal.id)
        self.cal_c1.save()
        self.ala_c1 = City(name='Montgomery', state_id=self.ala.id)
        self.ala_c1.save()
        self.ala_c2 = City(name='Birmingham', state_id=self.ala.id)
        self.ala_c2.save()

    def test_cities(self):
        '''Test the cities route'''
        with app.test_client() as c:
            resp = c.get('/api/v1/states/{}/cities'.format(self.cal.id))
            self.assertEqual(resp.status_code, 200)
            self.assertIsInstance(resp.get_json(), list)
            self.assertIn(self.cal_c1.to_dict(), resp.get_json())
            for city in resp.get_json():
                self.assertIsInstance(city, dict)
                self.assertIn('id', city)
                self.assertIn('created_at', city)
                self.assertIn('updated_at', city)

    def test_cities_wrong_id(self):
        '''Test cities with wrong state id'''
        with app.test_client() as c:
            resp = c.get('/api/v1/states/123456789/cities')
            self.assertEqual(resp.status_code, 404)

    def test_cities_id(self):
        '''Test cities with id'''
        with app.test_client() as c:
            resp = c.get('/api/v1/cities/{}'.format(self.cal_c1.id))
            self.assertEqual(resp.status_code, 200)
            self.assertIsInstance(resp.get_json(), dict)
            self.assertEqual(self.cal_c1.to_dict(), resp.get_json())

    def test_delete_city(self):
        '''Test delete city'''
        with app.test_client() as c:
            resp = c.delete('/api/v1/cities/{}'.format(self.cal_c1.id))
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.get_json(), {})

    def test_delete_wrong_city(self):
        '''Test delete with wrong id'''
        with app.test_client() as c:
            resp = c.delete('/api/v1/cities/123456789')
            self.assertEqual(resp.status_code, 404)

    def test_create_city(self):
        '''Test create city'''
        with app.test_client() as c:
            resp = c.post('/api/v1/states/{}/cities'.format(self.cal.id),
                          json={'name': 'Los Angeles'})
            self.assertEqual(resp.status_code, 201)
            self.assertIsInstance(resp.get_json(), dict)
            self.assertIn('id', resp.get_json())
            city_id = resp.get_json()['id']
            city = storage.get(City, city_id)
            self.assertEqual(city.name, 'Los Angeles')
            city.delete()

    def test_create_city_wrong_state(self):
        '''Test create city with wrong state id'''
        with app.test_client() as c:
            resp = c.post('/api/v1/states/123456789/cities',
                          json={'name': 'Los Angeles'})
            self.assertEqual(resp.status_code, 404)

    def test_create_city_no_json(self):
        '''Test create city with no json'''
        with app.test_client() as c:
            resp = c.post('/api/v1/states/{}/cities'.format(self.cal.id))
            self.assertEqual(resp.status_code, 400)
            self.assertEqual(resp.get_json(), {"error": "Not a JSON"})

    def test_create_city_no_name(self):
        '''Test create city with no name'''
        with app.test_client() as c:
            resp = c.post('/api/v1/states/{}/cities'.format(self.cal.id),
                          json={'foo': 'bar'})
            self.assertEqual(resp.status_code, 400)
            self.assertEqual(resp.get_json(), {"error": "Missing name"})

    def test_update_city(self):
        '''Test update city'''
        with app.test_client() as c:
            resp = c.put('/api/v1/cities/{}'.format(self.cal_c1.id),
                         json={'name': 'San Jose'})
            new = storage.get(City, self.cal_c1.id)
            self.assertEqual(resp.status_code, 200)
            self.assertIsInstance(resp.get_json(), dict)
            self.assertEqual(resp.get_json()['name'], 'San Jose')
            self.assertEqual(new.name, 'San Jose')
            self.assertEqual(resp.get_json()['id'], self.cal_c1.id)
            self.assertEqual(resp.get_json()['state_id'], self.cal.id)

    def test_update_city_wrong_id(self):
        '''Test update city with wrong id'''
        with app.test_client() as c:
            resp = c.put('/api/v1/cities/123456789', json={'name': 'San Jose'})
            self.assertEqual(resp.status_code, 404)

    def test_update_city_no_json(self):
        '''Test update city with no json'''
        with app.test_client() as c:
            resp = c.put('/api/v1/cities/{}'.format(self.cal_c1.id))
            self.assertEqual(resp.status_code, 400)
            self.assertEqual(resp.get_json(), {"error": "Not a JSON"})
