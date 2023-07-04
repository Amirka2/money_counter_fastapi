from fastapi import FastAPI, APIRouter
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import query

tags_metadata = [
    {
        "name": "Users",
        "description": "Operations with users. The **login** logic is also here.",
    },
    {
        "name": "Photos",
        "description": "Operations with users. The **login** logic is also here.",
    }
]

SQLALCHEMY_DATABASE_URL = "sqlite:///./db/sql_app.db"
engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )


def get_session():
    session_local = sessionmaker(autoflush=False, bind=engine)
    return session_local


Base = declarative_base()




Base.metadata.create_all(bind=engine)


app = FastAPI(openapi_tags=tags_metadata)


@app.get("/")
async def get_main_page():
    return "I fucked python"


@app.get("/users/", tags=["Users"])
async def get_users():
    db = get_session()

    return db.query(User).all()


@app.post("/users/", tags=['Users'])
async def add_user(tg_id: int, first_name: str,
                   last_name: str, username: str, hash: str):
    db = get_session()
    user = User(tg_id, first_name, last_name, username, hash)
    db.add(user)
    db.commit()

    return user
