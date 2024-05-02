#!/usr/bin/python3
'''Test places_amenities'''
from api.v1.app import app
from api.v1.views import places_amenities
from models import storage
from models import storage_t
from models.place import Place
from models.amenity import Amenity
from models.city import City
from models.state import State
from models.user import User
import unittest
import inspect
import pep8


class TestPlacesAmenitiesDocs(unittest.TestCase):
    '''Tests to check the documentation and style of places_amenities module'''
    @classmethod
    def setUpClass(cls):
        '''Set up for the doc tests'''
        cls.places_amenities_f = inspect.getmembers(places_amenities,
                                                    inspect.isfunction)

    def test_pep8_conformance_places_amenities(self):
        '''Test that places_amenities conforms to PEP8.'''
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['api/v1/views/places_amenities.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_places_amenities(self):
        '''Test that tests/test_places_amenities.py conforms to PEP8.'''
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(
            ['tests/test_api/test_v1/test_views/test_places_amenities.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_places_amenities_module_docstring(self):
        '''Test for the places_amenities.py module docstring'''
        self.assertIsNot(places_amenities.__doc__, None,
                         "places_reviews.py needs a docstring")
        self.assertTrue(len(places_amenities.__doc__) >= 1,
                        "places_reviews.py needs a docstring")

    def test_places_amenities_func_docstrings(self):
        '''Test for the presence of docstrings in places_amenities functions'''
        for func in self.places_amenities_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestPlacesAmenities(unittest.TestCase):
    '''Test class for places_amenities view'''
    def setUp(self):
        '''Set up for tests'''
        self.user = User(email='JohnDoe@gmail.com', password='1234',
                         first_name='John', last_name='Doe')
        self.york = State(name='New York')
        self.brok = City(name='Broklyn', state_id=self.york.id)
        self.amenity_1 = Amenity(name='Wifi')
        self.amenity_2 = Amenity(name='Cable')
        self.place_1 = Place(name='Place 1', city_id=self.brok.id,
                             user_id=self.user.id, number_rooms=3,
                             number_bathrooms=2, max_guest=6,
                             price_by_night=50)
        if storage_t == 'db':
            self.place_1.amenities.append(self.amenity_1)
            self.place_1.amenities.append(self.amenity_2)
        else:
            setattr(self.place_1, 'amenity_ids', [self.amenity_1.id,
                                                  self.amenity_2.id])
        self.york.save()
        self.brok.save()
        self.user.save()
        self.place_1.save()
        self.amenity_1.save()
        self.amenity_2.save()

    def test_get_amenities_by_place(self):
        '''Test to get all amenities of a place'''
        with app.test_client() as c:
            resp = c.get('/api/v1/places/{}/amenities'.format(self.place_1.id))
            self.assertEqual(resp.status_code, 200)
            resp_json = resp.get_json()
            self.assertEqual(len(resp_json), 2)

    def test_invalid_place_id(self):
        '''Test invalid place id'''
        with app.test_client() as c:
            resp = c.get('/api/v1/places/{}/amenities'.format('12345'))
            self.assertEqual(resp.status_code, 404)

    def test_delete_amenity_from_place(self):
        '''Test to delete an amenity from a place'''
        with app.test_client() as c:
            resp = c.delete('/api/v1/places/{}/amenities/{}'.format(
                self.place_1.id, self.amenity_1.id))
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.get_json(), {})
            if storage_t == 'db':
                self.assertNotIn(self.amenity_1, self.place_1.amenities)
            else:
                self.assertNotIn(self.amenity_1.id, self.place_1.amenity_ids)

    def test_delete_invalid_amenity_id(self):
        '''Test invalid amenity id'''
        with app.test_client() as c:
            resp = c.delete('/api/v1/places/{}/amenities/{}'.format(
                self.place_1.id, '12345'))
            self.assertEqual(resp.status_code, 404)

    def test_delete_invalid_place_id(self):
        '''Test invalid place id'''
        with app.test_client() as c:
            resp = c.delete('/api/v1/places/{}/amenities/{}'.format(
                '12345', self.amenity_1.id))
            self.assertEqual(resp.status_code, 404)

    def test_link_amenity_to_place(self):
        '''Test to link an amenity to a place'''
        self.amenity_3 = Amenity(name='Parking')
        self.amenity_3.save()
        with app.test_client() as c:
            resp = c.post('/api/v1/places/{}/amenities/{}'.format(
                self.place_1.id, self.amenity_3.id))
            self.assertEqual(resp.status_code, 201)
            self.assertEqual(resp.get_json()['name'], self.amenity_3.name)
            self.assertEqual(resp.get_json()['id'], self.amenity_3.id)
            if storage_t == 'db':
                self.assertIn(self.amenity_3, self.place_1.amenities)
            else:
                self.assertIn(self.amenity_3.id, self.place_1.amenity_ids)

    def test_link_invalid_amenity_id(self):
        '''Test invalid amenity id'''
        with app.test_client() as c:
            resp = c.post('/api/v1/places/{}/amenities/{}'.format(
                self.place_1.id, '12345'))
            self.assertEqual(resp.status_code, 404)

    def test_link_invalid_place_id(self):
        '''Test invalid place id'''
        with app.test_client() as c:
            resp = c.post('/api/v1/places/{}/amenities/{}'.format(
                '12345', self.amenity_1.id))
            self.assertEqual(resp.status_code, 404)
