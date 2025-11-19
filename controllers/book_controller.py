from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from config.database import get_db
from services.book_service import BookService
from services.author_service import AuthorService
from services.category_service import CategoryService
from schemas.book_schema import BookResponse, BookCreate, BookUpdate
from config.dependencies import get_current_active_user

router = APIRouter(prefix="/api/books", tags=["books"])

@router.get("/", response_model=List[BookResponse])
def get_all_books(
    skip: int = Query(0, ge=0, description="Пропустить записей"),
    limit: int = Query(100, ge=1, le=1000, description="Лимит записей"),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)):
    book_service = BookService(db)
    books = book_service.find_all()
    return books[skip:skip + limit]

@router.get("/{book_id}", response_model=BookResponse)
def get_book_by_id(
    book_id: int, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    book_service = BookService(db)
    book = book_service.find_by_id(book_id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with ID {book_id} not found"
        )
    return book

@router.post("/", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
def create_book(
    book_create: BookCreate, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    book_service = BookService(db)
    author_service = AuthorService(db)
    category_service = CategoryService(db)
    
    author = author_service.find_by_id(book_create.author_id)
    if not author:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"The author with ID {book_create.author_id} does not exist."
        )
    if book_create.category_id:
        category = category_service.find_by_id(book_create.category_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Category with ID {book_create.category_id} does not exist")

    existing_book = book_service.find_by_isbn(book_create.isbn)
    if existing_book:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"A book with ISBN {book_create.isbn} already exists"
        )
    
    return book_service.save(book_create)

@router.put("/{book_id}", response_model=BookResponse)
def update_book(book_id: int, book_update: BookUpdate, db: Session = Depends(get_db)):
    book_service = BookService(db)
    
    existing_book = book_service.find_by_id(book_id)
    if not existing_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with ID {book_id} not found"
        )
    
    if book_update.author_id:
        author_service = AuthorService(db)
        author = author_service.find_by_id(book_update.author_id)
        if not author:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"The author with ID {book_update.author_id} does not exist."
            )
    if book_update.isbn and book_update.isbn != existing_book.isbn:
        book_with_isbn = book_service.find_by_isbn(book_update.isbn)
        if book_with_isbn and book_with_isbn.id != book_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"A book with ISBN {book_update.isbn} already exists"
            )
    
    updated_book = book_service.update(book_id, book_update)
    if not updated_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with ID {book_id} not found"
        )
    return updated_book

@router.get("/public/", response_model=List[BookResponse])
def get_public_books(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)):
    book_service = BookService(db)
    books = book_service.find_all()
    return books[skip:skip + limit]


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book_service = BookService(db)
    if not book_service.delete_by_id(book_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with ID {book_id} not found"
        )

@router.get("/search/title/{title}", response_model=List[BookResponse])
def search_books_by_title(title: str, db: Session = Depends(get_db)):
    book_service = BookService(db)
    return book_service.find_by_title_containing(title)

@router.get("/author/{author_id}", response_model=List[BookResponse])
def get_books_by_author(author_id: int, db: Session = Depends(get_db)):
    book_service = BookService(db)
    return book_service.find_by_author_id(author_id)

@router.get("/search/title/{title}", response_model=List[BookResponse])
def search_books_by_title(title: str, db: Session = Depends(get_db)):
    book_service = BookService(db)
    return book_service.find_by_title_containing(title)

@router.get("/isbn/{isbn}", response_model=BookResponse)
def get_book_by_isbn(isbn: str, db: Session = Depends(get_db)):
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
    book_service = BookService(db)
    return book_service.find_available_books()

@router.get("/overdue/", response_model=List[BookResponse])
def get_overdue_books(db: Session = Depends(get_db)):
    book_service = BookService(db)
    return book_service.find_overdue_books()