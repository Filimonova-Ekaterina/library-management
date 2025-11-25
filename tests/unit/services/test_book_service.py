import pytest
from unittest.mock import Mock, MagicMock
from datetime import date
from sqlalchemy.orm import Session

from services.book_service import BookService
from repositories.book_repository import BookRepository
from schemas.book_schema import BookCreate, BookUpdate
from models.book import Book
from models.author import Author
from models.category import Category


class TestBookService:
    @pytest.fixture
    def mock_db(self):
        return Mock(spec=Session)
    
    @pytest.fixture
    def book_service(self, mock_db):
        return BookService(mock_db)
    
    @pytest.fixture
    def sample_author(self):
        author = Author(
            first_name="Лев",
            last_name="Толстой",
            birth_date=date(1828, 9, 9),
            biography="Русский писатель"
        )
        author.id = 1
        return author
    
    @pytest.fixture
    def sample_category(self):
        category = Category(
            name="Художественная литература",
            description="Романы, повести"
        )
        category.id = 1
        return category
    
    @pytest.fixture
    def sample_book(self, sample_author, sample_category):
        book = Book(
            title="Война и мир",
            isbn="978-5-17-123456-7",
            publication_date=date(1869, 1, 1),
            available_copies=5,
            author_id=1,
            category_id=1
        )
        book.id = 1
        book.author = sample_author
        book.category = sample_category
        return book
    
    def test_find_all_should_return_all_books(self, book_service, mock_db, sample_book):
        expected_books = [sample_book]
        book_service.book_repository.find_all = Mock(return_value=expected_books)
        actual_books = book_service.find_all()
        assert len(actual_books) == 1
        assert actual_books[0].title == "Война и мир"
        book_service.book_repository.find_all.assert_called_once()
    
    def test_find_by_id_when_book_exists_should_return_book(self, book_service, sample_book):
        book_service.book_repository.find_by_id = Mock(return_value=sample_book)
        result = book_service.find_by_id(1)
        assert result is not None
        assert result.title == "Война и мир"
        book_service.book_repository.find_by_id.assert_called_once_with(1)
    
    def test_find_by_id_when_book_not_exists_should_return_none(self, book_service):
        book_service.book_repository.find_by_id = Mock(return_value=None)
        result = book_service.find_by_id(999)
        assert result is None
        book_service.book_repository.find_by_id.assert_called_once_with(999)
    
    def test_save_should_return_saved_book(self, book_service, sample_book):
        book_create = BookCreate(
            title="Война и мир",
            isbn="978-5-17-123456-7",
            publication_date=date(1869, 1, 1),
            available_copies=5,
            author_id=1,
            category_id=1
        )
        
        book_service.book_repository.save = Mock(return_value=sample_book)
        result = book_service.save(book_create)
        assert result.title == "Война и мир"
        book_service.book_repository.save.assert_called_once()
    
    def test_delete_by_id_should_call_repository(self, book_service):
        book_service.book_repository.delete_by_id = Mock(return_value=True)
        result = book_service.delete_by_id(1)
        assert result is True
        book_service.book_repository.delete_by_id.assert_called_once_with(1)
    
    def test_find_by_title_containing_should_return_matching_books(self, book_service, sample_book):
        expected_books = [sample_book]
        book_service.book_repository.find_by_title_containing = Mock(return_value=expected_books)
        result = book_service.find_by_title_containing("война")
        assert len(result) == 1
        assert result[0].title == "Война и мир"
        book_service.book_repository.find_by_title_containing.assert_called_once_with("война")
    
    def test_find_by_author_id_should_return_books_by_author(self, book_service, sample_book):
        expected_books = [sample_book]
        book_service.book_repository.find_by_author_id = Mock(return_value=expected_books)
        result = book_service.find_by_author_id(1)
        assert len(result) == 1
        assert result[0].title == "Война и мир"
        book_service.book_repository.find_by_author_id.assert_called_once_with(1)
    
    def test_update_should_return_updated_book(self, book_service, sample_book):
        book_update = BookUpdate(title="Война и мир - том 1")
        updated_book = sample_book
        updated_book.title = "Война и мир - том 1"
        book_service.book_repository.update = Mock(return_value=updated_book)
        result = book_service.update(1, book_update)
        assert result.title == "Война и мир - том 1"
        book_service.book_repository.update.assert_called_once()