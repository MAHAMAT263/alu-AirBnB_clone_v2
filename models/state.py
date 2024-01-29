#!/usr/bin/python3
""" State Module for HBNB project """
import models
from models.base_model import BaseModel
from models.city import City
from models.base_model import Base
from os import getenv
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'

    name = Column(String(128), nullable=False)
    cities = relationship("city", back_populates="state", cascade="all, delete-orphan")
    if getenv("HBNB_TYPE_STORAGE") != "db":
    @property
    def cities(self):
        """Getter attribute for cities"""
        city_list = []
        for city in list(models.storage.all(city).value()):
            if city.state_id == self.id:
                city_list.append(city)
        return city_list
