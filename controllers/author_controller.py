from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from config.database import get_db
from services.author_service import AuthorService
from schemas.author_schema import AuthorResponse, AuthorCreate, AuthorUpdate

router = APIRouter(prefix="/api/authors", tags=["authors"])

@router.get("/", response_model=List[AuthorResponse])
def get_all_authors(db: Session = Depends(get_db)):
    """Get all authors"""
    author_service = AuthorService(db)
    return author_service.find_all()

@router.get("/{author_id}", response_model=AuthorResponse)
def get_author_by_id(author_id: int, db: Session = Depends(get_db)):
    """Get author by ID"""
    author_service = AuthorService(db)
    author = author_service.find_by_id(author_id)
    if not author:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Author with id {author_id} not found"
        )
    return author

@router.post("/", response_model=AuthorResponse, status_code=status.HTTP_201_CREATED)
def create_author(author_create: AuthorCreate, db: Session = Depends(get_db)):
    """Create new author"""
    author_service = AuthorService(db)
    return author_service.save(author_create)

@router.put("/{author_id}", response_model=AuthorResponse)
def update_author(author_id: int, author_update: AuthorUpdate, db: Session = Depends(get_db)):
    """Update author"""
    author_service = AuthorService(db)
    author = author_service.update(author_id, author_update)
    if not author:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Author with id {author_id} not found"
        )
    return author

@router.delete("/{author_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_author(author_id: int, db: Session = Depends(get_db)):
    """Delete author"""
    author_service = AuthorService(db)
    if not author_service.delete_by_id(author_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Author with id {author_id} not found"
        )