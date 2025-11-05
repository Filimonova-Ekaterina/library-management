from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from config.database import Base

class Book(Base):
    __tablename__ = "books" 
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    title = Column(String(200), nullable=False)
    isbn = Column(String(20), nullable=False, unique=True)
    
    publication_date = Column(Date, nullable=True)
    
    available_copies = Column(Integer, default=1)
    
    author_id = Column(Integer, ForeignKey("authors.id"))
    author = relationship("Author", back_populates="books")
    
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    category = relationship("Category", back_populates="books")
    
    def __repr__(self):
        return f"<Book {self.title}>"