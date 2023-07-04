# from sqlalchemy.orm import Session
# from fastapi import APIRouter, Depends
#
# from db.sessions import get_db
# from main import engine
# from logic import crud
# from db import models
# from schemas import schemas
#
# router = APIRouter(prefix='/photos')
# models.Base.metadata.create_all(bind=engine)
#
#
# @router.get("/", response_model=list[schemas.Photo])
# def read_items(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
#     photos = crud.get_photos(db, skip=skip, limit=limit)
#     return photos
