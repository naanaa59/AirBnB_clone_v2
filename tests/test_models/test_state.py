#!/usr/bin/python3
""" Testing State class"""
import os

from tests.test_models.test_base_model import test_basemodel
from models.state import State


class test_state(test_basemodel):
    """ Tests for State model """

    def __init__(self, *args, **kwargs):
        """ Initializes the test class """
        super().__init__(*args, **kwargs)
        self.name = "State"
        self.value = State

    def test_name3(self):
        """ Tests the type of name """
        new = self.value()
        self.assertNotEqual(
            type(new.name),
            str if os.getenv('HBNB_TYPE_STORAGE') != 'db' else type(None)
        )
