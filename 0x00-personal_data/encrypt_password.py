#!/usr/bin/env python3
"""
this is a function that
will be hashing  the password
"""


import bcrypt


def hash_password(password: str) -> bytes:
    """
    hashes a password using bcrypt
    """
    password = password.encode()
    hash_passwd = bcrypt.hashpw(password, bcrypt.gensalt(12))
    return hash_passwd


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    this checks the validity of a password if
    they match with the crypted value
    """
    password = password.encode()
    flag = bcrypt.checkpw(password, hashed_password)
    return flag
