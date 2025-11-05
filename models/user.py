from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from config.database import Base

class User(Base):
    __tablename__ = "users" 
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    email = Column(String(100), nullable=False, unique=True)
    
    password = Column(String(255), nullable=False)
    
    first_name = Column(String(50), nullable=False)
    
    last_name = Column(String(50), nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    loans = relationship("Loan", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User {self.email}>"