import uuid

import pytest
from httpx import AsyncClient

from tests.conftest import mint_jwt


@pytest.mark.asyncio
async def test_missing_auth_header(client: AsyncClient):
    response = await client.get("/api/v1/me")
    assert response.status_code == 401
    data = response.json()
    assert data["error"]["code"] == "AUTH_REQUIRED"


@pytest.mark.asyncio
async def test_invalid_jwt_signature(client: AsyncClient):
    bad_token = mint_jwt(str(uuid.uuid4()), secret="wrong-secret-key-12345678901234567890")
    response = await client.get("/api/v1/me", headers={"Authorization": f"Bearer {bad_token}"})
    assert response.status_code == 401
    data = response.json()
    assert data["error"]["code"] == "AUTH_REQUIRED"


@pytest.mark.asyncio
async def test_expired_jwt(client: AsyncClient):
    expired_token = mint_jwt(str(uuid.uuid4()), expires_in_seconds=-10)
    response = await client.get("/api/v1/me", headers={"Authorization": f"Bearer {expired_token}"})
    assert response.status_code == 401
    data = response.json()
    assert data["error"]["code"] == "AUTH_REQUIRED"


@pytest.mark.asyncio
async def test_authenticated_user_context(client: AsyncClient, test_data: dict):
    response = await client.get(
        "/api/v1/me",
        headers={"Authorization": f"Bearer {test_data['token_a']}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["user"]["id"] == str(test_data["user_a_id"])
    assert len(data["organizations"]) == 1
    assert data["organizations"][0]["role"] == "org_admin"


@pytest.mark.asyncio
async def test_cross_tenant_idor_concealment(client: AsyncClient, test_data: dict):
    # User A tries to access Project B from Organization B
    response = await client.get(
        f"/api/v1/projects/{test_data['project_b_id']}",
        headers={"Authorization": f"Bearer {test_data['token_a']}"},
    )
    # Must return 404 to avoid leaking existence of cross-tenant resource
    assert response.status_code == 404
    data = response.json()
    assert data["error"]["code"] == "RESOURCE_NOT_FOUND"


@pytest.mark.asyncio
async def test_viewer_role_write_forbidden(client: AsyncClient, test_data: dict):
    # Viewer tries to create a milestone on Project A
    payload = {
        "code": "MS-UNAUTHORIZED",
        "name": "Unauthorized Milestone",
    }
    response = await client.post(
        f"/api/v1/projects/{test_data['project_a_id']}/milestones",
        json=payload,
        headers={"Authorization": f"Bearer {test_data['token_viewer']}"},
    )
    assert response.status_code == 403
    data = response.json()
    assert data["error"]["code"] == "FORBIDDEN"
