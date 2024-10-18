#!/usr/bin/env python3

"""
Auth Module
"""

import bcrypt


def _hash_password(password: str) -> bytes:
    """Hashes a password using bcrypt with a salt and returns
    the hashed bytes.

    Args:
        password (str): The password string to hash.

    Returns:
        bytes: The hashed password.
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password
