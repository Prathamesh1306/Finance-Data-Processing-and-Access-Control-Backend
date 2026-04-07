import pytest

@pytest.mark.asyncio
async def test_anyone_can_list_transactions(async_client, viewer_token, sample_transaction):
    response = await async_client.get("/api/v1/transactions", headers={"Authorization": f"Bearer {viewer_token}"})
    assert response.status_code == 200
    assert len(response.json()["items"]) >= 1

@pytest.mark.asyncio
async def test_viewer_cannot_create_transaction(async_client, viewer_token):
    response = await async_client.post("/api/v1/transactions", headers={"Authorization": f"Bearer {viewer_token}"}, json={
        "amount": 100,
        "type": "EXPENSE",
        "category": "FOOD",
        "date": "2026-04-01"
    })
    assert response.status_code == 403

@pytest.mark.asyncio
async def test_admin_can_create_transaction(async_client, admin_token):
    response = await async_client.post("/api/v1/transactions", headers={"Authorization": f"Bearer {admin_token}"}, json={
        "amount": 250.50,
        "type": "INCOME",
        "category": "SALARY",
        "date": "2026-04-01"
    })
    assert response.status_code == 201

@pytest.mark.asyncio
async def test_date_filter_works(async_client, admin_token, sample_transaction):
    response = await async_client.get("/api/v1/transactions?date_from=2026-04-01&date_to=2026-04-01", headers={"Authorization": f"Bearer {admin_token}"})
    assert len(response.json()["items"]) >= 1
    
    empty_resp = await async_client.get("/api/v1/transactions?date_from=2026-05-01&date_to=2026-05-31", headers={"Authorization": f"Bearer {admin_token}"})
    assert len(empty_resp.json()["items"]) == 0

@pytest.mark.asyncio
async def test_admin_can_soft_delete(async_client, admin_token, sample_transaction):
    tx_id = sample_transaction.id
    response = await async_client.delete(f"/api/v1/transactions/{tx_id}", headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 204
    
    get_resp = await async_client.get(f"/api/v1/transactions/{tx_id}", headers={"Authorization": f"Bearer {admin_token}"})
    assert get_resp.status_code == 404
    
    list_resp = await async_client.get("/api/v1/transactions", headers={"Authorization": f"Bearer {admin_token}"})
    assert all(tx["id"] != str(tx_id) for tx in list_resp.json()["items"])

@pytest.mark.asyncio
async def test_create_with_amount_zero_or_future_date(async_client, admin_token):
    response = await async_client.post("/api/v1/transactions", headers={"Authorization": f"Bearer {admin_token}"}, json={
        "amount": 0,
        "type": "INCOME",
        "category": "SALARY",
        "date": "2026-12-01"
    })
    assert response.status_code == 422
