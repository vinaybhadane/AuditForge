from fastapi import APIRouter

from app.api.v1.endpoints.health import router as health_router

api_v1_router = APIRouter()

# Mount health routes under /health
api_v1_router.include_router(health_router, prefix="/health")

# Future phase routers will be mounted here:
# api_v1_router.include_router(auth_router, prefix="/auth")
# api_v1_router.include_router(projects_router, prefix="/projects")
# api_v1_router.include_router(milestones_router, prefix="/milestones")
# api_v1_router.include_router(evidence_router, prefix="/evidence")
# api_v1_router.include_router(documents_router, prefix="/documents")
# api_v1_router.include_router(reconciliations_router, prefix="/reconciliations")
# api_v1_router.include_router(findings_router, prefix="/findings")
# api_v1_router.include_router(certificates_router, prefix="/certificates")
