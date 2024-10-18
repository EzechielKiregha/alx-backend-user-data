#!/usr/bin/env python3


"""
DB Module
"""

from sqlalchemy.orm.session import Session
from user import User

class DB:
    """DB class to handle user operations in the database."""

    def __init__(self) -> None:
        """Initialize a new DB instance and setup the SQLite engine."""
        self._engine = create_engine("sqlite:///a.db", echo=True)
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
        """Adds a new user to the database and returns the User object.

        Args:
            email (str): The user's email.
            hashed_password (str): The user's hashed password.

        Returns:
            User: The created User object.
        """
        # Create a new User object
        new_user = User(email=email, hashed_password=hashed_password)

        # Add the user to the session
        self._session.add(new_user)

        # Commit the session to save the user in the database
        self._session.commit()

        # Return the created User object
        return new_user

