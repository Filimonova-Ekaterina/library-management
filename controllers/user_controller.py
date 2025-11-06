from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from config.database import get_db
from services.user_service import UserService
from schemas.user_schema import UserResponse, UserCreate, UserUpdate

router = APIRouter(prefix="/api/users", tags=["users"])

@router.get("/", response_model=List[UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    user_service = UserService(db)
    return user_service.find_all()

@router.get("/{user_id}", response_model=UserResponse)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user_service = UserService(db)
    user = user_service.find_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    return user

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user_create: UserCreate, db: Session = Depends(get_db)):
    user_service = UserService(db)
    
    if user_service.exists_by_email(user_create.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )
    
    return user_service.save(user_create)

@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    user_service = UserService(db)
    user = user_service.update(user_id, user_update)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    return user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user_service = UserService(db)
    if not user_service.delete_by_id(user_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )

@router.get("/email/{email}", response_model=UserResponse)
def get_user_by_email(email: str, db: Session = Depends(get_db)):
    user_service = UserService(db)
    user = user_service.find_by_email(email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with email {email} not found"
        )
    return user

@router.get("/search/{name}", response_model=List[UserResponse])
def search_users_by_name(name: str, db: Session = Depends(get_db)):
    user_service = UserService(db)
    return user_service.search_by_name(name)