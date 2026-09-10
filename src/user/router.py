from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from src.user.dtos import UserSchema, UserResponseSchema, LoginSchema
from src.user.models import UserModel
from src.utils.db import get_db
from src.user import controller


user_routes = APIRouter(prefix="/users")


@user_routes.post("/register", response_model=UserResponseSchema, status_code=status.HTTP_201_CREATED)
async def register(body: UserSchema, db: Session = Depends(get_db)):  
    return await controller.register(body=body,db=db)

@user_routes.post("/login", status_code=status.HTTP_200_OK)
def login(body: LoginSchema, db: Session = Depends(get_db)):  
    return controller.login_user(body=body,db=db)

@user_routes.get("/is_auth", status_code=status.HTTP_200_OK, response_model=UserResponseSchema)
def is_auth(current_user: UserModel = Depends(controller.is_authenticated)):
    return current_user