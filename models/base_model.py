#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class BaseModel:
    """A base class for all hbnb models"""
    # used for db storage
    id = Column(String(60), nullable=False, primary_key=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """Instantiates a new model"""
        if not kwargs:
            from models import storage
            self.id = str(uuid.uuid4())
            self.created_at = datetime.utcnow()
            self.updated_at = datetime.utcnow()
        if kwargs:
            if "id" not in kwargs:
                kwargs["id"] = str(uuid.uuid4())
            if "created_at" not in kwargs:
                kwargs["created_at"] = datetime.utcnow().isoformat()
            if "updated_at" not in kwargs:
                kwargs["updated_at"] = datetime.utcnow().isoformat()

            for key, value in kwargs.items():
                if key == 'updated_at':
                    kwargs[key] = datetime.strptime(
                        value,
                        '%Y-%m-%dT%H:%M:%S.%f')
                if key == 'created_at':
                    kwargs[key] = datetime.strptime(
                        value,
                        '%Y-%m-%dT%H:%M:%S.%f')
                if hasattr(self, key) and key != '__class__':
                    setattr(self, key, value)

            if '__class__' in kwargs:
                del kwargs['__class__']
            self.__dict__.update(kwargs)


    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        from models import storage
        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()
    def delete(self):
        """delete instance from the storage"""
        from models import storage
        storage.delete(self)

    def to_dict(self):
        """Convert instance into dict format"""
        dictionary = self.__dict__.copy()

    # Remove '_sa_instance_state' if it exists
        dictionary.pop('_sa_instance_state', None)

        dictionary.update({
            '__class__': (str(type(self)).split('.')[-1]).split('\'')[0],
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        })

        return dictionary

