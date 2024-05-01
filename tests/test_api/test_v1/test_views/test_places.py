#!/usr/bin/python3
'''Test places'''
from api.v1.app import app
from api.v1.views import places
from models.place import Place
from models.city import City
from models.state import State
from models.user import User
from models import storage
import unittest
import inspect
import pep8


class TestPlacesDocs(unittest.TestCase):
    '''Tests to check the documentation and style of places module'''
    @classmethod
    def setUpClass(cls):
        '''Set up for the doc tests'''
        cls.places_f = inspect.getmembers(places, inspect.isfunction)

    def test_pep8_conformance_places(self):
        '''Test that places conforms to PEP8.'''
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['api/v1/views/places.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_places(self):
        '''Test that tests/test_places.py conforms to PEP8.'''
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(
            ['tests/test_api/test_v1/test_views/test_places.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_places_module_docstring(self):
        '''Test for the places.py module docstring'''
        self.assertIsNot(places.__doc__, None,
                         "places.py needs a docstring")
        self.assertTrue(len(places.__doc__) >= 1,
                        "places.py needs a docstring")

    def test_places_func_docstrings(self):
        '''Test for the presence of docstrings in places functions'''
        for func in self.places_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestPlaces(unittest.TestCase):
    '''Test class for places view'''
    def setUp(self):
        '''Set up for tests'''
        self.york = State(name='New York')
        self.brok = City(name='Broklyn', state_id=self.york.id)
        self.user = User(email='JohnDoe@gmail.com', password='1234',
                         first_name='John', last_name='Doe')
        self.place_1 = Place(name='Place 1', city_id=self.brok.id,
                             user_id=self.user.id, number_rooms=3,
                             number_bathrooms=2, max_guest=6,
                             price_by_night=50)
        self.place_2 = Place(name='Place 2', city_id=self.brok.id,
                             user_id=self.user.id, number_rooms=2,
                             number_bathrooms=1, max_guest=5,
                             price_by_night=35)
        self.york.save()
        self.brok.save()
        self.user.save()
        self.place_1.save()
        self.place_2.save()

    def test_places(self):
        '''Test the places route'''
        with app.test_client() as c:
            resp = c.get('/api/v1/cities/{}/places'.format(self.brok.id))
            self.assertEqual(resp.status_code, 200)
            resp_json = resp.get_json()
            self.assertIsInstance(resp_json, list)
            self.assertEqual(len(resp_json), 2)
            self.assertIn(self.place_1.to_dict(), resp_json)
            self.assertIn(self.place_2.to_dict(), resp_json)

    def test_invalid_city_id(self):
        '''Test invalid city id'''
        with app.test_client() as c:
            resp = c.get('/api/v1/cities/{}/places'.format('12345'))
            self.assertEqual(resp.status_code, 404)

    def test_place(self):
        '''Test the place route'''
        with app.test_client() as c:
            resp = c.get('/api/v1/places/{}'.format(self.place_1.id))
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(self.place_1.to_dict(), resp.get_json())

    def test_place_invalid_id(self):
        '''Test invalid place id'''
        with app.test_client() as c:
            resp = c.get('/api/v1/places/{}'.format('12345'))
            self.assertEqual(resp.status_code, 404)

    def test_delete_place(self):
        '''Test delete place'''
        with app.test_client() as c:
            resp = c.delete('/api/v1/places/{}'.format(self.place_1.id))
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.get_json(), {})

    def test_delete_wrong_id(self):
        '''Test delete with wrong id'''
        with app.test_client() as c:
            resp = c.delete('/api/v1/places/{}'.format('12345'))
            self.assertEqual(resp.status_code, 404)

    def test_create_place(self):
        '''Test create place'''
        with app.test_client() as c:
            resp = c.post('/api/v1/cities/{}/places'.format(self.brok.id),
                          json={'user_id': self.user.id, 'name': 'Place 3',
                                'number_rooms': 3, 'number_bathrooms': 2,
                                'max_guest': 6, 'price_by_night': 50})
            self.assertEqual(resp.status_code, 201)
            self.assertIsInstance(resp.get_json(), dict)
            self.assertIn('id', resp.get_json())
            self.assertIn('created_at', resp.get_json())
            self.assertIn('updated_at', resp.get_json())
            self.assertIn('user_id', resp.get_json())
            self.assertIn('city_id', resp.get_json())
            self.assertIn('name', resp.get_json())
            self.assertIn('number_rooms', resp.get_json())
            self.assertIn('number_bathrooms', resp.get_json())
            self.assertIn('max_guest', resp.get_json())
            self.assertIn('price_by_night', resp.get_json())
            self.assertEqual(resp.get_json()['user_id'], self.user.id)
            self.assertEqual(resp.get_json()['city_id'], self.brok.id)
            self.assertEqual(resp.get_json()['name'], 'Place 3')
            self.assertEqual(resp.get_json()['number_rooms'], 3)
            self.assertEqual(resp.get_json()['number_bathrooms'], 2)
            self.assertEqual(resp.get_json()['max_guest'], 6)
            self.assertEqual(resp.get_json()['price_by_night'], 50)

    def test_create_place_invalid_city_id(self):
        '''Test create place invalid city id'''
        with app.test_client() as c:
            resp = c.post('/api/v1/cities/{}/places'.format('12345'),
                          json={'user_id': self.user.id, 'name': 'Place 3',
                                'number_rooms': 3, 'number_bathrooms': 2,
                                'max_guest': 6, 'price_by_night': 50})
            self.assertEqual(resp.status_code, 404)

    def test_create_place_no_json(self):
        '''Test create place no json'''
        with app.test_client() as c:
            resp = c.post('/api/v1/cities/{}/places'.format(self.brok.id))
            self.assertEqual(resp.status_code, 400)
            self.assertEqual(resp.get_json(), {'error': 'Not a JSON'})

    def test_create_place_no_user_id(self):
        '''Test create place no user id'''
        with app.test_client() as c:
            resp = c.post('/api/v1/cities/{}/places'.format(self.brok.id),
                          json={'name': 'Place 3', 'number_rooms': 3,
                                'number_bathrooms': 2, 'max_guest': 6,
                                'price_by_night': 50})
            self.assertEqual(resp.status_code, 400)

    def test_create_place_no_name(self):
        '''Test create place no name'''
        with app.test_client() as c:
            resp = c.post('/api/v1/cities/{}/places'.format(self.brok.id),
                          json={'user_id': self.user.id, 'number_rooms': 3,
                                'number_bathrooms': 2, 'max_guest': 6,
                                'price_by_night': 50})
            self.assertEqual(resp.status_code, 400)

    def test_update_place(self):
        '''Test update place'''
        with app.test_client() as c:
            resp = c.put('/api/v1/places/{}'.format(self.place_1.id),
                         json={'name': 'Updated Place 1'})
            self.assertEqual(resp.status_code, 200)
            self.assertIsInstance(resp.get_json(), dict)
            self.assertEqual(resp.get_json()['name'], 'Updated Place 1')

    def test_update_invalid_id(self):
        '''Test update invalid id'''
        with app.test_client() as c:
            resp = c.put('/api/v1/places/{}'.format('12345'),
                         json={'name': 'Updated Place 1'})
            self.assertEqual(resp.status_code, 404)

    def test_update_no_json(self):
        '''Test update no json'''
        with app.test_client() as c:
            resp = c.put('/api/v1/places/{}'.format(self.place_1.id))
            self.assertEqual(resp.status_code, 400)
            self.assertEqual(resp.get_json(), {'error': 'Not a JSON'})
