from typing import Annotated, Dict, Optional
from pydantic import BaseModel,Field
from sqlalchemy.orm import Session
from fastapi import  Depends, HTTPException, Path, APIRouter
from starlette import status

from ..models import todos
from ..database import  sessionlocal
from .auth import get_user

router = APIRouter(
    prefix='/to',
    tags= ['todos']
)


def get_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_user)]

class todoRequest(BaseModel):
    title: str = Field(min_length = 3)
    description: str = Field(min_length=3, max_length=100)
    priority: int=Field(gt=-1, lt=5)
    status: bool=Field(default=False)

class UpdateTodoRequest(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[int] = Field(default=None, gt=-1, lt=5)
    status: Optional[bool] = None

@router.get('/')
def get_all(db: db_dependency, user: user_dependency):
    return db.query(todos).filter(todos.owner_id==user.get('id')).all()


@router.get('/todos/{todo_id}')
def get_todo(db: db_dependency, todo_id:int=Path(gt=0)):
    todo_model = db.query(todos).filter(todos.id == todo_id).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail='Todo id is not found')


@router.get('/todos/priority/{pr}')
def get_by_priority(db: db_dependency, pr:int=Path(gt=-1)):
    todo_model = db.query(todos).filter(todos.priority == pr).all()
    if todo_model:
        return todo_model
    raise HTTPException(status_code=404, detail='Priority is not found')


@router.post('/todos/new',status_code=status.HTTP_201_CREATED)
def new_todo(db: db_dependency, user: user_dependency, todo_req: todoRequest):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    todo_model = todos(**todo_req.dict(), owner_id=user.get('id'))

    db.add(todo_model)
    db.commit()


@router.put('/todos/update/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
def update_todo(db: db_dependency, todo_id: int, todo_req: UpdateTodoRequest):
    todo_model = db.query(todos).filter(todos.id == todo_id).first()

    if not todo_model:
        raise HTTPException(status_code=404, detail='Todo not found')

    if todo_req.title is not None:
        todo_model.title = todo_req.title
    if todo_req.description is not None:
        todo_model.description = todo_req.description
    if todo_req.priority is not None:
        todo_model.priority = todo_req.priority
    if todo_req.status is not None:
        todo_model.status = todo_req.status

    db.add(todo_model)
    db.commit()



@router.delete('/todo/del/{id}',status_code=status.HTTP_204_NO_CONTENT)
def del_todo(db: db_dependency, id: int=Path(gt=0)):
    todo_model = db.query(todos).filter(todos.id==id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail='not found')
    db.delete(todo_model)
    db.commit()

