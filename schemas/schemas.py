from typing import Optional
from pydantic import BaseModel


class PhotoBase(BaseModel):
    name: str
    isDetectionCorrect: Optional[bool]


class PhotoCreate(PhotoBase):
    name: str
    isDetectionCorrect: Optional[bool]


class Photo(BaseModel):
    id: int
    owner_id: int
    name: str
    url: str
    isDetectionCorrect: Optional[bool]

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    tg_id: int
    first_name: str
    last_name: str
    username: str
    hash: str


class UserCreate(UserBase):
    pass


class User(BaseModel):
    tg_id: int
    first_name: str
    last_name: str
    username: str
    hash: str
    isAdmin: Optional[bool]
    photos: Optional[list[Photo]] = []

    class Config:
        orm_mode = True
