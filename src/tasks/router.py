from fastapi import APIRouter, Depends
from src.tasks import controller
from src.tasks import dtos
from src.utils.db import get_db
from fastapi import status, HTTPException
from src.tasks.dtos import TaskSchema, TastResponseSchema
from typing import List
from sqlalchemy.orm import Session
from src.utils.helpers import is_authenticated
from src.users.models import User

task_routes = APIRouter(prefix = "/tasks")

@task_routes.post("/create", response_model=TastResponseSchema, status_code=status.HTTP_201_CREATED)
def create_task(body: dtos.TaskSchema, db: Session = Depends(get_db), user:User =  Depends(is_authenticated)):
    return controller.create_task(body, db, user)


@task_routes.get("/all_tasks", response_model=List[TastResponseSchema],status_code=status.HTTP_200_OK)
def get_tasks(db: Session = Depends(get_db),  user:User =  Depends(is_authenticated)):
    return controller.get_tasks(db)
 


@task_routes.get("/one_tasks/{task_id}", status_code=status.HTTP_200_OK)
def get_one_task(task_id: int, db: Session = Depends(get_db),  user:User =  Depends(is_authenticated)):
    return controller.get_one_task(task_id, db)


@task_routes.put("/update_tasks/{task_id}", status_code=status.HTTP_201_CREATED)
def update_task(task_id: int, body: dtos.TaskSchema, db: Session = Depends(get_db),  user:User =  Depends(is_authenticated)):
    return controller.update_task(task_id, body, db)


@task_routes.delete("/delete_task/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(get_db),  user:User =  Depends(is_authenticated)):
    return controller.delete_task(task_id, db)