#!/usr/bin/env python3
"""Encrypting passwords"""
import bcrypt
from bcrypt import hashpw


def hash_password(password: str) -> bytes:
    """function that expects one string argument name password and
    returns a salted, hashed password, which is a byte string."""
    b = password.encode()
    hashed = hashpw(b, bcrypt.gensalt())
    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    """function that expects 2 arguments and returns a boolean.
    Use bcrypt to validate that the provided
    password matches the hashed password."""
    return bcrypt.checkpw(password.encode(), hashed_password)
