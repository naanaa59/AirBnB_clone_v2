""" Tests for console (command interpreter) """
import json
import MySQLdb
import sqlalchemy
import os
import unittest
from io import StringIO
from unittest.mock import patch
from console import HBNBCommand
from models import storage
from models.base_model import BaseModel
from models.user import User
from tests import clear_stream


class TestHBNBCommand(unittest.TestCase):
    """ Tests class for the HBNBCommand class """
    @unittest.skipIf(
        os.getenv('HBNB_TYPE_STORAGE') == 'db', 'FileStorage test')
    def test_fs_create(self):
        """Tests the create command for file storage """
        with patch('sys.stdout', new=StringIO()) as cout:
            cons = HBNBCommand()
            cons.onecmd('create City name="Texas"')
            model_id = cout.getvalue().strip()
            clear_stream(cout)
            self.assertIn('City.{}'.format(model_id), storage.all().keys())
            cons.onecmd('show City {}'.format(model_id))
            self.assertIn("'name': 'Texas'", cout.getvalue().strip())
            clear_stream(cout)
            cons.onecmd('create User name="James" age=17 height=5.9')
            model_id = cout.getvalue().strip()
            self.assertIn('User.{}'.format(model_id), storage.all().keys())
            clear_stream(cout)
            cons.onecmd('show User {}'.format(model_id))
            self.assertIn("'name': 'James'", cout.getvalue().strip())
            self.assertIn("'age': '17'", cout.getvalue().strip())
            self.assertIn("'height': '5.9'", cout.getvalue().strip())

    @unittest.skipIf(
        os.getenv('HBNB_TYPE_STORAGE') != 'db', 'DBStorage test')
    def test_db_create(self):
        """Tests the create command with the database storage"""
        with patch('sys.stdout', new=StringIO()) as cout:
            cons = HBNBCommand()
            # creating a model
            with self.assertRaises(sqlalchemy.exc.OperationalError):
                cons.onecmd('create User')
            # creating User instance
            clear_stream(cout)
            cons.onecmd('create User email="john25@gmail.com" password="123"')
            model_id = cout.getvalue().strip()
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
                    WHERE id="{}"'.format(model_id))
            result = cursor.fetchone()
            self.assertTrue(result is not None)
            self.assertIn('john25@gmail.com', result)
            self.assertIn('123', result)
            cursor.close()
            dbc.close()

    @unittest.skipIf(
        os.getenv('HBNB_TYPE_STORAGE') != 'db', 'DBStorage test')
    def test_db_show(self):
        """Tests the show command with the database storage"""
        with patch('sys.stdout', new=StringIO()) as cout:
            cons = HBNBCommand()
            # showing User instance
            obj = User(email="john25@gmail.com", password="123")
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
                    WHERE id="{}"'.format(obj.id))
            result = cursor.fetchone()
            self.assertTrue(result is not None)
            self.assertIn('show User {}'.format(obj.id))
            self.assertEqual(
                    cout.getvalue().strip(),
                    '** no instance found **'
            )
            obj.save()
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
                    WHERE id="{}"'.format(obj.id))
            clear_stream(cout)
            cons.onecmd('show User {}'.format(obj.id))
            result = cursor.fetchone()
            self.assertTrue(result is not None)
            self.assertIn('john25@gmail.com', result)
            self.assertIn('123', result)
            self.assertIn('john25@gmail.com', cout.getvalue())
            self.assertIn('123', cout.getvalue())
            cursor.close()
            obj.close()

    @unittest.skipIf(
        os.getenv('HBNB_TYPE_STORAGE') != 'db', 'DBStorage test')
    def test_db_count(self):
        """Tests the count command for database storage."""
        with patch('sys.stdout', new=StringIO()) as cout:
            cons = HBNBCommand()
            dbc = MySQLdb.connect(
                host=os.getenv('HBNB_MYSQL_HOST'),
                port=3306,
                user=os.getenv('HBNB_MYSQL_USER'),
                passwd=os.getenv('HBNB_MYSQL_PWD'),
                db=os.getenv('HBNB_MYSQL_DB')
            )
            cursor = dbc.cursor()
            cursor.execute('SELECT COUNT(*) FROM states;')
            res = cursor.fetchone()
            count = int(res[0])
            cons.onecmd('create State name="California"')
            clear_stream(cout)
            cons.onecmd('count State')
            i = cout.getvalue().strip()
            self.assertEqual(int(i), count + 1)
            clear_stream(cout)
            cons.onecmd('count State')
            cursor.close()
            dbc.close()
