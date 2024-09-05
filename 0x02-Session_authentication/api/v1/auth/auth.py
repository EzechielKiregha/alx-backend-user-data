#!/usr/bin/env python3
"""
a class that will manage api
authentication
"""


from flask import request
from typing import List, TypeVar
from models.user import User
import os


class Auth:
    """
    this is an auth class
    """
    # def require_auth(self,
    #                  path: str,
    #                  excluded_paths: List[str]
    #                  ) -> bool:
    #     """
    #     requires auth
    #     """
    #     if path is None:
    #         return True

    #     if excluded_paths is None or len(excluded_paths) == 0:
    #         return True

    #     if path[-1] != "/":
    #         path = path + "/"
    #     for patterns in excluded_paths:
    #         if path[-1] == "*":
    #             if patterns.startswith(path[0:-1]):
    #                 return False
    #         if path == patterns:
    #             return False
    #     return True
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ require auth function that returns false"""
        if excluded_paths and path:
            if path[-1] == '/':
                new_path = path[:-1]
            else:
                new_path = path
            new_excluded_path = []
            for element in excluded_paths:
                if element[-1] == '/':
                    new_excluded_path.append(element[:-1])
                if element[-1] == '*':
                    if new_path.startswith(element[:-1]):
                        return False

            if new_path not in new_excluded_path:
                return True
            else:
                return False
        if path is None:
            return True
        if not excluded_paths:
            return True

    def authorization_header(self, request=None) -> str:
        """
        dealing with the authorization header
        """
        if request is None:
            return None
        authorization = request.headers.get("Authorization")
        if authorization is None:
            return None
        return authorization

    def current_user(self, request=None) -> TypeVar('User'):
        """
        this returns the current loggin
        user
        """
        return None

    def session_cookie(self, request=None):
        """
        a method that returns a cookies values from
        the request
        """
        # if request is None:
        #     return None
        # _my_session_id = os.getenv("SESSION_NAME")
        # if _my_session_id is not None:
        #     return request.cookies.get(_my_session_id)
        # return None
        if request is not None:
            cookie_name = os.getenv('SESSION_NAME')
            return request.cookies.get(cookie_name)
