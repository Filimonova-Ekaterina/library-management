from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import hashlib

from models.user import User
from schemas.auth_schema import TokenData
from config.security import SECRET_KEY, ALGORITHM
from .user_service import UserService


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.user_service = UserService(db) 
    
    def simple_hash_password(self, password: str) -> str:
        salt = "library_salt_"
        return hashlib.sha256(f"{salt}{password}".encode()).hexdigest()
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.simple_hash_password(plain_password) == hashed_password
    
    def get_password_hash(self, password: str) -> str:
        return self.simple_hash_password(password)
    
    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        user = self.user_service.find_by_email(email)
        
        if not user:
            return None
        if not self.verify_password(password, user.password):
            return None
        
        return user
    
    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    
    def verify_token(self, token: str) -> TokenData:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            email: str = payload.get("sub")
            user_id: int = payload.get("user_id")
            if email is None or user_id is None:
                raise credentials_exception
            return TokenData(email=email, user_id=user_id)
        except JWTError:
            raise credentials_exception