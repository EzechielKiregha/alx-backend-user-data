#!/usr/bin/env python3
"""
a session class that keeps the session
in a db/file for future user
"""


from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """SessionDBAuth class"""

    def create_session(self, user_id=None):
        """
        creating a new instamce of user_session
        """
        user_session_id = super().create_session(user_id)
        if user_session_id is None:
            return None
        user_session_info = {
            "user_id": user_id,
            "session_id": user_session_id
        }
        user_session = UserSession(**user_session_info)
        user_session.save()
        user_session.save_to_file()
        return user_session_id

    # def user_id_for_session_id(self, session_id=None):
    #     """
    #     Returns a user ID based on a session ID
    #     Args:
    #         session_id (str): session ID
    #     Return:
    #         user id or None if session_id is None or not a string
    #     """
    #     user_id = UserSession.search({"session_id": session_id})
    #     if user_id:
    #         return user_id
    #     return None

    # def destroy_session(self, request=None):
    #     """
    #     Destroy a UserSession instance based on a
    #     Session ID from a request cookie
    #     """
    #     if request is None:
    #         return False
    #     session_id = self.session_cookie(request)
    #     if not session_id:
    #         return False
    #     user_session = UserSession.search({"session_id": session_id})
    #     if user_session:
    #         user_session[0].remove()
    #         return True
    #     return False
    def user_id_for_session_id(self, session_id=None):
        """Retrieves the user id of the user associated with
        a given session id.
        """
        try:
            sessions = UserSession.search({'session_id': session_id})
        except Exception:
            return None
        if len(sessions) <= 0:
            return None
        cur_time = datetime.now()
        time_span = timedelta(seconds=self.session_duration)
        exp_time = sessions[0].created_at + time_span
        if exp_time < cur_time:
            return None
        return sessions[0].user_id

    def destroy_session(self, request=None) -> bool:
        """Destroys an authenticated session.
        """
        session_id = self.session_cookie(request)
        try:
            sessions = UserSession.search({'session_id': session_id})
        except Exception:
            return False
        if len(sessions) <= 0:
            return False
        sessions[0].remove()
        return True
