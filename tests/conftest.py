import pytest
import sys
import os
import time
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app


@pytest.fixture(scope="function")
def client():
    """Test client fixture"""
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def auth_headers(client):
    unique_email = f"test_{int(time.time())}@library.com"
    
    user_data = {
        "email": unique_email,
        "password": "testpassword123",
        "first_name": "Test",
        "last_name": "User"
    }
    
    register_response = client.post("/api/auth/register", json=user_data)
    assert register_response.status_code == 201, f"Registration failed: {register_response.text}"
    login_data = {
        "email": unique_email,
        "password": "testpassword123"
    }
    
    login_response = client.post("/api/auth/login", json=login_data)
    assert login_response.status_code == 200, f"Login failed: {login_response.text}"
    
    token = login_response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def test_user_data():
    """Fixture with test user data"""
    unique_email = f"integration_test_{int(time.time())}@library.com"
    return {
        "email": unique_email,
        "password": "integration123",
        "first_name": "Integration",
        "last_name": "Test"
    }