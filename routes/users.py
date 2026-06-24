from fastapi import  APIRouter, HTTPException,Depends
from sqlalchemy.orm import Session
from models import User
from database import get_db

from schemas import(
    UserCreate,
    UserResponse
)

from utils import hash_password

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post('',response_model=UserResponse)
def create_user(create_user:UserCreate,
                db:Session = Depends(get_db)):
    
    existing_user = db.query(User).filter(User.email == create_user.email).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="User with this email already exists"
        )
    
    hashed_password = hash_password(create_user.password)

    new_user = User(
        name= create_user.name,
        email= create_user.email,
        password= hashed_password
    )

    db.add(new_user)

    db.commit()
    db.refresh(new_user)

    return new_user