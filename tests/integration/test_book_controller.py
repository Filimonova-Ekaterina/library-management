import pytest
import time


class TestBookController:
    def test_get_books_without_auth_should_return_unauthorized(self, client):
        response = client.get("/api/books/")
        assert response.status_code in [401, 403]
    
    def test_get_public_books_should_return_ok(self, client):
        response = client.get("/api/books/public/")
        assert response.status_code == 200
    
    def test_search_books_by_title_should_return_ok(self, client):
        response = client.get("/api/books/search/title/война")
        assert response.status_code in [200, 404]
    
    def test_get_books_with_auth_should_return_ok(self, client):
        unique_email = f"bookuser_{int(time.time())}@library.com"
        user_data = {
            "email": unique_email,
            "password": "password123",
            "first_name": "Book",
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
        response = client.get("/api/books/", headers=headers)
        assert response.status_code == 200
        assert isinstance(response.json(), list)