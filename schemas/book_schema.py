from pydantic import BaseModel, Field, validator
from datetime import date
from typing import Optional
from .author_schema import AuthorResponse

class BookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, description="Book Title")
    isbn: str = Field(..., min_length=10, max_length=20, description="Book ISBN")
    publication_date: Optional[date] = None
    available_copies: int = Field(ge=0, description="Available number of copies")
    author_id: int = Field(..., gt=0, description="Author ID")
    category_id: Optional[int] = Field(None, gt=0, description="Category ID")

class BookCreate(BookBase):
    @validator('title')
    def title_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("The book title is required")
        return v.strip()
    
    @validator('isbn')
    def isbn_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("ISBN is required")
        return v.strip()

class BookUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    isbn: Optional[str] = Field(None, min_length=10, max_length=20)
    publication_date: Optional[date] = None
    available_copies: Optional[int] = Field(None, ge=0)
    author_id: Optional[int] = Field(None, gt=0)
    category_id: Optional[int] = Field(None, gt=0)

class BookResponse(BookBase):
    id: int
    author: Optional[AuthorResponse] = None
    category_name: Optional[str] = None
    
    class Config:
        from_attributes = True