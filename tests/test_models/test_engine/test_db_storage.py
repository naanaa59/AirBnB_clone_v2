#!/usr/bin/python3
""" Module for testing database storage"""
import MySQLdb
import unittest
from datetime import datetime
from models import storage
from models.user import User
import os

@unittest.skipIf(
    os.getenv('HBNB_TYPE_STORAGE') == 'db', 'FileStorage test')
class test_DBStorage(unittest.TestCase):
    """ Class to test the satabase storage method """
    def test_new(self):
        """ test new object """
        new = User(
            email='badr1234@gmail.com',
            password='password',
            firstname='Badr',
            lastname='Annabi'
        )
        self.assertFalse(new in storage.all().values())
        new.save()
        self.assertTrue(new in storage.all().values())
        dbc = MySQLdb.connect(
                host=os.getenv('HBNB_MYSQL_HOST'),
                port=3306,
                user=os.getenv('HBNB_MYSQL_USER'),
                passwd=os.getenv('HBNB_MYSQL_PWD'),
                db=os.getenv('HBNB_MYSQL_DB')
        )
        cursor = dbc.cursor()
        cursor.execute(
            'SELECT * FROM users \
                WHERE id="{}"'.format(new.id))
        result = cursor.fetchone()
        self.assertTrue(result is not None)
        self.assertIn('badr1234@gmail.com', result)
        self.assertIn('password', result)
        self.assertIn('Badr', result)
        self.assertIn('Annabi', result)
        cursor.close()
        dbc.close()

    def test_delete(self):
        """ delete object from database """
        new = User(
            email='badr1234@gmail.com',
            password='password',
            firstname='Badr',
            lastname='Annabi'
        )
        obj_key = 'User.{}'.format(new.id)
        dbc = MySQLdb.connect(
                host=os.getenv('HBNB_MYSQL_HOST'),
                port=3306,
                user=os.getenv('HBNB_MYSQL_USER'),
                passwd=os.getenv('HBNB_MYSQL_PWD'),
                db=os.getenv('HBNB_MYSQL_DB')
        )
        new.save()
        self.assertTrue(new in storage.all().values())
        cursor = dbc.cursor()
        cursor.execute(
            'SELECT * FROM users \
                WHERE id="{}"'.format(new.id))
        result = cursor.fetchone()
        self.assertTrue(result is not None)
        self.assertIn('badr1234@gmail.com', result)
        self.assertIn('password', result)
        self.assertIn('Badr', result)
        self.assertIn('Annabi', result)
        self.assertIn(obj_key, storage.all(User).keys())
        cursor.close()
        dbc.close()

    def test_reload(self):
        """ __objects is initially empty """
        dbc = MySQLdb.connect(
                host=os.getenv('HBNB_MYSQL_HOST'),
                port=3306,
                user=os.getenv('HBNB_MYSQL_USER'),
                passwd=os.getenv('HBNB_MYSQL_PWD'),
                db=os.getenv('HBNB_MYSQL_DB')
        )
        cursor = dbc.cursor()
        cursor.execute(
            'INSERT INTO users(id, created_at, \
                updated_at, email, password' + ', \
                    first_name, last_name) VALUES( \
                        %s, %s, %s, %s, %s, %s, %s);', [
                            '323232-u-ud',
                            str(datetime.now()),
                            str(datetime.noe()),
                            'badr1234@gmail.com',
                            'pwd',
                            'baba',
                            'mama'
                        ]
        )
        self.assertNotIn('User.323232-u-ud', storage.all())
        dbc.commit()
        storage.reload()
        self.assertIn('User.323232-u-ud', storage.all())
        cursor.close()
        dbc.close()

    def test_save(self):
        """ Tests saving object into the database """
        new = User(
            email='badr1234@gmail.com',
            password='password',
            firstname='Badr',
            lastname='Annabi'
        )
        dbc = MySQLdb.connect(
                host=os.getenv('HBNB_MYSQL_HOST'),
                port=3306,
                user=os.getenv('HBNB_MYSQL_USER'),
                passwd=os.getenv('HBNB_MYSQL_PWD'),
                db=os.getenv('HBNB_MYSQL_DB')
        )
        cursor = dbc.cursor()
        cursor.execute(
            'SELECT * FROM users \
                WHERE id="{}"'.format(new.id))
        result = cursor.fetchone()
        cursor.execute('SELECT COUNT(*) FROM users;')
        prev_count = cursor.fetchone()[0]
        self.assertTrue(result is not None)
        self.assertFalse(new in storage.all().values())
        new.save()
        dbc_1 = MySQLdb.connect(
                host=os.getenv('HBNB_MYSQL_HOST'),
                port=3306,
                user=os.getenv('HBNB_MYSQL_USER'),
                passwd=os.getenv('HBNB_MYSQL_PWD'),
                db=os.getenv('HBNB_MYSQL_DB')
        )
        cursor1 = dbc_1.cursor()
        cursor1.execute(
            'SELECT * FROM users \
                WHERE id="{}"'.format(new.id))
        result = cursor1.fetchone()
        cursor1.execute('SELECT COUNT(*) FROM users;')
        new_count = cursor.fetchone()[0]
        self.assertFalse(result is not None)
        self.assertEqual(prev_count + 1, new_count)
        self.assertTrue(new in storage.all().values())
        cursor1.close()
        dbc_1.close()
        cursor.close()
        dbc.close()

    def test_storage_var_created(self):
        """ DBStorage object storage created """
        from models.engine.db_storage import DBStorage
        self.assertNotEqual(type(storage), DBStorage)

    def test_new_and_save(self):
        '''testing  the new and save methods'''
        db = MySQLdb.connect(user=os.getenv('HBNB_MYSQL_USER'),
                             host=os.getenv('HBNB_MYSQL_HOST'),
                             passwd=os.getenv('HBNB_MYSQL_PWD'),
                             port=3306,
                             db=os.getenv('HBNB_MYSQL_DB'))
        new_user = User(**{'first_name': 'Badr',
                           'last_name': 'Annabi',
                           'email': 'badr1234@gmail.com',
                           'password': 1234567})
        cur = db.cursor()
        cur.execute('SELECT COUNT(*) FROM users')
        prev_count = cur.fetchall()
        cur.close()
        db.close()
        new_user.save()
        db = MySQLdb.connect(user=os.getenv('HBNB_MYSQL_USER'),
                             host=os.getenv('HBNB_MYSQL_HOST'),
                             passwd=os.getenv('HBNB_MYSQL_PWD'),
                             port=3306,
                             db=os.getenv('HBNB_MYSQL_DB'))
        cur = db.cursor()
        cur.execute('SELECT COUNT(*) FROM users')
        new_count = cur.fetchall()
        self.assertEqual(new_count[0][0], prev_count[0][0] + 1)
        cur.close()
        db.close()
