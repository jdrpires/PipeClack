import pytest
from httpx import AsyncClient

async def auth_header(client, email, password):
    res = await client.post("/auth/login", json={"email":email,"password":password})
    token = res.json()["access_token"]
    return {"Authorization":f"Bearer {token}"}

@pytest.mark.anyio
async def test_crud_card_move(client: AsyncClient):
    hdr = await auth_header(client, "po@clack.com", "Po@123")
    res = await client.post("/projects/", json={"name":"Proj1"}, headers=hdr)
    project_id = res.json()["id"]
    res = await client.post(f"/projects/{project_id}/boards", json={"tipo":"DEV"}, headers=hdr)
    board_id = res.json()["id"]
    cols_res = await client.get(f"/boards/{board_id}/columns", headers=hdr)
    cols = cols_res.json()
    first_col, second_col = cols[0]["id"], cols[1]["id"]
    card_res = await client.post(f"/boards/{board_id}/cards", json={"column_id":first_col,"titulo":"Card1"}, headers=hdr)
    card = card_res.json()
    move_res = await client.post(f"/cards/{card['id']}/move", json={"to_column_id":second_col, "position":2000}, headers=hdr)
    moved = move_res.json()
    assert moved["column_id"] == second_col
    assert moved["position"] == 2000
