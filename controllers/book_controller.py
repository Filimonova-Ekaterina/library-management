from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from config.database import get_db
from services.book_service import BookService
from schemas.book_schema import BookResponse, BookCreate, BookUpdate

router = APIRouter(prefix="/api/books", tags=["books"])

@router.get("/", response_model=List[BookResponse])
def get_all_books(db: Session = Depends(get_db)):
    """Get all books - GET /api/books/"""
    book_service = BookService(db)
    return book_service.find_all()

@router.get("/{book_id}", response_model=BookResponse)
def get_book_by_id(book_id: int, db: Session = Depends(get_db)):
    """Get book by ID - GET /api/books/{id}"""
    book_service = BookService(db)
    book = book_service.find_by_id(book_id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id {book_id} not found"
        )
    return book

@router.post("/", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
def create_book(book_create: BookCreate, db: Session = Depends(get_db)):
    """Create new book - POST /api/books/"""
    book_service = BookService(db)
    return book_service.save(book_create)

@router.put("/{book_id}", response_model=BookResponse)
def update_book(book_id: int, book_update: BookUpdate, db: Session = Depends(get_db)):
    """Update book - PUT /api/books/{id}"""
    book_service = BookService(db)
    book = book_service.update(book_id, book_update)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id {book_id} not found"
        )
    return book

@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    """Delete book - DELETE /api/books/{id}"""
    book_service = BookService(db)
    if not book_service.delete_by_id(book_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id {book_id} not found"
        )

@router.get("/search/{title}", response_model=List[BookResponse])
def search_books_by_title(title: str, db: Session = Depends(get_db)):
    """Search books by title - GET /api/books/search/{title}"""
    book_service = BookService(db)
    return book_service.find_by_title_containing(title)

@router.get("/author/{author_id}", response_model=List[BookResponse])
def get_books_by_author(author_id: int, db: Session = Depends(get_db)):
    """Get books by author - GET /api/books/author/{author_id}"""
    book_service = BookService(db)
    return book_service.find_by_author_id(author_id)

@router.get("/search/title/{title}", response_model=List[BookResponse])
def search_books_by_title(title: str, db: Session = Depends(get_db)):
    """Search books by title - GET /api/books/search/title/{title}"""
    book_service = BookService(db)
    return book_service.find_by_title_containing(title)

@router.get("/isbn/{isbn}", response_model=BookResponse)
def get_book_by_isbn(isbn: str, db: Session = Depends(get_db)):
    """Get book by ISBN - GET /api/books/isbn/{isbn}"""
    book_service = BookService(db)
    book = book_service.find_by_isbn(isbn)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with ISBN {isbn} not found"
        )
    return book

@router.get("/available/", response_model=List[BookResponse])
def get_available_books(db: Session = Depends(get_db)):
    """Get available books - GET /api/books/available/"""
    book_service = BookService(db)
    return book_service.find_available_books()

@router.get("/overdue/", response_model=List[BookResponse])
def get_overdue_books(db: Session = Depends(get_db)):
    """Get overdue books - GET /api/books/overdue/"""
    book_service = BookService(db)
    return book_service.find_overdue_books()