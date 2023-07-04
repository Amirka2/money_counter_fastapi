from typing import List, Optional

from sqlalchemy import Column, Integer, String, Boolean, create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, Relationship

SQLALCHEMY_DATABASE_URL = "sqlite:///./db/sql_app.db"
engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )

SessionLocal = sessionmaker(autoflush=False, bind=engine)
Base = declarative_base()
Base.metadata.create_all(bind=engine)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


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
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="photos")


