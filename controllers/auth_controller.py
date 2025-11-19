from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta

from config.database import get_db
from config.dependencies import get_current_active_user  # ← Импортируем зависимость
from config.security import ACCESS_TOKEN_EXPIRE_MINUTES
from services.auth_service import AuthService
from services.user_service import UserService
from schemas.auth_schema import LoginRequest, Token, UserRegister
from schemas.user_schema import UserResponse

router = APIRouter(prefix="/api/auth", tags=["authentication"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_data: UserRegister, db: Session = Depends(get_db)):
    user_service = UserService(db)
    auth_service = AuthService(db)
    if user_service.exists_by_email(user_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user's email address already exists."
        )
    hashed_password = auth_service.get_password_hash(user_data.password)
    from schemas.user_schema import UserCreate
    user_create = UserCreate(
        email=user_data.email,
        password=hashed_password,
        first_name=user_data.first_name,
        last_name=user_data.last_name
    )
    
    return user_service.save(user_create)

@router.post("/login", response_model=Token)
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    auth_service = AuthService(db)
    user = auth_service.authenticate_user(login_data.email, login_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Wrong email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth_service.create_access_token(
        data={"sub": user.email, "user_id": user.id},
        expires_delta=access_token_expires
    )
    
    return Token(access_token=access_token)

@router.get("/me", response_model=UserResponse)
def get_current_user_info(current_user = Depends(get_current_active_user)):
    return current_user