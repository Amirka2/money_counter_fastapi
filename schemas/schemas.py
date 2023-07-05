from typing import Optional
from pydantic import BaseModel


class PhotoBase(BaseModel):
    name: str
    is_detection_correct: Optional[bool]
    is_favorite: bool


class PhotoCreate(PhotoBase):
    pass


class Photo(BaseModel):
    id: int
    owner_id: int
    name: str
    url: str
    is_detection_correct: Optional[bool]
    is_favorite: bool

    class Config:
        orm_mode = True


class DetectedPhoto(BaseModel):
    id: int
    owner_id: int
    name: str
    url: str
    is_detection_correct: Optional[bool]
    is_favorite: bool

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    id: int
    tg_id: int
    first_name: str
    last_name: str
    username: str
    hash: str
    tokens_value: int = 10


class UserCreate(UserBase):
    pass


class User(BaseModel):
    id: int
    tg_id: int
    first_name: str
    last_name: str
    username: str
    hash: str
    tokens_value: int = 10
    is_admin: Optional[bool]
    photos: Optional[list[Photo]] = []
    detected_photos: Optional[list[Photo]] = []

    class Config:
        orm_mode = True
