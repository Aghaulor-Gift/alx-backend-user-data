#!/usr/bin/env python3
"""DB module
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Add a user to the database.

        Args:
            email (str): The user's email.
            hashed_password (str): The user's hashed password.

        Returns:
            User: The created user object.
        """
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()

        return new_user

    def find_user_by(self, **kwargs) -> User:
        """Find a user by given keyword arguments.

        Args:
            **kwargs: Arbitrary keyword arguments to filter users.

        Returns:
            User: The first user that matches the filter criteria.

        Raises:
            NoResultFound: If no user matches the filter criteria.
            InvalidRequestError: If invalid arguments are passed.
        """
        try:
            user = self._session.query(User).filter_by(**kwargs).first()
            if user is None:
                raise NoResultFound("No user matches the given criteria.")
        except Exception as e:
            if isinstance(e, InvalidRequestError):
                raise InvalidRequestError("Invalid request arguments.")
            raise e
        return user
