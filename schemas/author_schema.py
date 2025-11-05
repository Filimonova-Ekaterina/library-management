from pydantic import BaseModel
from datetime import date
from typing import Optional, List

class AuthorCreate(BaseModel):
    first_name: str
    last_name: str
    birth_date: Optional[date] = None
    biography: Optional[str] = None

class AuthorUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    birth_date: Optional[date] = None
    biography: Optional[str] = None

class AuthorResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    birth_date: Optional[date] = None
    biography: Optional[str] = None
    
    class Config:
        from_attributes = True