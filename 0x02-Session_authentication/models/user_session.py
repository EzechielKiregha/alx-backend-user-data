#!/usr/bin/env python3
"""
a class that manages the user
sessions
"""


from models.base import Base


class UserSession(Base):
    """
    UserSession class
    """
    def __init__(self, *args: list, **kwargs: dict):
        """
        the init method for the session
        like for user but has only two attributes
        """
        self.user_id = kwargs.get("user_id")
        self.session_id = kwargs.get("session_id")
