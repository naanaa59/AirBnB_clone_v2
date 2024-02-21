#!/usr/bin/python3
""" Tests Place model """
from tests.test_models.test_base_model import test_basemodel
from models.place import Place
import os


class test_Place(test_basemodel):
    """ Tests Place model"""

    def __init__(self, *args, **kwargs):
        """ Initialized the tests for the Place model"""
        super().__init__(*args, **kwargs)
        self.name = "Place"
        self.value = Place

    def test_city_id(self):
        """ Tests the type of city_id """
        new = self.value()
        self.assertNotEqual(
            type(new.city_id),
            str if os.getenv('HBNB_TYPE_STORAGE') != 'db' else type(None))

    def test_user_id(self):
        """ Tests the type of user_id """
        new = self.value()
        self.assertNotEqual(
            type(new.user_id),
            str if os.getenv('HBNB_TYPE_STORAGE') != 'db' else type(None))

    def test_name(self):
        """ Tests the type of name """
        new = self.value()
        self.assertNotEqual(
            type(new.name),
            str if os.getenv('HBNB_TYPE_STORAGE') != 'db' else type(None))

    def test_description(self):
        """ Tests the type of desc """
        new = self.value()
        self.assertNotEqual(
            type(new.description),
            str if os.getenv('HBNB_TYPE_STORAGE') != 'db' else type(None))

    def test_number_rooms(self):
        """ Tests the type of number of rooms """
        new = self.value()
        self.assertNotEqual(
            type(new.number_rooms),
            int if os.getenv('HBNB_TYPE_STORAGE') != 'db' else type(None))

    def test_number_bathrooms(self):
        """ Tests the type of number of bathrooms """
        new = self.value()
        self.assertNotEqual(
            type(new.number_bathrooms),
            int if os.getenv('HBNB_TYPE_STORAGE') != 'db' else type(None))

    def test_max_guest(self):
        """ Tests the type of max_guest """
        new = self.value()
        self.assertNotEqual(
            type(new.max_guest),
            int if os.getenv('HBNB_TYPE_STORAGE') != 'db' else type(None))

    def test_price_by_night(self):
        """ Tests the type of price by night """
        new = self.value()
        self.assertNotEqual(
            type(new.price_by_night),
            int if os.getenv('HBNB_TYPE_STORAGE') != 'db' else type(None))

    def test_latitude(self):
        """ Tests the type of latitude """
        new = self.value()
        self.assertNotEqual(
            type(new.latitude),
            float if os.getenv('HBNB_TYPE_STORAGE') != 'db' else type(None))

    def test_longitude(self):
        """ Tests the type of longitude """
        new = self.value()
        self.assertNotEqual(
            type(new.longitude),
            float if os.getenv('HBNB_TYPE_STORAGE') != 'db' else type(None))

    def test_amenity_ids(self):
        """ Tests the type of amenity_ids """
        new = self.value()
        self.assertNotEqual(
            type(new.amenity_ids),
            float if os.getenv('HBNB_TYPE_STORAGE') != 'db' else type(None))
