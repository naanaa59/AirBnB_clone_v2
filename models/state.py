#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel
from models.base_model import Base
from models.city import City
from sqlalchemy import Column, String
from sqlalchemy.orm import sessionmaker, relationship
import os


class State(BaseModel, Base):
    """ State class """
    __tablename__ = "states"
    name = Column(String(128), nullable=False)
    cities = relationship(
        "City", cascade="all, delete-orphan", backref="state")

    if not os.getenv('HBNB_TYPE_STORAGE') == "db":
        @property
        def cities(self):
            from models import storage
            cities_list = [city for _, city in storage.all(City).items()
                           if city.state_id == self.id]
            return cities_list
