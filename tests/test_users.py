import pytest

@pytest.mark.asyncio
async def test_admin_can_list_users(async_client, admin_token):
    response = await async_client.get("/api/v1/users", headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 200
    assert "items" in response.json()

@pytest.mark.asyncio
async def test_viewer_cannot_list_users(async_client, viewer_token):
    response = await async_client.get("/api/v1/users", headers={"Authorization": f"Bearer {viewer_token}"})
    assert response.status_code == 403

@pytest.mark.asyncio
async def test_admin_can_create_user(async_client, admin_token):
    response = await async_client.post("/api/v1/users", headers={"Authorization": f"Bearer {admin_token}"}, json={
        "email": "admin_created@test.com",
        "full_name": "Created by Admin",
        "password": "password",
        "role": "ANALYST"
    })
    assert response.status_code == 201

@pytest.mark.asyncio
async def test_admin_can_update_user_role(async_client, admin_token):
    list_response = await async_client.get("/api/v1/users", headers={"Authorization": f"Bearer {admin_token}"})
    viewer_id = [u for u in list_response.json()["items"] if u["role"] == "VIEWER"][0]["id"]
    
    response = await async_client.patch(f"/api/v1/users/{viewer_id}", headers={"Authorization": f"Bearer {admin_token}"}, json={
        "role": "ANALYST"
    })
    assert response.status_code == 200
    assert response.json()["role"] == "ANALYST"

@pytest.mark.asyncio
async def test_admin_cannot_delete_themselves(async_client, admin_token):
    me_resp = await async_client.get("/api/v1/users", headers={"Authorization": f"Bearer {admin_token}"})
    admin_id = [u for u in me_resp.json()["items"] if u["email"] == "admin@test.com"][0]["id"]
    
    response = await async_client.delete(f"/api/v1/users/{admin_id}", headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 403

@pytest.mark.asyncio
async def test_get_non_existent_user(async_client, admin_token):
    import uuid
    response = await async_client.get(f"/api/v1/users/{uuid.uuid4()}", headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 404
