from fastapi import FastAPI
from src.utils.db import Base, engine
from src.tasks.models import TaskModel

Base.metadata.create_all(engine)

app = FastAPI(title="This is my Task Management Application")

@app.get("/")
def read_root():
    return {"message": "Welcome to Task Management API!"}