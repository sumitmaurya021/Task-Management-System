from src.tasks.dtos import TaskSchema
from sqlalchemy.orm import Session
from src.tasks.models import TaskModel
from src.user.models import UserModel
from fastapi import HTTPException

def create_tasks(body: TaskSchema, db: Session, current_user: UserModel):
    data = body.model_dump()
    new_task = TaskModel(
        title=data["title"],
        description=data["description"],
        is_completed=data["is_completed"],
        user_id=current_user.id
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task

def get_tasks(db: Session, current_user: UserModel):
    tasks = db.query(TaskModel).filter(TaskModel.user_id == current_user.id).all()
    return tasks


def get_one_task(task_id: int, db: Session, current_user: UserModel):
    one_task = db.query(TaskModel).filter(TaskModel.id == task_id, TaskModel.user_id == current_user.id).first()
    if not one_task:
        raise HTTPException(404, detail="Task not found")

    return one_task


def update_task(body: TaskSchema, task_id: int, db: Session, current_user: UserModel):
    one_task = db.query(TaskModel).filter(TaskModel.id == task_id, TaskModel.user_id == current_user.id).first()
    if not one_task:
        raise HTTPException(404, detail="Task not found")
    
    data = body.model_dump()
    for field, value in data.items():
        setattr(one_task, field, value)

    db.add(one_task)
    db.commit()
    db.refresh(one_task)

    return one_task


def delete_task(task_id: int, db: Session, current_user: UserModel):
    one_task = db.query(TaskModel).filter(TaskModel.id == task_id, TaskModel.user_id == current_user.id).first()
    if not one_task:
        raise HTTPException(404, detail="Task not found")
    
    db.delete(one_task)
    db.commit()
    return None