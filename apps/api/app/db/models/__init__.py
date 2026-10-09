"""SQLAlchemy models package.

Canonical models to be implemented in Phase 02/03 per docs/06_DATABASE_SCHEMA.md:
- user_profiles, organizations, organization_memberships, project_memberships
- projects, project_baseline_versions, milestones, acceptance_criteria
- units_of_measure, materials, material_aliases, boq_items, vendors
- evidence_assets, evidence_processing_jobs, ai_observations, documents, extracted_field_versions
- purchase_orders, delivery_challans, goods_receipts, stock_movements
- reconciliation_runs, reconciliation_lines, anomaly_findings, investigations
- review_decisions, clearance_certificates, audit_events
"""

from app.db.base import Base

__all__ = ["Base"]
