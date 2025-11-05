from sqlalchemy import Column, Integer, String, Date, Text
from sqlalchemy.orm import relationship
from config.database import Base

class Author(Base):
    __tablename__ = "authors" 
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    
    birth_date = Column(Date, nullable=True)
    biography = Column(Text, nullable=True)
    
    books = relationship("Book", back_populates="author", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Author {self.first_name} {self.last_name}>"