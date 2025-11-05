from typing import List, Optional
from sqlalchemy.orm import Session
from models.author import Author
from repositories.author_repository import AuthorRepository
from schemas.author_schema import AuthorCreate, AuthorUpdate

class AuthorService:
    def __init__(self, db: Session):
        self.author_repository = AuthorRepository(db)
    
    def find_all(self) -> List[Author]:
        return self.author_repository.find_all()
    
    def find_by_id(self, author_id: int) -> Optional[Author]:
        return self.author_repository.find_by_id(author_id)
    
    def save(self, author_create: AuthorCreate) -> Author:
        author = Author(**author_create.dict())
        return self.author_repository.save(author)
    
    def delete_by_id(self, author_id: int) -> bool:
        return self.author_repository.delete_by_id(author_id)
    
    def update(self, author_id: int, author_update: AuthorUpdate) -> Optional[Author]:
        update_data = {k: v for k, v in author_update.dict().items() if v is not None}
        return self.author_repository.update(author_id, update_data)
    
    def search_by_name(self, search_term: str) -> List[Author]:
        return self.author_repository.search_by_name(search_term)
    
    def find_by_last_name(self, last_name: str) -> List[Author]:
        return self.author_repository.find_by_last_name(last_name)
    
    def find_authors_with_books(self) -> List[Author]:
        return self.author_repository.find_authors_with_books()
    
    def count_books_by_author_id(self, author_id: int) -> int:
        return self.author_repository.count_books_by_author_id(author_id)