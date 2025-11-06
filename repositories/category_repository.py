from sqlalchemy.orm import Session
from typing import List, Optional
from models.category import Category

class CategoryRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def find_all(self) -> List[Category]:
        return self.db.query(Category).all()
    
    def find_by_id(self, category_id: int) -> Optional[Category]:
        return self.db.query(Category).filter(Category.id == category_id).first()
    
    def find_by_name(self, name: str) -> Optional[Category]:
        return self.db.query(Category).filter(Category.name == name).first()