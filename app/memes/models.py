from sqlalchemy import Column, ForeignKey, String

from app.core.db import Base


class Meme(Base):
    __tablename__ = 'memes'

    url = Column(String, nullable=False)
    desc = Column(String, nullable=True)
    author = Column(ForeignKey('users.id'))
