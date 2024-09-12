#!/usr/bin/env python3
"""Main code"""
import requests

BASE_URL = "http://localhost:5000"


def register_user(email: str, password: str) -> None:
    """Register a new user."""
    response = requests.post(f"{BASE_URL}/users", data={"email": email,
                                                        "password": password})
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "user created"}


def log_in_wrong_password(email: str, password: str) -> None:
    """Attempt to log in with the wrong password."""
    response = requests.post(f"{BASE_URL}/sessions",
                             data={"email": email, "password": password})
    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    """Log in and return the session ID."""
    response = requests.post(f"{BASE_URL}/sessions",
                             data={"email": email, "password": password})
    assert response.status_code == 200
    assert "session_id" in response.cookies
    assert response.json() == {"email": email, "message": "logged in"}
    return response.cookies["session_id"]


def profile_unlogged() -> None:
    """Try to access the profile without logging in."""
    response = requests.get(f"{BASE_URL}/profile")
    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    """Access the profile while logged in."""
    response = requests.get(f"{BASE_URL}/profile", cookies={"session_id":
                                                            session_id})
    assert response.status_code == 200
    assert response.json() == {"email": EMAIL}


def log_out(session_id: str) -> None:
    """Log out by deleting the session."""
    response = requests.delete(f"{BASE_URL}/sessions", cookies={"session_id":
                                                                session_id})
    assert response.status_code == 302
    assert response.url == f"{BASE_URL}/"


def reset_password_token(email: str) -> str:
    """Request a password reset token."""
    response = requests.post(f"{BASE_URL}/reset_password", data={"email":
                                                                 email})
    assert response.status_code == 200
    assert "reset_token" in response.json()
    return response.json()["reset_token"]


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Update the password using the reset token."""
    response = requests.put(f"{BASE_URL}/reset_password",
                            data={"email": email, "reset_token": reset_token,
                                  "new_password": new_password})
    assert response.status_code == 200


# Constants
EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
