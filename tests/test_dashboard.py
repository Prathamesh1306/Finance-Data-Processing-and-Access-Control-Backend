import pytest

@pytest.mark.asyncio
async def test_summary_calculations(async_client, admin_token, sample_transaction):
    await async_client.post("/api/v1/transactions", headers={"Authorization": f"Bearer {admin_token}"}, json={
        "amount": 1000, "type": "INCOME", "category": "SALARY", "date": "2026-04-01"
    })
    await async_client.post("/api/v1/transactions", headers={"Authorization": f"Bearer {admin_token}"}, json={
        "amount": 200, "type": "EXPENSE", "category": "FOOD", "date": "2026-04-02"
    })
    
    response = await async_client.get("/api/v1/dashboard/summary", headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 200
    data = response.json()
    assert float(data["total_income"]) >= 1000.0
    assert float(data["total_expenses"]) >= 350.0

@pytest.mark.asyncio
async def test_viewer_access(async_client, viewer_token):
    response = await async_client.get("/api/v1/dashboard/summary", headers={"Authorization": f"Bearer {viewer_token}"})
    assert response.status_code == 200
    
    trends_response = await async_client.get("/api/v1/dashboard/trends", headers={"Authorization": f"Bearer {viewer_token}"})
    assert trends_response.status_code == 403

@pytest.mark.asyncio
async def test_analyst_access_trends(async_client, analyst_token):
    response = await async_client.get("/api/v1/dashboard/trends", headers={"Authorization": f"Bearer {analyst_token}"})
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_category_totals_percentages(async_client, admin_token, sample_transaction):
    await async_client.post("/api/v1/transactions", headers={"Authorization": f"Bearer {admin_token}"}, json={
        "amount": 850, "type": "EXPENSE", "category": "RENT", "date": "2026-04-01"
    })
    
    response = await async_client.get("/api/v1/dashboard/category-totals?type=EXPENSE", headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 200
    data = response.json()
    total_percent = sum(float(cat["percentage"]) for cat in data)
    assert 99.0 <= total_percent <= 101.0 or total_percent == 0.0
