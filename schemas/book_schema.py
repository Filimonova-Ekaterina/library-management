from pydantic import BaseModel
from datetime import date
from typing import Optional
from .author_schema import AuthorResponse

class BookCreate(BaseModel):
    title: str
    isbn: str
    publication_date: Optional[date] = None
    available_copies: int = 1
    author_id: int
    category_id: Optional[int] = None

class BookUpdate(BaseModel):
    title: Optional[str] = None
    isbn: Optional[str] = None
    publication_date: Optional[date] = None
    available_copies: Optional[int] = None
    author_id: Optional[int] = None
    category_id: Optional[int] = None

class BookResponse(BaseModel):
    id: int
    title: str
    isbn: str
    publication_date: Optional[date] = None
    available_copies: int
    author_id: int
    category_id: Optional[int] = None
    author: Optional[AuthorResponse] = None
    
    class Config:
        from_attributes = True