#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.city import City

class State(BaseModel):
    """ State class """
    __tablename__ = 'states'

    name = Column(string(128), nullable=False)
    cities = relationship("city", back_populates="state", cascade="all, delete-orphan")

    @property
    def cities(self):
        """Getter attribute for cities"""
        from models import storage
        city_list = []
        for city_id, city in storage.all(City).items():
            if city.state_id == self.id:
                city_list.append(city)
        return city_list
