#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel
from models.base_model import Base
from models.city import City
from sqlalchemy import Column, String
from sqlalchemy.orm import sessionmaker, relationship


class State(BaseModel, Base):
    """ State class """
    __tablename__ = "states"
    name = Column(String(128), nullable=False)
    cities = relationship(
        "City", cascade="all, delete-orphan", back_populates="state")

    @property
    def cities(self):
        """
        returns the list of City instances with state_id
        equals to the current State.id
        """
        Session = sessionmaker(bind=Base.metadata.bind)
        with Session() as session:
            cities = session.query(City).filter(City.state_id == self.id).all()
        return cities
