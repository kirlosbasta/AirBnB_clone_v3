#!/usr/bin/python3
'''views test module'''
from api.v1.views import index
from api.v1.app import app
import inspect
import unittest
import pep8


class TestIndexDocs(unittest.TestCase):
    '''Tests to check the documentation and style of index module'''
    @classmethod
    def setUpClass(cls):
        '''Set up for the doc tests'''
        cls.index_f = inspect.getmembers(index, inspect.isfunction)

    def test_pep8_conformance_views(self):
        '''Test that views conforms to PEP8.'''
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['api/v1/views/index.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_views(self):
        '''Test that tests/test_views/test_index.py conforms to PEP8.'''
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(
            ['tests/test_api/test_v1/test_views/test_index.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_views_module_docstring(self):
        '''Test for the index.py module docstring'''
        self.assertIsNot(index.__doc__, None,
                         "index.py needs a docstring")
        self.assertTrue(len(index.__doc__) >= 1,
                        "index.py needs a docstring")

    def test_views_func_docstrings(self):
        '''Test for the presence of docstrings in index functions'''
        for func in self.index_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestIndex(unittest.TestCase):
    '''Test class for index view'''
    def test_index_status(self):
        '''Test the status route'''
        with app.test_client() as c:
            resp = c.get('/api/v1/status')
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.get_json(), {"status": "OK"})

    def test_index_stats(self):
        '''Test the stats route'''
        with app.test_client() as c:
            resp = c.get('/api/v1/stats')
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(len(resp.get_json()), 6)
            for key, value in resp.get_json().items():
                self.assertIn(key, ["amenities", "cities", "places",
                                    "reviews", "states", "users"])
                self.assertIsInstance(value, int)
                self.assertTrue(value >= 0)
