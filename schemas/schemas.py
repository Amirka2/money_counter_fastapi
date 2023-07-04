from pydantic import BaseModel


class PhotoBase(BaseModel):
    name: str
    url: str
    isDetectionCorrect: bool


class PhotoCreate(PhotoBase):
    pass


class Photo(PhotoBase):
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


class UserCreate(UserBase):
    tg_id = int
    first_name = str
    last_name = str
    username = str
    hash = str


class User(UserBase):
    id: int
    tg_id = int
    first_name = str
    last_name = str
    username = str
    hash = str
    photos: list[Photo] = []

    class Config:
        orm_mode = True
