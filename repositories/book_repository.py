from sqlalchemy.orm import Session
from typing import List, Optional
from models.book import Book
from sqlalchemy import or_, and_

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
    
    def update(self, book_id: int, book_data: dict) -> Optional[Book]:
        book = self.find_by_id(book_id)
        if book:
            for key, value in book_data.items():
                setattr(book, key, value)
            self.db.commit()
            self.db.refresh(book)
        return book
    
    def find_by_title_containing(self, title: str) -> List[Book]:
        return self.db.query(Book).filter(Book.title.ilike(f"%{title}%")).all()
    
    def find_by_isbn(self, isbn: str) -> Optional[Book]:
        return self.db.query(Book).filter(Book.isbn == isbn).first()
    
    def find_by_author_id(self, author_id: int) -> List[Book]:
        return self.db.query(Book).filter(Book.author_id == author_id).all()
    
    def find_by_category_id(self, category_id: int) -> List[Book]:
        return self.db.query(Book).filter(Book.category_id == category_id).all()
    
    def find_available_books(self, min_copies: int = 1) -> List[Book]:
        return self.db.query(Book).filter(Book.available_copies >= min_copies).all()
    
    def find_by_title_and_author_lastname(self, title: str, author_lastname: str) -> List[Book]:
        from models.author import Author
        return self.db.query(Book).join(Author).filter(
            Book.title.ilike(f"%{title}%"),
            Author.last_name.ilike(f"%{author_lastname}%")
        ).all()
    
    def find_overdue_books(self) -> List[Book]:
        from models.loan import Loan, LoanStatus
        from sqlalchemy import func
        return self.db.query(Book).join(Loan).filter(
            Loan.due_date < func.now(),
            Loan.status == LoanStatus.ACTIVE
        ).all()