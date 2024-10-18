#!/usr/bin/env python3
"""
Auth Module
"""

from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
import bcrypt


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        self._db = DB()

    def hash_password(self, password: str) -> bytes:
        """Hashes the password using bcrypt.

        Args:
            password (str): The plain text password to hash.

        Returns:
            bytes: The hashed password.
        """
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    def register_user(self, email: str, password: str) -> User:
        """Registers a new user with the provided email and password.

        Args:
            email (str): The user's email.
            password (str): The user's password.

        Returns:
            User: The created User object if registration is successful.

        Raises:
            ValueError: If the user already exists with the given email.
        """
        try:
            # Check if a user with the given email already exists
            self._db.find_user_by(email=email)
            # If a user is found, raise an exception
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            # Hash the password
            hashed_password = self.hash_password(password)
            # Create the user
            new_user = self._db.add_user(email, hashed_password)
            return new_user