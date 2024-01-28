#!/usr/bin/python3
""" City Module for HBNB project """
from models.base_model import BaseModel
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from models.state import State

class City(BaseModel):
    """ the city class contains state ID and name """
    __tablename__ = 'cities'
    state_id = Column(string(60), nullable=False,ForeignKey('states.id'))
    name = Column(string(128), nullable=False)

    state = relationship("State", back_populates="cities")
