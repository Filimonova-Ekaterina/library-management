import pytest
from unittest.mock import Mock
from datetime import datetime, timedelta

from services.auth_service import AuthService
from models.user import User


class TestAuthService:
    @pytest.fixture
    def auth_service(self):
        mock_db = Mock()
        return AuthService(mock_db)
    
    @pytest.fixture
    def sample_user(self):
        user = User(
            email="test@library.com",
            password="5f4dcc3b5aa765d61d8327deb882cf99",
            first_name="Test",
            last_name="User"
        )
        user.id = 1
        return user
    
    def test_verify_password_with_correct_password_should_return_true(self, auth_service):
        plain_password = "password123"
        hashed_password = auth_service.get_password_hash(plain_password)
        result = auth_service.verify_password(plain_password, hashed_password)
        assert result is True
    
    def test_verify_password_with_incorrect_password_should_return_false(self, auth_service):
        plain_password = "password123"
        wrong_password = "wrongpassword"
        hashed_password = auth_service.get_password_hash(plain_password)
        result = auth_service.verify_password(wrong_password, hashed_password)
        assert result is False
    
    def test_authenticate_user_with_correct_credentials_should_return_user(self, auth_service):
        mock_user_service = Mock()
        sample_user = User(
            email="test@library.com",
            password=auth_service.get_password_hash("password123"),
            first_name="Test",
            last_name="User"
        )
        mock_user_service.find_by_email.return_value = sample_user
        auth_service.user_service = mock_user_service
        result = auth_service.authenticate_user("test@library.com", "password123")
        assert result == sample_user
        mock_user_service.find_by_email.assert_called_once_with("test@library.com")
    
    def test_authenticate_user_with_incorrect_password_should_return_none(self, auth_service):

        mock_user_service = Mock()
        sample_user = User(
            email="test@library.com",
            password=auth_service.get_password_hash("password123"), 
            first_name="Test",
            last_name="User"
        )
        mock_user_service.find_by_email.return_value = sample_user
        auth_service.user_service = mock_user_service
        
        result = auth_service.authenticate_user("test@library.com", "wrongpassword")
        
        assert result is None
    
    def test_authenticate_user_with_nonexistent_email_should_return_none(self, auth_service):
        mock_user_service = Mock()
        mock_user_service.find_by_email.return_value = None
        auth_service.user_service = mock_user_service
        result = auth_service.authenticate_user("nonexistent@library.com", "password123")
        assert result is None
    
    def test_create_access_token_should_return_jwt_token(self, auth_service):
        data = {"sub": "test@library.com", "user_id": 1}
        token = auth_service.create_access_token(data)
        assert token is not None
        assert isinstance(token, str)
    
    def test_verify_token_with_valid_token_should_return_token_data(self, auth_service):
        data = {"sub": "test@library.com", "user_id": 1}
        token = auth_service.create_access_token(data)
        token_data = auth_service.verify_token(token)
        assert token_data.email == "test@library.com"
        assert token_data.user_id == 1