#!/usr/bin/env python3
"""sql model User for database users

   -attributes:
       id : Integer Primary key
       email: non-nullable string
       hashed_password: non-nullable string
       session_id: a nullable string
       reset_token: nullable string
"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from typing import Optional

Base = declarative_base()


class User(Base):
    __tablename__: str = 'users'

    id: Column = Column(Integer, primary_key=True)
    email: Column = Column(String, nullable=False)
    hashed_password: Column = Column(String, nullable=False)
    session_id: Column(String, nullable=True)
    reset_token: Column = Column(String, nullable=True)
