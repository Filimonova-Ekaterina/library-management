import pytest
from unittest.mock import Mock
from datetime import datetime

from services.user_service import UserService
from schemas.user_schema import UserCreate, UserUpdate
from models.user import User


class TestUserService:
    @pytest.fixture
    def user_service(self):
        mock_db = Mock()
        return UserService(mock_db)
    
    @pytest.fixture
    def sample_user(self):
        user = User(
            email="test@library.com",
            password="hashedpassword123",
            first_name="Test",
            last_name="User"
        )
        user.id = 1
        user.created_at = datetime.now()
        return user
    
    def test_find_all_should_return_all_users(self, user_service, sample_user):
        expected_users = [sample_user]
        user_service.user_repository.find_all = Mock(return_value=expected_users)
        actual_users = user_service.find_all()
        
        assert len(actual_users) == 1
        assert actual_users[0].email == "test@library.com"
        user_service.user_repository.find_all.assert_called_once()
    
    def test_find_by_id_when_user_exists_should_return_user(self, user_service, sample_user):
        user_service.user_repository.find_by_id = Mock(return_value=sample_user)
        result = user_service.find_by_id(1)
        assert result is not None
        assert result.email == "test@library.com"
        user_service.user_repository.find_by_id.assert_called_once_with(1)
    
    def test_save_should_return_saved_user(self, user_service, sample_user):
        user_create = UserCreate(
            email="test@library.com",
            password="password123",
            first_name="Test",
            last_name="User"
        )
        
        user_service.user_repository.save = Mock(return_value=sample_user)
        result = user_service.save(user_create)
        assert result.email == "test@library.com"
        user_service.user_repository.save.assert_called_once()
    
    def test_find_by_email_when_user_exists_should_return_user(self, user_service, sample_user):
        user_service.user_repository.find_by_email = Mock(return_value=sample_user)
        result = user_service.find_by_email("test@library.com")
        assert result is not None
        assert result.email == "test@library.com"
        user_service.user_repository.find_by_email.assert_called_once_with("test@library.com")
    
    def test_exists_by_email_when_user_exists_should_return_true(self, user_service):
        user_service.user_repository.exists_by_email = Mock(return_value=True)
        result = user_service.exists_by_email("test@library.com")
        assert result is True
        user_service.user_repository.exists_by_email.assert_called_once_with("test@library.com")