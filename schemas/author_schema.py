from pydantic import BaseModel, Field, validator
from datetime import date
from typing import Optional

class AuthorBase(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=100, description="Author's name")
    last_name: str = Field(..., min_length=1, max_length=100, description="Author's last name")
    birth_date: Optional[date] = None
    biography: Optional[str] = Field(None, max_length=1000, description="Biography")

class AuthorCreate(AuthorBase):
    @validator('first_name')
    def first_name_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("Author's name is required")
        return v.strip()
    
    @validator('last_name')
    def last_name_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("Author's last name is required")
        return v.strip()

class AuthorUpdate(BaseModel):
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    birth_date: Optional[date] = None
    biography: Optional[str] = Field(None, max_length=1000)

class AuthorResponse(AuthorBase):
    id: int
    
    class Config:
        from_attributes = True