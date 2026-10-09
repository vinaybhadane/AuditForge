import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_site_photo_file_upload_rejected_by_modality_policy(client: AsyncClient, test_data: dict):
    """CRITICAL DOMAIN RULE: Site photos must originate from verified live camera capture.
    Uploading pre-existing file/gallery photos is strictly forbidden and returns 422 INVALID_INGESTION_SOURCE.
    """
    payload = {
        "evidence_type": "site_photo",
        "ingestion_source": "file_upload",  # FORBIDDEN for site_photo!
        "filename": "old_gallery_photo.jpg",
        "declared_content_type": "image/jpeg",
        "size_bytes": 1048576,
        "milestone_id": str(test_data["milestone_a_id"]),
    }
    response = await client.post(
        f"/api/v1/projects/{test_data['project_a_id']}/evidence/uploads",
        json=payload,
        headers={"Authorization": f"Bearer {test_data['token_a']}"},
    )
    assert response.status_code == 422
    data = response.json()
    assert data["error"]["code"] == "INVALID_INGESTION_SOURCE"


@pytest.mark.asyncio
async def test_site_photo_live_capture_succeeds(client: AsyncClient, test_data: dict):
    """Live camera capture for site photo is permitted and returns upload instructions."""
    payload = {
        "evidence_type": "site_photo",
        "ingestion_source": "live_capture",  # ALLOWED
        "filename": "live_site_frame_01.jpg",
        "declared_content_type": "image/jpeg",
        "size_bytes": 1048576,
        "milestone_id": str(test_data["milestone_a_id"]),
        "capture_metadata": {
            "device_client": "AuditForge Web Camera Stream v1",
            "camera_facing": "environment",
            "geo_location": {
                "latitude": 19.0760,
                "longitude": 72.8777,
                "accuracy_meters": 10.0,
            },
        },
    }
    response = await client.post(
        f"/api/v1/projects/{test_data['project_a_id']}/evidence/uploads",
        json=payload,
        headers={"Authorization": f"Bearer {test_data['token_a']}"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["evidence_type"] == "site_photo"
    assert data["ingestion_source"] == "live_capture"
    assert "upload_instructions" in data
    assert "upload_url" in data["upload_instructions"]

    evidence_id = data["id"]

    # Complete upload
    complete_payload = {
        "sha256_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        "size_bytes": 1048576,
    }
    comp_res = await client.post(
        f"/api/v1/evidence/{evidence_id}/complete-upload",
        json=complete_payload,
        headers={"Authorization": f"Bearer {test_data['token_a']}"},
    )
    assert comp_res.status_code == 200
    assert comp_res.json()["upload_status"] == "verified"

    # Trigger processing
    proc_res = await client.post(
        f"/api/v1/evidence/{evidence_id}/process",
        json={"job_type": "visual_assessment"},
        headers={"Authorization": f"Bearer {test_data['token_a']}"},
    )
    assert proc_res.status_code == 202
    job_id = proc_res.json()["id"]

    # Check job status
    job_res = await client.get(
        f"/api/v1/jobs/{job_id}",
        headers={"Authorization": f"Bearer {test_data['token_a']}"},
    )
    assert job_res.status_code == 200
    assert job_res.json()["status"] == "succeeded"


@pytest.mark.asyncio
async def test_vendor_document_dual_modality_and_correction(client: AsyncClient, test_data: dict):
    """Vendor documents permit both digital file upload and live scan."""
    payload = {
        "evidence_type": "delivery_challan",
        "ingestion_source": "file_upload",  # ALLOWED for documents
        "filename": "challan_088.pdf",
        "declared_content_type": "application/pdf",
        "size_bytes": 204800,
    }
    response = await client.post(
        f"/api/v1/projects/{test_data['project_a_id']}/evidence/uploads",
        json=payload,
        headers={"Authorization": f"Bearer {test_data['token_a']}"},
    )
    assert response.status_code == 201
    evidence_id = response.json()["id"]

    # Complete upload
    await client.post(
        f"/api/v1/evidence/{evidence_id}/complete-upload",
        json={
            "sha256_hash": "a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2",
            "size_bytes": 204800,
        },
        headers={"Authorization": f"Bearer {test_data['token_a']}"},
    )

    # Process document extraction
    proc_res = await client.post(
        f"/api/v1/evidence/{evidence_id}/process",
        json={"job_type": "document_extraction"},
        headers={"Authorization": f"Bearer {test_data['token_a']}"},
    )
    assert proc_res.status_code == 202

    # Verify document record created
    docs_res = await client.get(
        f"/api/v1/projects/{test_data['project_a_id']}/documents",
        headers={"Authorization": f"Bearer {test_data['token_a']}"},
    )
    assert docs_res.status_code == 200
    docs = docs_res.json()
    assert len(docs) >= 1
    doc_id = docs[0]["id"]

    # Record human field correction
    corr_res = await client.post(
        f"/api/v1/documents/{doc_id}/fields/quantity/corrections",
        json={
            "normalized_value": "520",
            "correction_reason": "Typo in OCR extraction, challan indicates 520 bags",
        },
        headers={"Authorization": f"Bearer {test_data['token_a']}"},
    )
    assert corr_res.status_code == 201
    corr_data = corr_res.json()
    assert corr_data["version"] == 2
    assert corr_data["review_status"] == "corrected"
