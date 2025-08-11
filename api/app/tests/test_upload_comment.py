import pytest
from httpx import AsyncClient
from io import BytesIO

async def auth_header(client):
    res = await client.post("/auth/login", json={"email":"po@clack.com","password":"Po@123"})
    token = res.json()["access_token"]
    return {"Authorization":f"Bearer {token}"}

@pytest.mark.anyio
async def test_upload_and_comment(client: AsyncClient):
    hdr = await auth_header(client)
    res = await client.post("/projects/", json={"name":"ProjAtt"}, headers=hdr)
    project_id = res.json()["id"]
    res = await client.post(f"/projects/{project_id}/boards", json={"tipo":"DEV"}, headers=hdr)
    board_id = res.json()["id"]
    cols = (await client.get(f"/boards/{board_id}/columns", headers=hdr)).json()
    first_col = cols[0]["id"]
    card = (await client.post(f"/boards/{board_id}/cards", json={"column_id":first_col,"titulo":"Card"}, headers=hdr)).json()
    # upload file
    file = BytesIO(b"test")
    res = await client.post(f"/cards/{card['id']}/attachments", files={"file":("test.txt", file, "text/plain")}, headers=hdr)
    assert res.status_code == 200
    # comment
    res = await client.post(f"/cards/{card['id']}/comments", json={"texto":"hello"}, headers=hdr)
    assert res.status_code == 200
    comments = (await client.get(f"/cards/{card['id']}/comments", headers=hdr)).json()
    assert len(comments) == 1
