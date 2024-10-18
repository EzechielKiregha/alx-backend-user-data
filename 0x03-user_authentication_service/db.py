#!/usr/bin/env python3

"""
DB Module
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from user import Base, User


class DB:
    """DB class to handle user operations in the database."""

    def __init__(self) -> None:
        """Initialize a new DB instance and setup the SQLite engine."""
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object to interact with the database."""
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Adds a new user to the database and returns the User object."""
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """Find a user in the database by arbitrary keyword arguments."""
        try:
            user = self._session.query(User).filter_by(**kwargs).one()
        except NoResultFound:
            raise NoResultFound("No user found with the provided filters")
        except InvalidRequestError:
            raise InvalidRequestError("Invalid query parameters")
        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """Update a user's attributes based on keyword arguments and
        commit the changes.

        Args:
            user_id (int): The user's ID.
            kwargs: The attributes to update with new values.

        Raises:
            ValueError: If an invalid attribute is passed.
        """
        user = self.find_user_by(id=user_id)

        for key, value in kwargs.items():
            if not hasattr(user, key):
                raise ValueError(f"'{key}' is not a valid attribute of User")
            setattr(user, key, value)

        self._session.commit()
