from fastapi import FastAPI
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from endpoints.photos import router as photos_router
from endpoints.users import router as users_router


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

SessionLocal = sessionmaker(autoflush=False, bind=engine)
Base = declarative_base()
Base.metadata.create_all(bind=engine)

app = FastAPI(openapi_tags=tags_metadata)
app.include_router(users_router, tags=['Users'])
app.include_router(photos_router, tags=['Photos'])


@app.get("/")
async def get_main_page():
    return "I fucked python"

