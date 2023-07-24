from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse

from db.models import get_db
from schemas import schemas
from logic import crud


login_router = APIRouter(prefix='/login', tags=['Login'])


@login_router.get("/")
def log_in(tg_id: int, first_name: str, username: str, hash: str, db: Session = Depends(get_db)):
    user = schemas.UserCreate(tg_id=tg_id, first_name=first_name, username=username, hash=hash)
    db_user = crud.get_user_by_username(db, username=user.username)
    response = JSONResponse(content={"message": "куки установлены"})
    if db_user is None:
        user = crud.create_user(db=db, user=user)
    else:
        user = db_user

    response.set_cookie(key="user_id", value=user.id)
    return response

