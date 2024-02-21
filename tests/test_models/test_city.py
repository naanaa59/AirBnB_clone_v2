#!/usr/bin/python3
""" Tests city model """
from tests.test_models.test_base_model import test_basemodel
from models.city import City
import os


class test_City(test_basemodel):
    """ Tests city model """

    def __init__(self, *args, **kwargs):
        """ Initialized the test class """
        super().__init__(*args, **kwargs)
        self.name = "City"
        self.value = City

    def test_state_id(self):
        """ Test the type of state_id """
        new = self.value()
        self.assertNotEqual(
            type(new.state_id),
            str if os.getenv('HBNB_TYPE_STORAGE') != 'db' else type(None))

    def test_name(self):
        """ Test the type of name """
        new = self.value()
        self.assertNotEqual(
            type(new.name),
            str if os.getenv('HBNB_TYPE_STORAGE') != 'db' else type(None))
