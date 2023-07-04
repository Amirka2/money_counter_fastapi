from fastapi import Depends
from sqlalchemy.orm import Session

from main import SessionLocal, engine
from logic import crud
from db import models
from schemas import schemas
from fastapi import APIRouter

router = APIRouter(prefix='/photos')
models.Base.metadata.create_all(bind=engine)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=list[schemas.Photo])
def read_items(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    photos = crud.get_photos(db, skip=skip, limit=limit)
    return photos
