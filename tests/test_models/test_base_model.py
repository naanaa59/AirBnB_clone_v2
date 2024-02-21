#!/usr/bin/python3
""" Tests all edge cases for basemodel """
from models.base_model import BaseModel, Base

import unittest
from datetime import datetime
from uuid import UUID
import json
import os


class test_basemodel(unittest.TestCase):
    """ """

    def __init__(self, *args, **kwargs):
        """ """
        super().__init__(*args, **kwargs)
        self.name = 'BaseModel'
        self.value = BaseModel

    def setUp(self):
        """ makes some operations before running the test """
        pass

    def tearDown(self):
        """ removes JSON file after finishing all tests """
        try:
            os.remove('file.json')
        except Exception:
            pass

    def test_default(self):
        """ Tests the type of stored value """
        i = self.value()
        self.assertEqual(type(i), self.value)

    def test_kwargs(self):
        """ Tests kwargs with an element """
        i = self.value()
        copy = i.to_dict()
        new = BaseModel(**copy)
        self.assertFalse(new is i)

    def test_kwargs_int(self):
        """ Tests kwargs with an int """
        i = self.value()
        copy = i.to_dict()
        copy.update({1: 2})
        with self.assertRaises(TypeError):
            new = BaseModel(**copy)

    def test_save(self):
        """ Testing save """
        i = self.value()
        i.save()
        key = self.name + "." + i.id
        with open('file.json', 'r') as f:
            j = json.load(f)
            self.assertEqual(j[key], i.to_dict())

    @unittest.skipIf(
            os.getenv('HBNB_TYPE_STORAGE') == 'db', 'FileStorage test')
    def test_save(self):
        """ Tests save method """
        i = self.value()
        i.save()
        key = self.name + "." + i.id
        with open('file.json', 'r') as file:
            j = json.load(file)
            self.assertEqual(j[key], i.to_dict())

    def test_str(self):
        """ Tests the __str__ method """
        i = self.value()
        self.assertEqual(str(i), '[{}] ({}) {}'.format(self.name, i.id,
                         i.__dict__))

    def test_todict(self):
        """ Tests to_dict method """
        i = self.value()
        n = i.to_dict()
        self.assertEqual(i.to_dict(), n)
        # Testing if it's a dictionary
        self.assertIsInstance(self.value().to_dict(), dict)
        # Testing if to_dict contains accurate keys
        self.assertIn('id', self.value().to_dict())
        self.assertIn('created_at', self.value().to_dict())
        self.assertIn('updated_at', self.value().to_dict())
        # Testing if to_dict contains added attributes
        new_attr = self.value()
        new_attr.firstname = 'Badr'
        new_attr.lastname = 'Annabi'
        self.assertIn('firstname', new_attr.to_dict())
        self.assertIn('lastname', new_attr.to_dict())
        self.assertIn('firstname', self.value(firstname='Badr').to_dict())
        self.assertIn('lastname', self.value(lastname='Annabi').to_dict())
        # Testing to_dict datetime if they are strings
        self.assertIsInstance(self.value().to_dict()['created_at'], str)
        self.assertIsInstance(self.value().to_dict()['updated_at'], str)
        # Testing to_dict output
        datetime_now = datetime.today()
        model = self.value()
        model.id = '012345'
        model.created_at = model.updated_at = datetime_now
        to_dict = {
            'id': '012345',
            '__class__': model.__class__.__name__,
            'created_at': datetime_now.isoformat(),
            'updated_at': datetime_now.isoformat()
        }
        self.assertDictEqual(model.to_dict(), to_dict)

        # if os.getenv('HBNB_TYPE_STORAGE') != 'db':
        #     # self.assertDictEqual(
        #     #     self.value(id='Oum12', age=24).to_dict(),
        #     #     {
        #     #         '__class__': model.__class__.__name__,
        #     #         'id': 'Oum12',
        #     #         'age': 24
        #     #     }
        #     # )
        #     self.assertDictEqual(
        #         self.value(id='Oum123', age=None).to_dict(),
        #         {
        #             '__class__': model.__class__.__name__,
        #             'id': 'Oum123',
        #             'age': None
        #         }
        #     )
        # Testing to_dict output contradiction
        model_2 = self.value()
        self.assertIn('__class__', self.value().to_dict())
        self.assertNotIn('__class__', self.value().__dict__)
        self.assertNotEqual(model_2.to_dict(), model_2.__dict__)
        self.assertNotEqual(
            model_2.to_dict()['__class__'],
            model_2.__class__
        )
        # Testing to_dict with args
        with self.assertRaises(TypeError):
            self.value().to_dict(None)
        with self.assertRaises(TypeError):
            self.value().to_dict(self.value())
        with self.assertRaises(TypeError):
            self.value().to_dict(45)
        self.assertNotIn('_sa_instance_state', n)

    def test_kwargs_none(self):
        """ Tests empty kwargs """
        n = {None: None}
        with self.assertRaises(TypeError):
            new = self.value(**n)

    def test_kwargs_one(self):
        """ Tests kwargs with one key-value """
        n = {'Name': 'test'}
        new = self.value(**n)
        self.assertTrue(hasattr(new, 'Name'))

    def test_id(self):
        """ Tests the type of id """
        new = self.value()
        self.assertEqual(type(new.id), str)

    def test_created_at(self):
        """ Tests the type of created_at """
        new = self.value()
        self.assertEqual(type(new.created_at), datetime)

    def test_updated_at(self):
        """ Tests the type of updated_at """
        new = self.value()
        self.assertEqual(type(new.updated_at), datetime)
        n = new.to_dict()
        new = BaseModel(**n)
        self.assertTrue(new.created_at == new.updated_at)

    @unittest.skipIf(
        os.getenv('HBNB_TYPE_STORAGE') == 'id', 'FileStorage test')
    def test_delete(self):
        """ Tests the delete method """
        from models import storage
        i = self.value()
        i.save()
        self.assertTrue(i in storage.all().values())
        i.delete()
        self.assertFalse(i in storage.all().values())
