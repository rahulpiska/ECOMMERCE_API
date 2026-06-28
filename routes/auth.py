from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from utils import verify_password, create_access_token, get_current_user
from models import User
from fastapi.security import OAuth2PasswordRequestForm

from schemas import(
    UserLogin,
    UserResponse
)


router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

@router.post('/login')
def user_login(form_data: OAuth2PasswordRequestForm = Depends(),
               db:Session= Depends(get_db)):
    
    user = db.query(User).filter(User.email == form_data.username).first()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid creditials"
        )
    
    check_password = verify_password(
        form_data.password,
        user.password
    )

    if not check_password:
        raise HTTPException(
            status_code=401,
            detail="Invalid credintials"
        )
    
    token = create_access_token(
        {"user_id": user.id}
    )
    
    return {
        'access_token': token,
        "token_type":"bearer"
    }

@router.get("/me", response_model=UserResponse)
def get_user(current_user:User = Depends(get_current_user)):

    return current_user

