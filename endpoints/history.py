from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db.models import get_db
from schemas import schemas
from logic import crud


history_router = APIRouter(prefix='/history', tags=['History'])


@history_router.get("/{user_id}/", response_model=schemas.History)
def get_user_history(user_id: int, db: Session = Depends(get_db)):
    history = crud.get_user_history(db, user_id)
    if history is None:
        raise HTTPException(status_code=404, detail="User not found")
    return history
