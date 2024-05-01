#!/usr/bin/python3
'''Test places reviews'''
from api.v1.app import app
from api.v1.views import place_reviews
from models import storage
from models.city import City
from models.review import Review
from models.place import Place
from models.user import User
from models.state import State
import unittest
import inspect
import pep8


class TestPlacesReviewsDocs(unittest.TestCase):
    '''Tests to check the documentation and style of places_reviews module'''
    @classmethod
    def setUpClass(cls):
        '''Set up for the doc tests'''
        cls.place_reviews_f = inspect.getmembers(place_reviews,
                                                 inspect.isfunction)

    def test_pep8_conformance_places_reviews(self):
        '''Test that places_reviews conforms to PEP8.'''
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['api/v1/views/places_reviews.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_places_reviews(self):
        '''Test that tests/test_places_reviews.py conforms to PEP8.'''
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(
            ['tests/test_api/test_v1/test_views/test_places_reviews.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_places_reviews_module_docstring(self):
        '''Test for the places_reviews.py module docstring'''
        self.assertIsNot(place_reviews.__doc__, None,
                         "places_reviews.py needs a docstring")
        self.assertTrue(len(place_reviews.__doc__) >= 1,
                        "places_reviews.py needs a docstring")

    def test_places_reviews_func_docstrings(self):
        '''Test for the presence of docstrings in places_reviews functions'''
        for func in self.place_reviews_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestPlacesReviews(unittest.TestCase):
    '''Test class for places_reviews view'''
    def setUp(self):
        '''Set up for tests'''
        self.user = User(email='JohnDoe@gmail.com', password='1234',
                         first_name='John', last_name='Doe')
        self.york = State(name='New York')
        self.brok = City(name='Broklyn', state_id=self.york.id)
        self.place_1 = Place(name='Place 1', city_id=self.brok.id,
                             user_id=self.user.id, number_rooms=3,
                             number_bathrooms=2, max_guest=6,
                             price_by_night=50)
        self.place_2 = Place(name='Place 2', city_id=self.brok.id,
                             user_id=self.user.id, number_rooms=2,
                             number_bathrooms=1, max_guest=5,
                             price_by_night=35)
        self.review_1 = Review(text='Great', place_id=self.place_1.id,
                               user_id=self.user.id)
        self.york.save()
        self.brok.save()
        self.user.save()
        self.place_1.save()
        self.place_2.save()
        self.review_1.save()

    def test_get_place_reviews(self):
        '''Test to get all reviews of a place'''
        with app.test_client() as c:
            rv = c.get('/api/v1/places/{}/reviews'.format(self.place_1.id))
            response = rv.get_json()
            self.assertEqual(rv.status_code, 200)
            self.assertEqual(len(response), 1)
            self.assertEqual(response[0], self.review_1.to_dict())

    def test_get_place_review_invalid_id(self):
        '''Test to get reviews of a place with invalid id'''
        with app.test_client() as c:
            rv = c.get('/api/v1/places/{}/reviews'.format('invalid_id'))
            self.assertEqual(rv.status_code, 404)

    def test_get_review(self):
        '''Test to get review by id'''
        with app.test_client() as c:
            rv = c.get('/api/v1/reviews/{}'.format(self.review_1.id))
            response = rv.get_json()
            self.assertEqual(rv.status_code, 200)
            self.assertEqual(response, self.review_1.to_dict())

    def test_review_invalid_id(self):
        '''Test to get review by invalid id'''
        with app.test_client() as c:
            rv = c.get('/api/v1/reviews/{}'.format('invalid_id'))
            self.assertEqual(rv.status_code, 404)

    def test_delete_review(self):
        '''Test to delete review'''
        with app.test_client() as c:
            rv = c.delete('/api/v1/reviews/{}'.format(self.review_1.id))
            self.assertEqual(rv.status_code, 200)
            self.assertEqual(rv.get_json(), {})

    def test_delete_invalid_review(self):
        '''Test to delete invalid review'''
        with app.test_client() as c:
            rv = c.delete('/api/v1/reviews/{}'.format('invalid_id'))
            self.assertEqual(rv.status_code, 404)

    def test_create_reveiw(self):
        '''Test to create review'''
        with app.test_client() as c:
            rv = c.post('/api/v1/places/{}/reviews'.format(self.place_1.id),
                        json={'user_id': self.user.id, 'text': 'Great'})
            response = rv.get_json()
            self.assertEqual(rv.status_code, 201)
            self.assertIsInstance(response, dict)
            self.assertIn('id', response)
            self.assertIn('created_at', response)
            self.assertIn('updated_at', response)
            self.assertIn('user_id', response)
            self.assertIn('place_id', response)
            self.assertIn('text', response)
            self.assertEqual(response['user_id'], self.user.id)
            self.assertEqual(response['place_id'], self.place_1.id)
            self.assertEqual(response['text'], 'Great')

    def test_create_review_no_json(self):
        '''Test to create review with no json'''
        with app.test_client() as c:
            rv = c.post('/api/v1/places/{}/reviews'.format(self.place_1.id))
            self.assertEqual(rv.status_code, 400)
            self.assertEqual(rv.get_json(), {'error': 'Not a JSON'})

    def test_create_invalid_id(self):
        ''''Test to create review with invalid id'''
        with app.test_client() as c:
            rv = c.post('/api/v1/places/{}/reviews'.format('invalid_id'),
                        json={'user_id': self.user.id, 'text': 'Great'})
            self.assertEqual(rv.status_code, 404)

    def test_create_review_no_user_id(self):
        '''Test to create review with no user id'''
        with app.test_client() as c:
            rv = c.post('/api/v1/places/{}/reviews'.format(self.place_1.id),
                        json={'text': 'Great'})
            self.assertEqual(rv.status_code, 400)
            self.assertEqual(rv.get_json(), {'error': 'Missing user_id'})

    def test_create_review_no_text(self):
        '''Test to create review with no text'''
        with app.test_client() as c:
            rv = c.post('/api/v1/places/{}/reviews'.format(self.place_1.id),
                        json={'user_id': self.user.id})
            self.assertEqual(rv.status_code, 400)
            self.assertEqual(rv.get_json(), {'error': 'Missing text'})

    def test_update_review(self):
        '''Test to update review'''
        with app.test_client() as c:
            rv = c.put('/api/v1/reviews/{}'.format(self.review_1.id),
                       json={'text': 'Awesome'})
            response = rv.get_json()
            self.assertEqual(rv.status_code, 200)
            self.assertEqual(response['text'], 'Awesome')
            self.assertEqual(response['user_id'], self.user.id)
            self.assertEqual(response['place_id'], self.place_1.id)
            self.assertEqual(response['id'], self.review_1.id)

    def test_update_review_invalid_id(self):
        '''Test to update review with invalid id'''
        with app.test_client() as c:
            rv = c.put('/api/v1/reviews/{}'.format('invalid_id'),
                       json={'text': 'Awesome'})
            self.assertEqual(rv.status_code, 404)

    def test_update_review_no_json(self):
        '''Test to update review with no json'''
        with app.test_client() as c:
            rv = c.put('/api/v1/reviews/{}'.format(self.review_1.id))
            self.assertEqual(rv.status_code, 400)
            self.assertEqual(rv.get_json(), {'error': 'Not a JSON'})
