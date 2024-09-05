#!/usr/bin/env python3
"""
a class that implement the expiration
session id after a period of time
"""


from api.v1.auth.session_auth import SessionAuth
import os
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """
    session expiration functionalities
    """
    def __init__(self):
        """
        initialization
        """
        super().__init__()
        try:
            self.session_duration = int(os.getenv('SESSION_DURATION', '0'))
        except Exception:
            self.session_duration = 0

    # def create_session(self, user_id=None):
    #     """
    #     creating a session id , overloaded method
    #     """
    #     session_id = super().create_session(user_id)
    #     if session_id is None:
    #         return None
    #     self.user_id_by_session_id[session_id] = {
    #         'user_id': user_id,
    #         'created_at': datetime.now(),
    #     }
    #     return session_id

    # def user_id_for_session_id(self, session_id=None):
    #     """
    #     retrieving user id basing on the session
    #     id this method is overload
    #     """
    #     if session_id is None:
    #         return None
    #     if session_id not in self.user_id_by_session_id.keys():
    #         return None
    #     user_session_info = self.user_id_by_session_id.get(session_id)
    #     if self.session_duration <= 0:
    #         return user_session_info['user_id']
    #     if "created_at" not in user_session_info:
    #         now = datetime.now()
    #         # the duration into seconds
    #         time_span = timedelta(seconds=self.session_duration)
    #         exp_time = user_session_info['created_at'] + time_span
    #         if exp_time < now:
    #             return None
    #         return user_session_info['user_id']
    #     return None
    def create_session(self, user_id=None):
        """Creates a session id for the user.
        """
        session_id = super().create_session(user_id)
        if type(session_id) != str:
            return None
        self.user_id_by_session_id[session_id] = {
            'user_id': user_id,
            'created_at': datetime.now(),
            }
        return session_id

    def user_id_for_session_id(self, session_id=None) -> str:
        """Retrieves the user id of the user associated with
        a given session id.
        """
        if session_id in self.user_id_by_session_id:
            session_dict = self.user_id_by_session_id[session_id]
            if self.session_duration <= 0:
                return session_dict['user_id']
            if 'created_at' not in session_dict:
                return None
            cur_time = datetime.now()
            time_span = timedelta(seconds=self.session_duration)
            exp_time = session_dict['created_at'] + time_span
            if exp_time < cur_time:
                return None
            return session_dict['user_id']
