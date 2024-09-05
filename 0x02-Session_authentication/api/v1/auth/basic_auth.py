#!/usr/bin/env python3
"""
BasicAuth class
"""

from api.v1.auth.auth import Auth
import base64
import binascii
from typing import List, TypeVar
from models.user import User


class BasicAuth(Auth):
    """
    doing nothing for
    now
    """
    def extract_base64_authorization_header(self,
                                            authorization_header: str
                                            ) -> str:
        """
        this this is to convert to 64bytes
        encoded data format
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str
                                           ) -> str:
        """
        a method that is going to decode from the base64
        byte encode type
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            encode = base64_authorization_header.encode('utf-8')
            base = base64.b64decode(encode)
            return base.decode('utf-8')
        except binascii.Error:
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str
                                 ) -> (str, str):
        """
        extract the user info basic on the
        authorizationheader sent
        encoded in base64
        """
        b64auth = decoded_base64_authorization_header
        if b64auth is None:
            return (None, None)
        if (not isinstance(b64auth, str) or ":" not in b64auth):
            return (None, None)

        userValues = b64auth.split(":", 1)
        return (userValues[0], userValues[1])

    def user_object_from_credentials(self,
                                     user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """
        making user data from the authorization
        header infomation note that this is the
        baseAuth
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        try:
            users = User.search({'email': user_email})
            if not users or users == []:
                return None
            for u in users:
                if u.is_valid_password(user_pwd):
                    return u
            return None
        except Exception:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        this is an overload method , that returns the
        current loggined user/ or that retrieve the user
        instance of the request
        """
        Auth_header = self.authorization_header(request)
        if Auth_header is not None:
            token = self.extract_base64_authorization_header(Auth_header)
            if token is not None:
                decoded = self.decode_base64_authorization_header(token)
                if decoded is not None:
                    email, pword = self.extract_user_credentials(decoded)
                    if email is not None:
                        return self.user_object_from_credentials(email, pword)
        return
