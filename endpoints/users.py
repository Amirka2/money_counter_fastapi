from fastapi import APIRouter
from models.models import User


router = APIRouter(prefix="/users/")


@router.get("/")
async def get_users():
    return {"message": "Hello World"}


@router.post("/")
async def add_user(name: str):
    return {User}