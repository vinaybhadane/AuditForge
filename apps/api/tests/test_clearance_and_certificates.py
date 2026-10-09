import uuid

import pytest
from httpx import AsyncClient
from sqlalchemy.orm import Session

from app.db.models.evidence import EvidenceAsset


@pytest.mark.asyncio
async def test_clearance_eligibility_and_certificate_issuance(client: AsyncClient, test_data: dict, db: Session):
    project_id = test_data["project_a_id"]
    milestone_id = test_data["milestone_a_id"]
    token = test_data["token_a"]

    # 1. Eligibility Check (Initially blocked: no approved review decision)
    elig_res = await client.get(
        f"/api/v1/milestones/{milestone_id}/clearance-eligibility",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert elig_res.status_code == 200
    assert elig_res.json()["is_eligible"] is False
    assert len(elig_res.json()["blockers"]) >= 1

    # 2. Attempting to issue certificate while blocked MUST FAIL with 422 CLEARANCE_BLOCKED
    fake_decision_id = str(uuid.uuid4())
    bad_cert_res = await client.post(
        f"/api/v1/milestones/{milestone_id}/certificates",
        json={
            "review_decision_id": fake_decision_id,
            "report_format": "pdf",
            "idempotency_key": "cert-key-001",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert bad_cert_res.status_code == 422
    assert bad_cert_res.json()["error"]["code"] == "CLEARANCE_BLOCKED"

    # 3. Upload and verify required evidence
    ev = EvidenceAsset(
        organization_id=test_data["org_a_id"],
        project_id=project_id,
        milestone_id=milestone_id,
        uploader_id=test_data["user_a_id"],
        evidence_type="site_photo",
        ingestion_source="live_capture",
        original_filename="foundation_pour_verified.jpg",
        object_key=f"projects/{project_id}/evidence/verified_frame.jpg",
        media_type="image/jpeg",
        size_bytes=1024000,
        upload_status="verified",
    )
    db.add(ev)
    db.commit()

    # 4. Record approved human review decision
    dec_res = await client.post(
        f"/api/v1/milestones/{milestone_id}/review-decisions",
        json={
            "decision_type": "approve",
            "reason": "Live site inspection photos confirm foundation rebar and pour completion meeting specifications.",
            "criteria_version": 1,
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert dec_res.status_code == 201
    decision_id = dec_res.json()["id"]

    # 5. Re-check eligibility: Should now pass!
    elig_pass_res = await client.get(
        f"/api/v1/milestones/{milestone_id}/clearance-eligibility",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert elig_pass_res.status_code == 200
    assert elig_pass_res.json()["is_eligible"] is True

    # 6. Issue Clearance Certificate
    cert_res = await client.post(
        f"/api/v1/milestones/{milestone_id}/certificates",
        json={
            "review_decision_id": decision_id,
            "report_format": "pdf",
            "idempotency_key": "cert-key-002",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert cert_res.status_code == 201
    cert_data = cert_res.json()
    assert cert_data["status"] == "issued"
    assert "certificate_number" in cert_data
    assert "snapshot_hash" in cert_data
    cert_id = cert_data["id"]

    # 7. Get Certificate Download URL
    dl_res = await client.get(
        f"/api/v1/certificates/{cert_id}/download",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert dl_res.status_code == 200
    assert "download_url" in dl_res.json()

    # 8. Generate Evidence-Linked Audit Report
    rep_res = await client.post(
        f"/api/v1/projects/{project_id}/reports",
        json={"milestone_id": str(milestone_id)},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert rep_res.status_code == 200
    rep = rep_res.json()
    assert "extracted_facts" in rep
    assert "deterministic_calculations" in rep
    assert "ai_observations" in rep
    assert "unresolved_discrepancies" in rep
    assert "human_decisions" in rep
    assert len(rep["human_decisions"]) >= 1
