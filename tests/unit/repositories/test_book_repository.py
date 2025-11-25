import pytest
from datetime import date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.book import Book
from models.author import Author
from models.category import Category
from repositories.book_repository import BookRepository
from config.database import Base


class TestBookRepository:
    @pytest.fixture(scope="function")
    def db_session(self):
        engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
        TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        Base.metadata.create_all(bind=engine)
        
        session = TestingSessionLocal()
        yield session
        session.close()
        Base.metadata.drop_all(bind=engine)
    
    @pytest.fixture
    def book_repository(self, db_session):
        return BookRepository(db_session)
    
    @pytest.fixture
    def sample_data(self, db_session):
        author = Author(first_name="Лев", last_name="Толстой")
        category = Category(name="Художественная литература")
        
        db_session.add(author)
        db_session.add(category)
        db_session.commit()
        db_session.refresh(author)
        db_session.refresh(category)
        
        book = Book(
            title="Война и мир",
            isbn="978-5-17-123456-7",
            publication_date=date(1869, 1, 1),
            available_copies=5,
            author_id=author.id,
            category_id=category.id
        )
        
        db_session.add(book)
        db_session.commit()
        db_session.refresh(book)
        
        return {
            "author": author,
            "category": category,
            "book": book
        }
    
    def test_find_all_should_return_all_books(self, book_repository, sample_data):
        books = book_repository.find_all()
        assert len(books) == 1
        assert books[0].title == "Война и мир"
    
    def test_find_by_id_should_return_book(self, book_repository, sample_data):
        book = book_repository.find_by_id(sample_data["book"].id)
        assert book is not None
        assert book.title == "Война и мир"
    
    def test_find_by_title_containing_should_return_matching_books(self, book_repository, sample_data):
        books = book_repository.find_by_title_containing("Война")
        assert len(books) == 1
        assert books[0].title == "Война и мир"
    
    def test_find_by_title_containing_partial_match(self, book_repository, sample_data):
        books = book_repository.find_by_title_containing("ойна")
        assert len(books) == 1
        assert books[0].title == "Война и мир"
    
    def test_find_by_title_containing_no_matches(self, book_repository, sample_data):
        books = book_repository.find_by_title_containing("Несуществующая книга")
        
        # Then
        assert len(books) == 0