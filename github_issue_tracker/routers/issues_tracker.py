from enum import Enum
from datetime import datetime
from typing import Annotated, Optional

from pydantic import BaseModel,Field
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, Path, Body,APIRouter
from starlette import status

import models
from models import Issues
from database import engine, sessionlocal


router = APIRouter(
    prefix="/issues_tracker",
    tags=["issues_tracker"],
)

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]

#pydantic class here

class IssueStatus(str, Enum):
    open = 'Open'
    closed = 'Closed'
    in_progress = 'In Progress'


class AddIssue(BaseModel):
    title: str=Field(...,min_length=5, max_length=50)
    body: str=Field(...,min_length=5, max_length=500)
    status: IssueStatus=Field(...,example='In Progress,Closed,Open',description='Please follow this pattern for status')

    class Config:
        schema_extra = {
            "example": {
                "title": "Login Issue",
                "body": "App crashes after entering credentials.",
                "status": "In progress"
            }
        }

class UpdateIssue(BaseModel):
    title: Optional[str]=Field(None,min_length=5, max_length=50)
    body: Optional[str]=Field(None, min_length=5, max_length=500)
    status: Optional[IssueStatus]=Field(None,example='In Progress,Closed,Open',description='Please follow this pattern for status')

    class Config:
        schema_extra = {
            "example": {
                "title": "Login Issue",
                "body": "App crashes after entering credentials.",
                "status": "In progress"
            }
        }

#get methods here


@router.get("/")
async def root():
    return {'WELCOME TO GIT ISSUES TRACKER'}

@router.get('/all_issues',status_code=status.HTTP_200_OK)
async def get_all_issues(db:db_dependency):
    return db.query(Issues).all()


@router.get('/issue/{issue_id}',status_code=status.HTTP_200_OK)
async def get_issue( db:db_dependency,issue_id: int =Path(description='enter id of the issue you want to get',gt=0)):
    issue = db.query(Issues).filter(Issues.id == issue_id).first()
    if issue is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='issue not found')

    return issue

#post methods

@router.post('/addissue',status_code=status.HTTP_201_CREATED)
async def add_issue(db:db_dependency, issue: AddIssue):
    new_issue = Issues(title=issue.title, body=issue.body, status=issue.status.value,created_at=datetime.utcnow(),
        updated_at=datetime.utcnow())

    db.add(new_issue)
    db.commit()

    return new_issue


@router.put('/updateissue/{issue_id}',status_code=status.HTTP_200_OK)
async def update_issue(db:db_dependency, issue_id: int=Path(...,gt=0), issue: UpdateIssue=Body(...)):
    updated_issue = db.query(Issues).filter(Issues.id == issue_id).first()
    if updated_issue is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='issue not found')

    if issue.title is not None:
        updated_issue.title = Issues.title
    if issue.body is not None:
        updated_issue.body = issue.body
    if issue.status is not None:
        updated_issue.status = issue.status.value

    updated_issue.updated_at = datetime.utcnow()

    db.add(updated_issue)
    db.commit()

    return updated_issue


@router.delete('/deleteissue/{issue_id}',status_code=status.HTTP_204_NO_CONTENT)
async def delete_issue(db:db_dependency, issue_id: int=Path(...,gt=0)):
    deleted_issue = db.query(Issues).filter(Issues.id == issue_id).first()
    if deleted_issue is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='issue not found')

    db.delete(deleted_issue)
    db.commit()


