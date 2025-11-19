from typing import List, Optional
from sqlalchemy.orm import Session
from models.user import User
from repositories.user_repository import UserRepository
from schemas.user_schema import UserCreate, UserUpdate

class UserService:
    def __init__(self, db: Session):
        self.user_repository = UserRepository(db)
    
    def find_all(self) -> List[User]:
        return self.user_repository.find_all()
    
    def find_by_id(self, user_id: int) -> Optional[User]:
        return self.user_repository.find_by_id(user_id)
    
    def save(self, user_create: UserCreate) -> User:
        user = User(**user_create.dict())
        return self.user_repository.save(user)
    
    def delete_by_id(self, user_id: int) -> bool:
        return self.user_repository.delete_by_id(user_id)
    
    def find_by_email(self, email: str) -> Optional[User]:
        return self.user_repository.find_by_email(email)
    
    def update(self, user_id: int, user_update: UserUpdate) -> Optional[User]:
        update_data = {k: v for k, v in user_update.dict().items() if v is not None}
        return self.user_repository.update(user_id, update_data)
    
    def search_by_name(self, search_term: str) -> List[User]:
        return self.user_repository.search_by_name(search_term)
    
    def exists_by_email(self, email: str) -> bool:
        return self.user_repository.exists_by_email(email)
    
    def find_users_with_active_loans(self) -> List[User]:
        return self.user_repository.find_users_with_active_loans()
    
    def create_user_with_hashed_password(self, user_create: UserCreate) -> User:
        from services.auth_service import AuthService
        auth_service = AuthService(self.db)
        
        hashed_password = auth_service.get_password_hash(user_create.password)
        user_data = user_create.dict()
        user_data['password'] = hashed_password
        
        user = User(**user_data)
        return self.user_repository.save(user)