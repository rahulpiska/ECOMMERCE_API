from passlib.context import CryptContext


import os
from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer

from database import get_db
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from models import User


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated = "auto"
)

def hash_password(password:str):
    return pwd_context.hash(password)

def verify_password(
        plain_password: str,
        hashed_password: str
):
    return pwd_context.verify(
        plain_password,
        hashed_password
    )

#--------------JWT---------------------------------------
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os. getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

def create_access_token(data:dict):
    to_encode = data.copy()

    expire = datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update(
        {"exp":expire}
    )

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)


#---------------------------------------------------------------
def get_current_user(
        token: str = Depends(oauth2_scheme),
        db:Session = Depends(get_db)
    ):
    
    try:
        playload =jwt.decode(
        token,
        SECRET_KEY,
        algorithms=[ALGORITHM]
        )

        user_id = playload.get("user_id")

    except JWTError:
        raise HTTPException(
        status_code=401,
        detail="Invalid token"
    )

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    
    return user

#--------------------------------------------------------------------------

def get_current_admin(
        current_user: User = Depends(get_current_user)
):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )
    return current_user






