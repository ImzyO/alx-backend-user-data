#!/usr/bin/env python3
"""
This module contains functions for handling user passwords
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """this function takes a str argument and encodes it returing a
    hashed password which is a byte string"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """this function checks wether provided password matches the
    hashed password
    Returns:
        True if valid(matches) or False if not matching
    """
    is_valid = False
    if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
        is_valid = True
    return is_valid
