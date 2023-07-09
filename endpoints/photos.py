from fastapi import APIRouter, Depends, UploadFile, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import FileResponse
import datetime

from db.models import get_db
from schemas import schemas
from logic import crud
from neuro_processing.photo_processor import detect_objects_on_image, work_with_items
from neuro_processing.photo_processor import processed_photo_folder, unprocessed_photo_folder


photos_router = APIRouter(prefix='/photos', tags=['Photos'])


@photos_router.post("/{user_id}/", response_class=FileResponse)
async def create_photo_for_user(
    user_id: int, file: UploadFile, db: Session = Depends(get_db)
):
    user = crud.get_user(db, user_id)
    if user.tokens_value <= 0:
        raise HTTPException(status_code=404, detail="tokens are out")
    user.tokens_value = user.tokens_value - 1
    crud.change_user_info(db, user)
    if not file.content_type.__contains__('image'):
        raise HTTPException(status_code=404, detail="Filetype is incorrect")
    current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    file_name = f"{current_time}_{file.filename}"
    file_path = f"photos/unprocessed/{file_name}"
    with open(file_path, "wb") as f:
        f.write(await file.read())
    photo = schemas.PhotoCreate(name=file_name, url=file_path, is_favorite=False)
    crud.create_user_photo(db=db, photo=photo, user_id=user_id)
    file_path = unprocessed_photo_folder + file_name
    сoords_list = detect_objects_on_image(file_path)
    if len(сoords_list) < 1:
        return file_path
    processed_photo_path, message_sum, money_classes = work_with_items(file_name, сoords_list)
    message = schemas.MessageCreate(owner_id=user_id,
                                    message_text=f"{', '.join(money_classes)}",
                                    message_sum=message_sum)
    crud.create_user_message(db, user_id, message)
    return processed_photo_path


@photos_router.get("/{user_id}/", response_model=list[schemas.Photo])
def read_photos(user_id: int, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    photos = crud.get_photos(db, user_id, skip=skip, limit=limit)
    return photos


@photos_router.get("/{user_id}/favorite", response_model=list[schemas.Photo])
def read_photos(user_id: int, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    fav_photos = crud.get_favorite_photos(db, user_id, skip=skip, limit=limit)
    return fav_photos
