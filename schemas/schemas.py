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

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    tg_id: int
    first_name: str
    last_name: str
    username: str


class UserCreate(UserBase):
    hash: str


class User(UserBase):
    id: int
    photos: list[Photo] = []

    class Config:
        orm_mode = True
