import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_health_live_endpoint(client: AsyncClient):
    response = await client.get("/health/live")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "pass"
    assert "version" in data
    assert "timestamp" in data
    assert "checks" in data
    assert "process" in data["checks"]


@pytest.mark.asyncio
async def test_health_ready_endpoint(client: AsyncClient):
    response = await client.get("/health/ready")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] in ["pass", "warn"]
    assert "checks" in data
    assert "configuration" in data["checks"]


@pytest.mark.asyncio
async def test_api_v1_health_route(client: AsyncClient):
    response = await client.get("/api/v1/health/live")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "pass"


@pytest.mark.asyncio
async def test_request_id_correlation(client: AsyncClient):
    # Verify client-supplied request id is echoed back
    custom_id = "test-corr-12345"
    response = await client.get("/health/live", headers={"X-Request-ID": custom_id})
    assert response.status_code == 200
    assert response.headers.get("X-Request-ID") == custom_id


@pytest.mark.asyncio
async def test_standard_error_envelope_on_not_found(client: AsyncClient):
    response = await client.get("/api/v1/nonexistent-route")
    assert response.status_code == 404
    data = response.json()
    # Contract from docs/11_API_CONTRACTS.md
    assert "error" in data
    assert "code" in data["error"]
    assert "message" in data["error"]
    assert "request_id" in data["error"]
    assert "details" in data["error"]
