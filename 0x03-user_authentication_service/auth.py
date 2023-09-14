#!/usr/bin/env python3
"""Hash password"""
import bcrypt
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4
from typing import (
    TypeVar,
    Union
)

from user import Base, User
U = TypeVar(User)


def _hash_password(password: str) -> bytes:
    """method that takes in a password string
    arguments and returns bytes."""
    passwrd = password.encode('utf-8')
    return bcrypt.hashpw(passwrd, bcrypt.gensalt())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """If a user already exist with the passed email,
        raise a ValueError with the message
        User <user's email> already exists.
        If not, hash the password with _hash_password,
        save the user to the database
        using self._db and return the User object.
        """
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            hashed = _hash_password(password)
            usr = self._db.add_user(email, hashed)
            return usr
        raise ValueError(f"User {email} already exists")

    def valid_login(self, email: str, password: str) -> bool:
        """validate login details"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False

        usr_password = usr.hashed_password
        passwrd = password.encode("utf-8")
        return bcrypt.checkpw(passwrd, usr_password)

    def create_session(self, email: str) -> Union[None, str]:
        """begin session"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None

        session_id = _generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> Union[None, U]:
        """user from session id"""
        if session_id is None:
            return None

        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None

        return user

    def destroy_session(self, user_id: int) -> None:
        """end session"""
        try:
            self._db.update_user(user_id, session_id=None)
        except ValueError:
            return None
        return None

    def get_reset_password_token(self, email: str) -> str:
        """reset password"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError

        reset_token = _generate_uuid()
        self._db.update_user(user.id, reset_token=reset_token)
        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """update password"""
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError()

        hashed = _hash_password(password)
        self._db.update_user(user.id, hashed_password=hashed, reset_token=None)

def _generate_uuid() -> str:
    """
    Generate a uuid and return it
    """
    return str(uuid4())
