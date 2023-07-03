from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

from fastapi import FastAPI, APIRouter

# строка подключения
SQLALCHEMY_DATABASE_URL = "sqlite:///./db/sql_app.db"

# создаем движок SqlAlchemy
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
# создаем базовый класс для моделей
Base = declarative_base()


# создаем модель, объекты которой будут храниться в бд
class Person(Base):
    __tablename__ = "people"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    age = Column(Integer, )


# создаем таблицы
Base.metadata.create_all(bind=engine)

# приложение, которое ничего не делает
app = FastAPI()
router = APIRouter()


@router.get("/")
async def root():
    return {"message": "Hello World"}


@router.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
