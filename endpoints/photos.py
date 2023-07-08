from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.models import get_db
from schemas import schemas
from logic import crud


photos_router = APIRouter(prefix='/photos', tags=['Photos'])


@photos_router.get("/{user_id}/", response_model=list[schemas.Photo])
def read_photos(user_id: int, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    photos = crud.get_photos(db, user_id, skip=skip, limit=limit)
    return photos


@photos_router.get("/{user_id}/favorite", response_model=list[schemas.Photo])
def read_photos(user_id: int, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    fav_photos = crud.get_favorite_photos(db, user_id, skip=skip, limit=limit)
    return fav_photos

