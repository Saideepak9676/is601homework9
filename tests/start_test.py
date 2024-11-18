import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app  # Import the FastAPI app from your app.main module

# Test: Login for Access Token
@pytest.mark.asyncio
async def test_login_for_access_token():
    form_data = {
        "username": "admin",
        "password": "secret",
    }
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/token", json=form_data)  # Ensure correct path '/token'
        # Ensure the token endpoint returns status 200
        assert response.status_code == 200
        assert "access_token" in response.json()

# Test: Create QR Code Unauthorized
@pytest.mark.asyncio
async def test_create_qr_code_unauthorized():
    qr_request = {
        "url": "https://example.com",
        "fill_color": "red",
        "back_color": "white",
        "size": 10,
    }
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/qr-codes/", json=qr_request)  # Ensure correct path '/qr-codes/'
        assert response.status_code == 401  # Unauthorized if no token is provided

# Test: Create and Delete QR Code
@pytest.mark.asyncio
async def test_create_and_delete_qr_code():
    form_data = {
        "username": "admin",
        "password": "secret",
    }
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # Login and get the access token
        token_response = await ac.post("/token", json=form_data)  # Ensure correct path '/token'
        assert token_response.status_code == 200
        access_token = token_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}
    
        # Create a QR code
        qr_request = {
            "url": "https://example.com",
            "fill_color": "red",
            "back_color": "white",
            "size": 10,
        }
        create_response = await ac.post("/qr-codes/", json=qr_request, headers=headers)  # Ensure correct path '/qr-codes/'
        assert create_response.status_code == 200  # Successfully created QR code