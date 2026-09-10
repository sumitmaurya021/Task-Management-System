from typing import Optional
from fastapi import status, HTTPException, Request, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.user.dtos import UserSchema, LoginSchema
from sqlalchemy.orm import Session
from src.user.models import UserModel
from pwdlib import PasswordHash
from src.utils.settings import settings
from src.utils.db import get_db
from datetime import datetime, timedelta, timezone
import jwt
from jwt.exceptions import InvalidTokenError

security = HTTPBearer(auto_error=False)


password_hash = PasswordHash.recommended()

def get_password_hash(password):
    return password_hash.hash(password)

def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)

def register(body:UserSchema, db:Session):
    is_user = db.query(UserModel).filter(UserModel.username == body.username).first()
    if is_user:
        raise HTTPException(400, detail="Username already exist")

    is_email = db.query(UserModel).filter(UserModel.email == body.email).first()
    if is_email:
        raise HTTPException(400, detail="Email already exist")
    
    hashed_password = get_password_hash(body.password)

    new_user = UserModel(
        name = body.name,
        username = body.username,
        hashed_password = hashed_password,
        email = body.email
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user


def login_user(body:LoginSchema, db:Session):
    user = db.query(UserModel).filter(UserModel.username == body.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username")

    if not verify_password(body.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password")

    exp_time = datetime.now(timezone.utc) + timedelta(minutes=settings.EXP_TIME)
    token = jwt.encode({
        "id": user.id,
        "exp": exp_time
    }, settings.SECRET_KEY, settings.ALGORITHM)

    return {"success":True, "access_token":token}
    
    

def is_authenticated(
    request: Request,
    db: Session = Depends(get_db),
    token_auth: Optional[HTTPAuthorizationCredentials] = Depends(security)
):
    try:
        token = None
        if token_auth and token_auth.credentials:
            token = token_auth.credentials
        elif request.headers.get("authorization"):
            token = request.headers.get("authorization").split(" ")[-1]

        if not token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are unauthenticated")

        data = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
        user_id = data.get("id")

        user = db.query(UserModel).filter(UserModel.id == user_id).first()

        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
            
        return user
    except InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are unauthenticated")