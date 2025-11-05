from sqlalchemy.orm import Session
from typing import List, Optional
from models.author import Author
from sqlalchemy import or_, func

class AuthorRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def find_all(self) -> List[Author]:
        return self.db.query(Author).all()
    
    def find_by_id(self, author_id: int) -> Optional[Author]:
        return self.db.query(Author).filter(Author.id == author_id).first()
    
    def save(self, author: Author) -> Author:
        self.db.add(author)
        self.db.commit()
        self.db.refresh(author)
        return author
    
    def delete_by_id(self, author_id: int) -> bool:
        author = self.find_by_id(author_id)
        if author:
            self.db.delete(author)
            self.db.commit()
            return True
        return False
    
    def update(self, author_id: int, author_data: dict) -> Optional[Author]:
        author = self.find_by_id(author_id)
        if author:
            for key, value in author_data.items():
                setattr(author, key, value)
            self.db.commit()
            self.db.refresh(author)
        return author
    
    def search_by_name(self, search_term: str) -> List[Author]:
        return self.db.query(Author).filter(
            or_(
                Author.first_name.ilike(f"%{search_term}%"),
                Author.last_name.ilike(f"%{search_term}%")
            )
        ).all()
    
    def find_by_last_name(self, last_name: str) -> List[Author]:
        return self.db.query(Author).filter(Author.last_name.ilike(f"%{last_name}%")).all()
    
    def find_authors_with_books(self) -> List[Author]:
        from models.book import Book
        return self.db.query(Author).join(Book).distinct().all()
    
    def count_books_by_author_id(self, author_id: int) -> int:
        from models.book import Book
        return self.db.query(Book).filter(Book.author_id == author_id).count()