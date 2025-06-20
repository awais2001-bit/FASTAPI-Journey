from typing import Annotated,List
import os
from fastapi import FastAPI
from pydantic import BaseModel,Field
import json

app = FastAPI()

class Todo(BaseModel):
    id: Annotated[int,Field(...,description='id of the task')]
    title: Annotated[str,Field(...,description='title of the task')]
    completed: Annotated[bool,Field(...,description='if the task is completed')]


tasks_file='tasks.json'
def read_tasks() -> List[dict]:
    if not os.path.exists(tasks_file):
        return []
    with open(tasks_file, 'r') as f:
        return json.load(f)

def write_tasks(tasks: List[dict]):
    with open(tasks_file, 'w') as f:
        json.dump(tasks, f, indent=4)
@app.post("/newtask")
def new_task(todo: Todo):
    tasks = read_tasks()
    tasks.append(todo.dict())
    write_tasks(tasks)
    return {"message": "Task saved successfully", "task": todo}



