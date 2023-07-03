from fastapi import FastAPI, APIRouter
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URL = "sqlite:///./db/sql_app.db"
engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )


def get_session():
    session_local = sessionmaker(autoflush=False, bind=engine)
    return session_local

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    tg_id = Column(Integer)
    first_name = Column(String)
    last_name = Column(String)
    username = Column(String)
    hash = Column(String)


class Photo(Base):
    __tablename__ = "photos"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    url = Column(String, unique=True)
    isDetectionCorrect = Column(Boolean)


Base.metadata.create_all(bind=engine)


app = FastAPI()
users_router = APIRouter()


@app.get("/")
async def get_main_page():
    return "I fucked python"


@users_router.get("/users", tags=['Users'])
async def get_users():
    db = get_session()

    return db.Query(User).all()


@users_router.post("/users", tags=['Users'])
async def add_user(tg_id: int, first_name: str,
                   last_name: str, username: str, hash: str):
    db = get_session()
    user = User(tg_id, first_name, last_name, username, hash)
    db.add(user)

    return user
