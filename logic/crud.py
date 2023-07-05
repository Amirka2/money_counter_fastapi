from fastapi import HTTPException
from sqlalchemy.orm import Session

from db import models
from schemas import schemas


photos_directory = "./photos/"


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def change_tokens_value(db: Session, user: schemas.User):
    user_db = db.query(models.User).filter(models.User.id == user.id).first()
    if not user_db:
        raise HTTPException(status_code=404, detail="User not found")
    user_db = models.User(**user.dict())
    db.add(user_db)
    db.commit()
    db.refresh(user_db)
    return user_db


def get_photos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Photo).offset(skip).limit(limit).all()


def create_user_photo(db: Session, photo: schemas.PhotoCreate, user_id: int):
    db_item = models.Photo(**photo.dict(), owner_id=user_id, url=photos_directory+photo.name)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
