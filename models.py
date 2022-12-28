from __future__ import annotations
from datetime import datetime

from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from flask_login import UserMixin


class User(UserMixin, Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(120), unique=True, nullable=False)
    firstname = Column(String(50), nullable=False)
    lastname = Column(String(50), nullable=False)
    password = Column(String(100), nullable=False)
    created = Column(Date, default=datetime.utcnow)
    updated = Column(Date, default=datetime.utcnow)
    urlss = relationship('Urls', backref='users')

    def __init__(self, email=None, firstname=None, lastname=None, password=None):
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.password = password

    def __repr__(self):
        return f'<User {self.email, self.firstname, self.lastname, self.password!r}>'


class Urls(Base):
    __tablename__ = 'urls'

    id = Column(Integer, primary_key=True)
    created = Column(Date, default=datetime.utcnow)
    original_url = Column(String(255), nullable=False)
    clicks = Column(Integer)
    user_id = Column(Integer, ForeignKey('users.id'))

    def __init__(self, original_url=None, clicks=0, user_id=user_id):
        self.original_url = original_url
        self.clicks = clicks
        self.user_id = user_id

    def __repr__(self):
        return f'<Urls {self.id, self.original_url, self.clicks, self.created!r}>'
