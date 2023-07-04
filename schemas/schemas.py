from pydantic import BaseModel


class PhotoBase(BaseModel):
    owner_id: int
    name: str
    url: str
    isDetectionCorrect: bool


class PhotoCreate(PhotoBase):
    owner_id: int
    name: str
    url: str
    isDetectionCorrect: bool


class Photo(BaseModel):
    id: int
    owner_id: int
    name: str
    url: str
    isDetectionCorrect = bool

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    tg_id: int
    first_name: str
    last_name: str
    username: str
    hash = str


class UserCreate(UserBase):
    tg_id = int
    first_name = str
    last_name = str
    username = str
    hash = str


class User(BaseModel):
    id: int
    tg_id = int
    first_name = str
    last_name = str
    username = str
    hash = str
    photos: list[Photo] = []

    class Config:
        orm_mode = True
