from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from config.database import get_db
from services.auth_service import AuthService
from schemas.auth_schema import TokenData

security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Зависимость для получения текущего пользователя"""
    auth_service = AuthService(db)
    token_data = auth_service.verify_token(credentials.credentials)
    
    from services.user_service import UserService
    user_service = UserService(db)
    user = user_service.find_by_email(token_data.email)
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Пользователь не найден",
        )
    return user

def get_current_active_user(current_user = Depends(get_current_user)):
    """Зависимость для получения активного пользователя"""
    return current_user