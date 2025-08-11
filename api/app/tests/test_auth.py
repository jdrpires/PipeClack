import pytest
from httpx import AsyncClient

@pytest.mark.anyio
async def test_login_invalid(client: AsyncClient):
    res = await client.post("/auth/login", json={"email":"wrong@x.com","password":"123"})
    assert res.status_code == 400

@pytest.mark.anyio
async def test_login_valid_and_refresh(client: AsyncClient):
    res = await client.post("/auth/login", json={"email":"admin@clack.com","password":"Admin@123"})
    assert res.status_code == 200
    tokens = res.json()
    refresh = await client.post("/auth/refresh", json=tokens)
    assert refresh.status_code == 200

@pytest.mark.anyio
async def test_rbac_block(client: AsyncClient):
    res = await client.post("/auth/login", json={"email":"dev@clack.com","password":"Dev@123"})
    token = res.json()["access_token"]
    res2 = await client.post("/projects/", json={"name":"Test"}, headers={"Authorization":f"Bearer {token}"})
    assert res2.status_code == 403

@pytest.mark.anyio
async def test_rbac_allow(client: AsyncClient):
    res = await client.post("/auth/login", json={"email":"po@clack.com","password":"Po@123"})
    token = res.json()["access_token"]
    res2 = await client.post("/projects/", json={"name":"Test2"}, headers={"Authorization":f"Bearer {token}"})
    assert res2.status_code == 200
