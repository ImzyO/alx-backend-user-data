#!/usr/bin/env python3
"""
Session Authentication module
"""

from api.v1.auth.auth import Auth
from models.user import User
from uuid import uuid4


class SessionAuth(Auth):
    """SessionAuth class"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """this method creates a session ID for a user"""
        if user_id is None or type(user_id) != str:
            return None
        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """this method returns a User ID based on a Session ID"""
        if session_id is None or type(session_id) != str:
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """this method returns a User instance based on cookie value"""
        _my_session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(_my_session_id)
        return User.get(user_id)

    def destroy_session(self, request=None):
        """this method deletes the user session - logout"""
        if request is None:
            return None
        _my_session_id = self.session_cookie(request)
        if not _my_session_id:
            return False
        user_id = self.user_id_for_session_id(_my_session_id)
        if not user_id:
            return False
        del self.user_id_by_session_id[_my_session_id]
        return True
