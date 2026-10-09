import uuid

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.security import AuthenticatedUser, get_current_user, verify_project_access
from app.db.session import get_db
from app.schemas.projects import ProjectCreate, ProjectListResponse, ProjectResponse, ProjectUpdate
from app.services.project_service import ProjectService

router = APIRouter(tags=["Projects"])


@router.get(
    "/projects",
    response_model=ProjectListResponse,
    status_code=status.HTTP_200_OK,
    summary="List Accessible Projects",
)
async def list_projects(
    user: AuthenticatedUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ProjectListResponse:
    projects = ProjectService.list_user_projects(db, user.id)
    items = [ProjectResponse.model_validate(p) for p in projects]
    return ProjectListResponse(items=items, total=len(items))


@router.post(
    "/projects",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create Project",
)
async def create_project(
    data: ProjectCreate,
    user: AuthenticatedUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ProjectResponse:
    project = ProjectService.create_project(db, data, user.id)
    return ProjectResponse.model_validate(project)


@router.get(
    "/projects/{project_id}",
    response_model=ProjectResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Project Detail",
)
async def get_project(
    project_id: uuid.UUID,
    user: AuthenticatedUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ProjectResponse:
    ctx = await verify_project_access(project_id, user, db)
    return ProjectResponse.model_validate(ctx.project)


@router.patch(
    "/projects/{project_id}",
    response_model=ProjectResponse,
    status_code=status.HTTP_200_OK,
    summary="Update Project",
)
async def update_project(
    project_id: uuid.UUID,
    data: ProjectUpdate,
    user: AuthenticatedUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ProjectResponse:
    ctx = await verify_project_access(project_id, user, db, require_write=True)
    p = ctx.project
    if data.name:
        p.name = data.name
    if data.description:
        p.description = data.description
    if data.timezone:
        p.timezone = data.timezone
    if data.currency_code:
        p.currency_code = data.currency_code
    if data.status:
        p.status = data.status
    if data.planned_start_date:
        p.planned_start_date = data.planned_start_date
    if data.planned_end_date:
        p.planned_end_date = data.planned_end_date
    db.commit()
    db.refresh(p)
    return ProjectResponse.model_validate(p)
