import pytest
from httpx import AsyncClient

async def auth_header(client):
    res = await client.post("/auth/login", json={"email":"po@clack.com","password":"Po@123"})
    token = res.json()["access_token"]
    return {"Authorization":f"Bearer {token}"}

@pytest.mark.anyio
async def test_discovery_complete(client: AsyncClient):
    hdr = await auth_header(client)
    res = await client.post("/projects/", json={"name":"DiscProj"}, headers=hdr)
    project_id = res.json()["id"]
    template_res = await client.get("/projects/discovery/template", headers=hdr)
    template = template_res.json()
    respostas = {"requisitos_funcionais":[{"titulo":"Func1","descricao":"Desc","prioridade":"ALTA"}]}
    await client.post(f"/projects/{project_id}/discovery", json={"template_id":template["id"],"respostas_json":respostas}, headers=hdr)
    complete = await client.post(f"/projects/{project_id}/discovery/complete", headers=hdr)
    assert complete.status_code == 200
    # verify board created
    boards = await client.get(f"/projects/{project_id}/boards", headers=hdr)
    assert any(b["tipo"] == "PO" for b in boards.json())
    # verify project status
    proj = await client.get(f"/projects/{project_id}", headers=hdr)
    assert proj.json()["status"] == "EM_PO"
