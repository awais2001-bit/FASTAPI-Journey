import token
from datetime import timedelta, datetime, timezone
from typing import Annotated
from fastapi import APIRouter,Depends,HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from ..models import Users
from ..database import sessionlocal
from passlib.context import CryptContext
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError


router = APIRouter(
    prefix="/users",
    tags=["users"],
)

secret_key = '73ad04ad316d7da7a10f19ca68db80269772b7b45d7aa439831b25962b091dad'
ALGORITHM = 'HS256'


becrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
outh2_bearer = OAuth2PasswordBearer(tokenUrl='users/token')

def get_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session,Depends(get_db)]

def authenticate_user(db, username: str, password: str):
    user = db.query(Users).filter(Users.username == username).first()
    if user is None:
        return False
    if not becrypt_context.verify(password, user.hashed_password):
        return False

    return user

def create_access_token(username: str, user_id: str, expires_delta: timedelta):
    encode = {'sub': username, 'id': user_id}
    expire = datetime.utcnow() + expires_delta
    encode.update({'exp': expire})

    return jwt.encode(encode, secret_key, algorithm=ALGORITHM)

def get_user(token: Annotated[str, Depends(outh2_bearer)]):
    try:
        payload = jwt.decode(token, secret_key, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: str = payload.get('id')

        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


        return {'username': username, 'user_id': user_id}

    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)




class CreateUser(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str



@router.post('/create', status_code=status.HTTP_201_CREATED)
def create_user(user: CreateUser, db:db_dependency):
    user_model = Users(username=user.username,
                       email=user.email,
                       first_name=user.first_name,
                       last_name=user.last_name,
                       hashed_password= becrypt_context.hash(user.password)
                       )

    db.add(user_model)
    db.commit()






