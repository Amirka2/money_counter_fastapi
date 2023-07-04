import uvicorn
from fastapi import FastAPI,Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from db.models import get_db
from logic import crud
from schemas import schemas
from fastapi import APIRouter


tags_metadata = [
    {
        "name": "Users",
        "description": "Operations with users. The **login** logic is also here.",
    },
    {
        "name": "Photos",
        "description": "Operations with users. The **login** logic is also here.",
    }
]


users_router = APIRouter(prefix='/users', tags=['Users'])
photos_router = APIRouter(prefix='/photos', tags=['Photos'])


@users_router.post("/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="username already exists")
    return crud.create_user(db=db, user=user)


@users_router.get("/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@users_router.get("/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@users_router.post("/users/{user_id}/photos/", response_model=schemas.Photo)
def create_item_for_user(
    user_id: int, photo: schemas.PhotoCreate, db: Session = Depends(get_db)
):
    return crud.create_user_photo(db=db, photo=photo, user_id=user_id)


@photos_router.get("/", response_model=list[schemas.Photo])
def read_items(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    photos = crud.get_photos(db, skip=skip, limit=limit)
    return photos


app = FastAPI(openapi_tags=tags_metadata)
app.include_router(users_router)
app.include_router(photos_router)
app.mount("/", StaticFiles(directory="static", html=True), name="static")


if __name__ == '__main__':
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8080,
        reload=True
    )

