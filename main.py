import uvicorn
from fastapi import FastAPI, Depends, HTTPException, Cookie
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from db.models import get_db
from logic import crud
from logic.logic import is_admin
from schemas import schemas
from fastapi import APIRouter


tags_metadata = [
    {
        "name": "Users",
        "description": "Operations with users.",
    },
    {
        "name": "Photos",
        "description": "Operations with users.",
    },
    {
        "name": "Login",
    },
    {
        "name": "Admin",
        "description": "Operations for admins",
    }
]


login_router = APIRouter(prefix='/login', tags=['Login'])
users_router = APIRouter(prefix='/users', tags=['Users'])
photos_router = APIRouter(prefix='/photos', tags=['Photos'])
admin_router = APIRouter(prefix='/admin', tags=['Admin'])


@login_router.post("/")
def log_in(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    response = JSONResponse(content={"message": "куки установлены"})
    if db_user is None:
        user = crud.create_user(db, user)
    else:
        user = db_user

    response.set_cookie(key="user_id", value=user.id)
    return Cookie()


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


@users_router.post("/{user_id}/photos/", response_model=schemas.Photo)
def create_photo_for_user(
    user_id: int, photo: schemas.PhotoCreate, db: Session = Depends(get_db)
):
    return crud.create_user_photo(db=db, photo=photo, user_id=user_id)


@photos_router.get("/", response_model=list[schemas.Photo])
def read_photos(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    photos = crud.get_photos(db, skip=skip, limit=limit)
    return photos


@admin_router.patch("/tokens/{user_id}", response_model=schemas.User)
def change_tokens_value(user_id: int, tokens_value: int, db: Session = Depends(get_db)):
    cur_user = crud.get_user(db, Cookie())
    if not is_admin(cur_user):
        raise HTTPException(status_code=404, detail="You dont have rights")
    db_user = crud.get_user(db, user_id)
    user = db_user
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    user.tokens_value = tokens_value
    return crud.change_user_info(db, user)


@admin_router.post("/{user_id}", response_model=schemas.User)
def make_admin(user_id: int, db: Session = Depends(get_db)):
    cookie = Cookie()
    cur_user = crud.get_user(db, Cookie())
    if not is_admin(cur_user):
        raise HTTPException(status_code=404, detail="You dont have rights")
    db_user = crud.get_user(db, user_id)
    user = db_user
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    user.is_admin = True
    return crud.change_user_info(db, user)


app = FastAPI(openapi_tags=tags_metadata)
app.include_router(users_router)
app.include_router(photos_router)
app.include_router(login_router)
app.include_router(admin_router)
app.mount("/", StaticFiles(directory="static", html=True), name="static")


if __name__ == '__main__':
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8080,
        reload=True
    )

