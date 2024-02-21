#!/usr/bin/python3
""" Tests Amenity model"""
from tests.test_models.test_base_model import test_basemodel
from models.amenity import Amenity
import os


class test_Amenity(test_basemodel):
    """ Tests Amenity model"""

    def __init__(self, *args, **kwargs):
        """ Initialized the tests for Amenity model """
        super().__init__(*args, **kwargs)
        self.name = "Amenity"
        self.value = Amenity

    def test_name2(self):
        """ Tests the type of name  """
        new = self.value()
        self.assertNotEqual(
            type(new.name),
            str if os.getenv('HBNB_TYPE_STORAGE') != 'db' else type(None))
