from typing import List, Optional
from sqlalchemy.orm import Session
from models.category import Category
from repositories.category_repository import CategoryRepository

class CategoryService:
    def __init__(self, db: Session):
        self.category_repository = CategoryRepository(db)
    
    def find_all(self) -> List[Category]:
        return self.category_repository.find_all()
    
    def find_by_id(self, category_id: int) -> Optional[Category]:
        return self.category_repository.find_by_id(category_id)
    
    def find_by_name(self, name: str) -> Optional[Category]:
        return self.category_repository.find_by_name(name)