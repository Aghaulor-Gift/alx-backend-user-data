#!/usr/bin/env python3
"""define a _hash_password method that takes in a password string arguments
and returns bytes.The returned bytes is a salted hash of the input password,
hashed with bcrypt.hashpw."""
import bcrypt
from sqlalchemy.orm.exc import NoResultFound

from db import DB
from user import User

def _hash_password(password: str) -> bytes:
        """Hashes a password using bcrypt.

        Args:
            password (str): The plain text password to hash.

        Returns:
            bytes: The salted, hashed password as bytes.
        """
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

        return hashed_password
