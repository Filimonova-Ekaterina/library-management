from typing import List, Optional
from sqlalchemy.orm import Session
from models.book import Book
from repositories.book_repository import BookRepository
from schemas.book_schema import BookCreate, BookUpdate

class BookService:
    def __init__(self, db: Session):
        self.book_repository = BookRepository(db)
    
    def find_all(self) -> List[Book]:
        return self.book_repository.find_all()
    
    def find_by_id(self, book_id: int) -> Optional[Book]:
        return self.book_repository.find_by_id(book_id)
    
    def save(self, book_create: BookCreate) -> Book:
        book = Book(**book_create.dict())
        return self.book_repository.save(book)
    
    def delete_by_id(self, book_id: int) -> bool:
        return self.book_repository.delete_by_id(book_id)
    
    def update(self, book_id: int, book_update: BookUpdate) -> Optional[Book]:
        update_data = {k: v for k, v in book_update.dict().items() if v is not None}
        return self.book_repository.update(book_id, update_data)
    
    def find_by_title_containing(self, title: str) -> List[Book]:
        return self.book_repository.find_by_title_containing(title)
    
    def find_by_author_id(self, author_id: int) -> List[Book]:
        return self.book_repository.find_by_author_id(author_id)
    
    def find_by_isbn(self, isbn: str) -> Optional[Book]:
        return self.book_repository.find_by_isbn(isbn)
    
    def find_available_books(self) -> List[Book]:
        return self.book_repository.find_available_books()
    
    def find_by_title_and_author_lastname(self, title: str, author_lastname: str) -> List[Book]:
        return self.book_repository.find_by_title_and_author_lastname(title, author_lastname)
    
    def find_overdue_books(self) -> List[Book]:
        return self.book_repository.find_overdue_books()