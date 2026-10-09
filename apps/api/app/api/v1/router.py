from fastapi import APIRouter

from app.api.v1.endpoints.audit_events import router as audit_events_router
from app.api.v1.endpoints.audit_jobs import router as jobs_router
from app.api.v1.endpoints.auth import router as auth_router
from app.api.v1.endpoints.certificates import router as certificates_router
from app.api.v1.endpoints.documents import router as documents_router
from app.api.v1.endpoints.evidence import router as evidence_router
from app.api.v1.endpoints.findings import router as findings_router
from app.api.v1.endpoints.health import router as health_router
from app.api.v1.endpoints.inventory import router as inventory_router
from app.api.v1.endpoints.investigations import router as investigations_router
from app.api.v1.endpoints.milestones import router as milestones_router
from app.api.v1.endpoints.organizations import router as organizations_router
from app.api.v1.endpoints.projects import router as projects_router
from app.api.v1.endpoints.reconciliation import router as reconciliation_router
from app.api.v1.endpoints.reports import router as reports_router

api_v1_router = APIRouter()

# Mount all domain and infrastructure routers under /api/v1
api_v1_router.include_router(health_router, prefix="/health")
api_v1_router.include_router(auth_router)
api_v1_router.include_router(organizations_router)
api_v1_router.include_router(projects_router)
api_v1_router.include_router(milestones_router)
api_v1_router.include_router(evidence_router)
api_v1_router.include_router(jobs_router)
api_v1_router.include_router(documents_router)
api_v1_router.include_router(inventory_router)
api_v1_router.include_router(reconciliation_router)
api_v1_router.include_router(findings_router)
api_v1_router.include_router(investigations_router)
api_v1_router.include_router(certificates_router)
api_v1_router.include_router(reports_router)
api_v1_router.include_router(audit_events_router)
