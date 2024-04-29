#!/usr/bin/python3
'''Test module for app.py'''
from api.v1 import app
from flask import Flask
import inspect
import unittest
import pep8
import os


class TestAppDocs(unittest.TestCase):
    '''Test class for app documentation'''
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.app_f = inspect.getmembers(app, inspect.isfunction)

    def test_pep8_conformance_app(self):
        """Test that api/v1/app.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['api/v1/app.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_app(self):
        """Test that tests/test_api/test_v1/test_app.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_api/test_v1/test_app.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_app_module_docstring(self):
        """Test for the app.py docstring"""
        self.assertIsNot(app.__doc__, None,
                         "app.py needs a docstring")
        self.assertTrue(len(app.__doc__) >= 1,
                        "app.py needs a docstring")

    def test_app_func_docstrings(self):
        """Test for the presence of docstrings in app methods"""
        for func in self.app_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestApp(unittest.TestCase):
    '''Test class for app.py'''
    def test_app_type(self):
        '''Type of app'''
        self.assertIsInstance(app.app, Flask)

    def test_app_name(self):
        '''Name of app'''
        self.assertEqual(app.app.name, 'api.v1.app')
