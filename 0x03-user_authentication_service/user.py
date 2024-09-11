#!/usr/bin/env python3
"""A module that create a SQLAlchemy model named User for a database table
named users (by using the mapping declaration of SQLAlchemy).
"""
from sqlalchemy import Integer, Column, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    """A class user that records user information
    """
    __tablename__ = 'User'

    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)

    def __repr__(self):
        return "<User(name='%s', fullname='%s', nickname='%s')>" % (
                      self.name, self.fullname, self.nickname)
