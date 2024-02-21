#!/usr/bin/python3
""" Tests the Review model """
from tests.test_models.test_base_model import test_basemodel
from models.review import Review
import os


class test_review(test_basemodel):
    """ Tests the Review model """

    def __init__(self, *args, **kwargs):
        """ Initialized the tests for  the Amenity model"""
        super().__init__(*args, **kwargs)
        self.name = "Review"
        self.value = Review

    def test_place_id(self):
        """ Tests the type of place_id """
        new = self.value()
        self.assertNotEqual(
            type(new.place_id),
            str if os.getenv('HBNB_TYPE_STORAGE') != 'db' else type(None))

    def test_user_id(self):
        """ Tests the user_id"""
        new = self.value()
        self.assertNotEqual(
            type(new.user_id),
            str if os.getenv('HBNB_TYPE_STORAGE') != 'db' else type(None))

    def test_text(self):
        """ Tests the type of text """
        new = self.value()
        self.assertNotEqual(
            type(new.text),
            str if os.getenv('HBNB_TYPE_STORAGE') != 'db' else type(None))
