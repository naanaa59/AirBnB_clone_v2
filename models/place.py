#!/usr/bin/python3
""" Place Module for HBNB project """

from sqlalchemy import Column, String, Integer, Float, ForeignKey
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from os import getenv
import models
import shlex


class Place(BaseModel, Base):
    """ A place to stay """
    """
    city_id = ""
    user_id = ""
    name = ""
    description = ""
    number_rooms = 0
    number_bathrooms = 0
    max_guest = 0
    price_by_night = 0
    latitude = 0.0
    longitude = 0.0
    amenity_ids = []
    """
    __tablename__ = "places"
    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False, )
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=False)
    number_rooms = Column(Integer, default=0, nullable=False)
    number_bathrooms = Column(Integer, default=0, nullable=False)
    max_guest = Column(Integer, default=0, nullable=False)
    price_by_night = Column(Integer, default=0, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    amenity_ids = []

    if getenv("HBNB_TYPE_STORAGE") == "db":
        reviews = relationship("Review", cascade="all, delete, \
                               delete-orphan", backref="place")
        amenities = relationship("Amenity", cascade="all, delete, \
                                 delete-orphan", backref="place")
    else:
        @property
        def reviews(self):
            """ returns list of reviews.id"""
            list_rev = []
            final_list = []
            all_rev = models.storage.all()
            for key in all_rev:
                review = key.replace('.', ' ')
                review = shlex.split(review)
            for rev in all_rev:
                if (rev.place_id == self.id):
                    final_list.append(rev)
            return final_list

    @property
    def amenities(self):
        """ returns list of amenities id"""
        return self.amenity_ids

    @amenities.setter
    def amenities(self, obj=None):
        """ sets amenity ids to attribute"""
        # if type(obj) is Amenity
