from typing import Annotated

from sqlalchemy.orm import Session
from fastapi import  Depends, HTTPException, APIRouter
from starlette import status

from ..models import todos
from ..database import  sessionlocal
from .auth import get_user

router = APIRouter(
    prefix='/admin',
    tags= ['admin']
)


def get_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_user)]


@router.get('/get_todos_user')
async def get_todos(user: user_dependency, db: db_dependency):
    if user is None or user.get('role') != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return db.query(todos).all()

