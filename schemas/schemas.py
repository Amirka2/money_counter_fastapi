from typing import Optional

from pydantic import BaseModel


class PhotoBase(BaseModel):
    owner_id: int
    name: str
    url: str
    isDetectionCorrect: Optional[bool]


class PhotoCreate(PhotoBase):
    owner_id: int
    name: str
    url: str
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
    tg_id: int
    first_name: str
    last_name: str
    username: str
    hash: str


class User(BaseModel):
    tg_id: int
    first_name: str
    last_name: str
    username: str
    hash: str
    photos: Optional[list[Photo]] = []

    class Config:
        orm_mode = True
