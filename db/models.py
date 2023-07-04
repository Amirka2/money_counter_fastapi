from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from main import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    tg_id = Column(Integer)
    first_name = Column(String)
    last_name = Column(String)
    username = Column(String)
    hash = Column(String)

    photos = relationship("Photo", back_populates="owner")


class Photo(Base):
    __tablename__ = "photos"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    url = Column(String, unique=True)
    isDetectionCorrect = Column(Boolean)

    owner_id = relationship("User", back_populates="items")


