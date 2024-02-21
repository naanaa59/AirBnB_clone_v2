#!/usr/bin/python3
""" Tests the User model """
from tests.test_models.test_base_model import test_basemodel
from models.user import User
import os


class test_User(test_basemodel):
    """ Test the user model """

    def __init__(self, *args, **kwargs):
        """ Initialized the test for User model """
        super().__init__(*args, **kwargs)
        self.name = "User"
        self.value = User

    def test_first_name(self):
        """ Test the type of firstname """
        new = self.value()
        self.assertNotEqual(
            type(new.first_name),
            str if os.getenv('HBNB_TYPE_STORAGE') != 'db' else type(None))

    def test_last_name(self):
        """ Test the type of lastname """
        new = self.value()
        self.assertNotEqual(
            type(new.last_name),
            str if os.getenv('HBNB_TYPE_STORAGE') != 'db' else type(None))

    def test_email(self):
        """ Test the type of email """
        new = self.value()
        self.assertNotEqual(
            type(new.email),
            str if os.getenv('HBNB_TYPE_STORAGE') != 'db' else type(None))

    def test_password(self):
        """ Test the type of password """
        new = self.value()
        self.assertNotEqual(
            type(new.password),
            str if os.getenv('HBNB_TYPE_STORAGE') != 'db' else type(None))
