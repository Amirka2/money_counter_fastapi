from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.models import get_db
from schemas import schemas
from logic import crud


photos_router = APIRouter(prefix='/photos', tags=['Photos'])


@photos_router.get("/", response_model=list[schemas.Photo])
def read_photos(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    photos = crud.get_photos(db, skip=skip, limit=limit)
    return photos
