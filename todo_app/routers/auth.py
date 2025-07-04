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
    prefix="/auth",
    tags=["auth"],
)

secret_key = '84e72db8c15b3d9dc69701992bd98076ba8069c362780c9e8f30f7c9e6005946'
ALGORITHM = 'HS256'

becrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
outh2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")


def get_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()



def authenticate_user(username: str, password: str, db):
    user = db.query(Users).filter(Users.username == username).first()
    if user is None:
        return False
    if not becrypt_context.verify(password, user.hashed_password):
        return False
    return user


def create_access_token(username: str, user_id:int, role:str, expires_delta: timedelta):
    encode = {'sub': username, 'id': user_id, 'role': role}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp': expires})

    return jwt.encode(encode, secret_key, algorithm=ALGORITHM)

def get_user(token: Annotated[str, Depends(outh2_bearer)]):
    try:
        payload = jwt.decode(token, secret_key, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        user_role: str = payload.get('role')

        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not validate credentials')

        return {'username': username, 'id': user_id, 'role': user_role}

    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate credentials')


db_dependency = Annotated[Session,Depends(get_db)]



class CreateUser(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str

@router.post('/auth',status_code=status.HTTP_201_CREATED)
def create_user(db: db_dependency, user_req: CreateUser):
    create_user_model = Users(
        username=user_req.username,
        email=user_req.email,
        first_name=user_req.first_name,
        last_name=user_req.last_name,
        hashed_password=becrypt_context.hash(user_req.password),
        role=user_req.role,
        is_active=True
    )

    db.add(create_user_model)
    db.commit()



@router.post('/token')
def get_token(db: db_dependency, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):

    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        return 'YOU ARE NOT AUTHENTICATED'

    token = create_access_token(user.username,user.id,user.role,timedelta(minutes=20))

    return {'access_token': token}


