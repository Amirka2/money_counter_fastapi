from fastapi import APIRouter
from db.models import User
from db.sessions import get_session


router = APIRouter(prefix="/users/")


@router.get("/")
async def get_users():
    db = get_session()
    
    return db.Query(User).all()


@router.post("/")
async def add_user(tg_id: int, first_name: str,
                   last_name: str, username: str, hash: str):
    db = get_session()
    user = User(tg_id, first_name, last_name, username, hash)
    db.add(user)

    return user
