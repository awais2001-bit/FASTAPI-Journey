from typing import Annotated
from pydantic import BaseModel,Field
from sqlalchemy.orm import Session
from fastapi import  Depends, HTTPException, Path, APIRouter
from starlette import status
from ..models import Users
from ..database import  sessionlocal
from .auth import get_user
from passlib.context import CryptContext

router = APIRouter(
    prefix='/user',
    tags= ['user']
)


def get_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()

becrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_user)]

class passwordchange(BaseModel):
    password: str
    new_password: str = Field(..., min_length=8, max_length=128)


@router.get('/get_details')
async def get_user_details(user: user_dependency, db: db_dependency):
    if user is None or user.get('role') != 'user':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return db.query(Users).filter(Users.id == user.get('id')).first()


@router.put('/change password')
async def change_password(user: user_dependency, password: str, db: db_dependency, user_pass: passwordchange):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()

    if not becrypt_context.verify(user_model.hashed_password, user_pass.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    user_model.hashed_password = becrypt_context.hash(user_pass.new_password)
    db.add(user_model)
    db.commit()


