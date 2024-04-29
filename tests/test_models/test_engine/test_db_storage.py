#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""

from datetime import datetime
import inspect
import models
from models.engine import db_storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import json
import os
import pep8
import unittest
DBStorage = db_storage.DBStorage
classes = {"Amenity": Amenity, "City": City, "Place": Place,
           "Review": Review, "State": State, "User": User}


class TestDBStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of DBStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.dbs_f = inspect.getmembers(DBStorage, inspect.isfunction)

    def test_pep8_conformance_db_storage(self):
        """Test that models/engine/db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_db_storage(self):
        """Test tests/test_models/test_db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_engine/\
test_db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_db_storage_module_docstring(self):
        """Test for the db_storage.py module docstring"""
        self.assertIsNot(db_storage.__doc__, None,
                         "db_storage.py needs a docstring")
        self.assertTrue(len(db_storage.__doc__) >= 1,
                        "db_storage.py needs a docstring")

    def test_db_storage_class_docstring(self):
        """Test for the DBStorage class docstring"""
        self.assertIsNot(DBStorage.__doc__, None,
                         "DBStorage class needs a docstring")
        self.assertTrue(len(DBStorage.__doc__) >= 1,
                        "DBStorage class needs a docstring")

    def test_dbs_func_docstrings(self):
        """Test for the presence of docstrings in DBStorage methods"""
        for func in self.dbs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


@unittest.skipIf(models.storage_t != 'db', 'not testing db storage')
class TestFileStorage(unittest.TestCase):
    """Test the FileStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.storage = DBStorage()
        cls.storage.reload()

    def test_delete(self):
        """Test that delete removes an object from the database"""
        state = State(name="colorado")
        self.storage.new(state)
        self.storage.save()
        key = "{}.{}".format(type(state).__name__, state.id)
        self.assertIn(key, self.storage.all(State))
        self.storage.delete(state)
        self.assertNotIn(key, self.storage.all(State))

    def test_all_returns_dict(self):
        """Test that all returns a dictionary"""
        all_objects = self.storage.all()
        self.assertIsInstance(all_objects, dict)

    def test_all_no_class(self):
        """Test that all returns all rows when no class is passed"""
        all_objects = self.storage.all()
        self.assertEqual(len(all_objects), self.storage.count())

    def test_new(self):
        """test that new adds an object to the database"""
        state = State(name="colorado")
        self.storage.new(state)
        key = "{}.{}".format(type(state).__name__, state.id)
        self.assertIn(key, self.storage.all(State))

    def test_save(self):
        """Test that save properly saves objects to database"""
        state = State(name="colorado")
        self.storage.new(state)
        self.storage.save()
        self.storage.reload()
        key = "{}.{}".format(type(state).__name__, state.id)
        self.assertIn(key, self.storage.all(State))

    def test_get(self):
        '''Test that get retrive the correct object'''
        State_1 = State(name="colorado")
        State_2 = State(name="denver")
        self.storage.new(State_1)
        self.storage.new(State_2)
        self.assertIs(State_1, self.storage.get(State, State_1.id))
        self.assertIs(State_2, self.storage.get(State, State_2.id))

    def test_count(self):
        '''Test that count method count all the objects in for the class or
        all the objects'''
        State_1 = State(name="colorado")
        State_2 = State(name="denver")
        amenity_1 = Amenity(name="Coffe")
        States = self.storage.count(State)
        all = self.storage.count()
        self.storage.new(amenity_1)
        self.storage.new(State_1)
        self.storage.new(State_2)
        self.assertEqual(States + 2, self.storage.count(State))
        self.assertEqual(all + 3, self.storage.count())
