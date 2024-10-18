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

Base = declarative_base()

class User(Base):
    """
    SQLAlchemy model representing the 'users' table.

    Attributes:
        id (int): The primary key for the user.
        email (str): The user's email address (max 250 chars,
        non-nullable).
        hashed_password (str): The user's hashed password (max 250 chars,
        non-nullable).
        session_id (str): A session ID for tracking user sessions
        (nullable, max 250 chars).
        reset_token (str): A token for password reset functionality
        (nullable, max 250 chars).
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)

