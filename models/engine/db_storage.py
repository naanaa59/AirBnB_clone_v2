#!/usr/bin/python3
""" This script defines nes engine DBStorage"""
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from models.base_model import Base
from models.user import User
from models.place import Place
from models.city import City
from models.state import State
from models.review import Review
from models.amenity import Amenity


import os


class DBStorage:
    """ Class DBStorage that store all data in a sql database"""
    __engine = None
    __session = None

    def __init__(self):
        db_user = os.getenv('HBNB_MYSQL_USER')
        db_pwd = os.getenv('HBNB_MYSQL_PWD')
        db_hst = os.getenv('HBNB_MYSQL_HOST')
        db_name = os.getenv('HBNB_MYSQL_DB')
        env = os.getenv('HBNB_ENV')
        db_url = f"mysql+mysqldb://{db_user}:{db_pwd}@{db_hst}:3306/{db_name}"
        self.__engine = create_engine(db_url, pool_pre_ping=True)

        if env == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """ query on the current database session all objects
            depending on the class name
        """
        all_classes = ['User', 'State', 'City', 'Place', 'Amenity', 'Review']

        dictionary = {}

        if cls is not None:
            objs = self.__session.query(cls)
        else:
            objs = []
            for clas in all_classes:
                objs = self.__session.query(eval(clas))
        for obj in objs:
            key = f"{type(obj).__name__}.{obj.id}"
            try:
                del (obj._sa_instance_state)
            except KeyError:
                pass
            dictionary[key] = obj
        return dictionary

    def new(self, obj):
        """ add a new obj to the current database"""
        self.__session.add(obj)

    def save(self):
        """ commit all changes of the current database"""
        self.__session.commit()

    def delete(self, obj=None):
        """ delete from the current database session"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(
            bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """Call remove() method on the private session or close() on Session"""
        self.__session.close()
