from sqlalchemy.orm import Session
from typing import List, Optional
from models.user import User
from sqlalchemy import or_

class UserRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def find_all(self) -> List[User]:
        return self.db.query(User).all()
    
    def find_by_id(self, user_id: int) -> Optional[User]:
        return self.db.query(User).filter(User.id == user_id).first()
    
    def save(self, user: User) -> User:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def delete_by_id(self, user_id: int) -> bool:
        user = self.find_by_id(user_id)
        if user:
            self.db.delete(user)
            self.db.commit()
            return True
        return False
    
    def update(self, user_id: int, user_data: dict) -> Optional[User]:
        user = self.find_by_id(user_id)
        if user:
            for key, value in user_data.items():
                setattr(user, key, value)
            self.db.commit()
            self.db.refresh(user)
        return user
    
    def find_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).filter(User.email == email).first()
    
    def search_by_name(self, search_term: str) -> List[User]:
        return self.db.query(User).filter(
            or_(
                User.first_name.ilike(f"%{search_term}%"),
                User.last_name.ilike(f"%{search_term}%")
            )
        ).all()
    
    def exists_by_email(self, email: str) -> bool:
        return self.db.query(User).filter(User.email == email).first() is not None
    
    def find_users_with_active_loans(self) -> List[User]:
        from models.loan import Loan, LoanStatus
        return self.db.query(User).join(Loan).filter(Loan.status == LoanStatus.ACTIVE).distinct().all()