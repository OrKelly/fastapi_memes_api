from sqlalchemy import Column, String

from app.core.db import Base


class User(Base):
    __tablename__ = 'users'

    login = Column(String, nullable=False)
    password = Column(String, nullable=False)
