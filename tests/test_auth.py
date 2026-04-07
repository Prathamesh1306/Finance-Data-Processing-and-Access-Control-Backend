import pytest

@pytest.mark.asyncio
async def test_register_new_user(async_client):
    response = await async_client.post("/api/v1/auth/register", json={
        "email": "new@test.com",
        "full_name": "New User",
        "password": "Password123!"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "new@test.com"

@pytest.mark.asyncio
async def test_register_duplicate_email(async_client):
    await async_client.post("/api/v1/auth/register", json={
        "email": "admin@test.com",
        "full_name": "Existing",
        "password": "Password123!"
    })
    response = await async_client.post("/api/v1/auth/register", json={
        "email": "admin@test.com",
        "full_name": "Existing",
        "password": "Password123!"
    })
    assert response.status_code == 409

@pytest.mark.asyncio
async def test_login_valid_credentials(async_client):
    response = await async_client.post("/api/v1/auth/login", json={
        "email": "admin@test.com",
        "password": "password"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

@pytest.mark.asyncio
async def test_login_wrong_password(async_client):
    response = await async_client.post("/api/v1/auth/login", json={
        "email": "admin@test.com",
        "password": "wrongpassword"
    })
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_login_inactive_user(async_client):
    response = await async_client.post("/api/v1/auth/login", json={
        "email": "inactive@test.com",
        "password": "password"
    })
    assert response.status_code == 403
