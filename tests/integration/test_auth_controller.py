import pytest
import time


class TestAuthController:
    def test_register_new_user_should_return_user(self, client):
        unique_email = f"newuser_{int(time.time())}@library.com"
        user_data = {
            "email": unique_email,
            "password": "password123",
            "first_name": "New",
            "last_name": "User"
        }
        response = client.post("/api/auth/register", json=user_data)
        assert response.status_code == 201, f"Expected 201, got {response.status_code}. Response: {response.text}"
        data = response.json()
        assert data["email"] == unique_email
        assert data["first_name"] == "New"
        assert data["last_name"] == "User"
        assert "password" not in data 
    
    def test_login_with_correct_credentials_should_return_token(self, client):
        unique_email = f"loginuser_{int(time.time())}@library.com"
        user_data = {
            "email": unique_email,
            "password": "password123",
            "first_name": "Login",
            "last_name": "User"
        }
        
        register_response = client.post("/api/auth/register", json=user_data)
        assert register_response.status_code == 201, f"Registration failed: {register_response.text}"
        login_data = {
            "email": unique_email,
            "password": "password123"
        }
        response = client.post("/api/auth/login", json=login_data)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}. Response: {response.text}"
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
    
    def test_login_with_incorrect_password_should_return_unauthorized(self, client):
        unique_email = f"loginuser2_{int(time.time())}@library.com"
        user_data = {
            "email": unique_email,
            "password": "password123",
            "first_name": "Login",
            "last_name": "User"
        }
        register_response = client.post("/api/auth/register", json=user_data)
        assert register_response.status_code == 201
        
        login_data = {
            "email": unique_email,
            "password": "wrongpassword"
        }
        response = client.post("/api/auth/login", json=login_data)
        assert response.status_code == 401
    
    def test_register_existing_user_should_return_bad_request(self, client):
        unique_email = f"duplicate_{int(time.time())}@library.com"
        user_data = {
            "email": unique_email,
            "password": "password123",
            "first_name": "Duplicate",
            "last_name": "User"
        }
        register_response = client.post("/api/auth/register", json=user_data)
        assert register_response.status_code == 201
        response = client.post("/api/auth/register", json=user_data)
        assert response.status_code == 400
    
    def test_get_current_user_with_valid_token_should_return_user(self, client):
        unique_email = f"currentuser_{int(time.time())}@library.com"
        user_data = {
            "email": unique_email,
            "password": "password123",
            "first_name": "Current",
            "last_name": "User"
        }
        register_response = client.post("/api/auth/register", json=user_data)
        assert register_response.status_code == 201
        login_data = {
            "email": unique_email,
            "password": "password123"
        }
        
        login_response = client.post("/api/auth/login", json=login_data)
        assert login_response.status_code == 200
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        response = client.get("/api/auth/me", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == unique_email
        assert "password" not in data