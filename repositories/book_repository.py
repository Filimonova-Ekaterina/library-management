from sqlalchemy.orm import Session
from typing import List, Optional
from models.book import Book

class BookRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def find_all(self) -> List[Book]:
        return self.db.query(Book).all()
    
    def find_by_id(self, book_id: int) -> Optional[Book]:
        return self.db.query(Book).filter(Book.id == book_id).first()
    
    def save(self, book: Book) -> Book:
        self.db.add(book)
        self.db.commit()
        self.db.refresh(book)
        return book
    
    def delete_by_id(self, book_id: int) -> bool:
        book = self.find_by_id(book_id)
        if book:
            self.db.delete(book)
            self.db.commit()
            return True
        return False
    
    def find_by_title_containing(self, title: str) -> List[Book]:
        return self.db.query(Book).filter(Book.title.contains(title)).all()
    
    def find_by_author_id(self, author_id: int) -> List[Book]:
        return self.db.query(Book).filter(Book.author_id == author_id).all()
    
    def update(self, book_id: int, book_data: dict) -> Optional[Book]:
        book = self.find_by_id(book_id)
        if book:
            for key, value in book_data.items():
                setattr(book, key, value)
            self.db.commit()
            self.db.refresh(book)
        return book