import datetime

from fastapi import APIRouter, HTTPException, Depends, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from db.models import get_db
from schemas import schemas
from logic import crud
from neuro_processing.photo_processor import detect_objects_on_image, draw_rectangles


users_router = APIRouter(prefix='/users', tags=['Users'])


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


@users_router.post("/{user_id}/photos/", response_class=FileResponse)
async def create_photo_for_user(
    user_id: int, file: UploadFile, db: Session = Depends(get_db)
):
    if not file.content_type.__contains__('image'):
        raise HTTPException(status_code=404, detail="Filetype is incorrect")
    current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    file_name = f"{current_time}_{file.filename}"
    file_path = f"photos/unprocessed/{file_name}"
    with open(file_path, "wb") as f:
        f.write(await file.read())
    photo = schemas.PhotoCreate(name=file_name, url=file_path, is_favorite=False)
    result_photo = crud.create_user_photo(db=db, photo=photo, user_id=user_id)
    res = detect_objects_on_image(file_path)
    draw_rectangles(file_name, res[0][0], res[0][1], res[0][2], res[0][3])
    return file_path
