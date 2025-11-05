from sqlalchemy import Column, Integer, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from config.database import Base
import enum

class LoanStatus(enum.Enum):
    ACTIVE = "ACTIVE"
    RETURNED = "RETURNED"
    OVERDUE = "OVERDUE"

class Loan(Base):
    __tablename__ = "loans"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    book = relationship("Book")
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="loans")
    
    loan_date = Column(DateTime, nullable=False)
    
    due_date = Column(DateTime, nullable=False)
    
    return_date = Column(DateTime, nullable=True)
    
    status = Column(Enum(LoanStatus), default=LoanStatus.ACTIVE)
    
    def __repr__(self):
        return f"<Loan {self.id}>"