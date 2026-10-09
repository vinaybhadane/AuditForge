from decimal import Decimal

import pytest
from httpx import AsyncClient
from sqlalchemy.orm import Session

from app.db.models.projects import BOQItem


@pytest.mark.asyncio
async def test_material_reconciliation_and_excess_issue_detection(client: AsyncClient, test_data: dict, db: Session):
    project_id = test_data["project_a_id"]
    token = test_data["token_a"]

    # 1. Add BOQ Item to Project A
    boq = BOQItem(
        project_id=project_id,
        item_code="BOQ-CEMENT-01",
        description="Structural Grade Cement",
        material_code="CEMENT_OPC_53",
        planned_quantity=Decimal("100.00"),
        unit="bags",
        approved_wastage_rate=Decimal("0.05"),  # 5% allowance -> 105 bags max allowed
    )
    db.add(boq)
    db.commit()

    # 2. Record Stock Movements (Receipt of 200 bags, Issue of 150 bags -> exceeds 105 allowed!)
    await client.post(
        f"/api/v1/projects/{project_id}/inventory/movements",
        json={
            "material_code": "CEMENT_OPC_53",
            "movement_type": "receipt",
            "quantity": 200.0,
            "unit": "bags",
            "effective_date": "2026-10-01",
            "source_reference": "GRN-001",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    await client.post(
        f"/api/v1/projects/{project_id}/inventory/movements",
        json={
            "material_code": "CEMENT_OPC_53",
            "movement_type": "issue",
            "quantity": 150.0,
            "unit": "bags",
            "effective_date": "2026-10-05",
            "source_reference": "ISSUE-001",
        },
        headers={"Authorization": f"Bearer {token}"},
    )

    # 3. Start Reconciliation Run
    recon_res = await client.post(
        f"/api/v1/projects/{project_id}/reconciliations",
        json={
            "period_start": "2026-10-01T00:00:00Z",
            "period_end": "2026-10-10T23:59:59Z",
            "idempotency_key": "test-recon-run-001",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert recon_res.status_code == 202
    run_id = recon_res.json()["id"]

    # 4. Fetch Details and Verify Calculation Lines
    detail_res = await client.get(
        f"/api/v1/reconciliations/{run_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert detail_res.status_code == 200
    details = detail_res.json()
    assert details["run"]["status"] == "completed"

    # Line for REC-005 should flag discrepancy (150 issued vs 105 allowed)
    rec005_lines = [line for line in details["lines"] if line["rule_code"] == "REC-005"]
    assert len(rec005_lines) == 1

    assert rec005_lines[0]["status"] == "discrepancy"

    # 5. Fetch Findings and Verify Anomaly Created
    findings_res = await client.get(
        f"/api/v1/projects/{project_id}/findings",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert findings_res.status_code == 200
    findings = findings_res.json()["items"]
    assert len(findings) >= 1

    finding = findings[0]
    assert finding["rule_code"] == "AN-006"
    assert finding["severity"] in ["high", "medium"]

    # 6. Record Reviewer Disposition on Finding
    disp_res = await client.patch(
        f"/api/v1/findings/{finding['id']}/disposition",
        json={
            "status": "resolved",
            "resolution_notes": "Supervisor verified 45 bags issued for foundation extra depth under change order.",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert disp_res.status_code == 200
    assert disp_res.json()["status"] == "resolved"
