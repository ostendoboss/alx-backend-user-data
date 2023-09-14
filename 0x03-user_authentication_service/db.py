#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError

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
        """returns a User object. The method
        should save the user to the database"""
        new = User(email=email, hashed_password=hashed_password)
        self._session.add(new)
        self._session.commit()
        return new

    def find_user_by(self, **kwargs) -> User:
        """implement the DB.find_user_by method.
        This method takes in arbitrary keyword arguments
        and returns the first row found in the users
        table as filtered by the method’s input arguments"""
        every_user = self._session.query(User)
        for k, v in kwargs.items():
            if k not in User.__dict__:
                raise InvalidRequestError
            for usr in every_user:
                if getattr(usr, k) == v:
                    return usr
        raise NoResultFound

    def update_user(self, user_id: int, **kwargs) -> None:
        """The method will use find_user_by to locate
        the user to update, then will update the user’s attributes
        """
        try:
            usr = self.find_user_by(id=user_id)
        except NoResultFound:
            raise ValueError()
        for k, v in kwargs.items():
            if hasattr(usr, k):
                setattr(usr, k, v)
            else:
                raise ValueError
        self._session.commit()
