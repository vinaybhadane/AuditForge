import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.security import AuthenticatedUser, get_current_user, verify_project_access
from app.db.session import get_db
from app.schemas.milestones import (
    AcceptanceCriterionCreate,
    AcceptanceCriterionResponse,
    CertificateIssueRequest,
    CertificateResponse,
    ClearanceEligibilityResponse,
    MilestoneCreate,
    MilestoneResponse,
    MilestoneUpdate,
    ReviewDecisionCreate,
    ReviewDecisionResponse,
)
from app.services.milestone_service import MilestoneService
from app.services.review_service import ReviewService

router = APIRouter(tags=["Milestones, Criteria, Decisions & Certificates"])


@router.get(
    "/projects/{project_id}/milestones",
    response_model=List[MilestoneResponse],
    status_code=status.HTTP_200_OK,
    summary="List Milestones",
)
async def list_milestones(
    project_id: uuid.UUID,
    user: AuthenticatedUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> List[MilestoneResponse]:
    await verify_project_access(project_id, user, db)
    milestones = MilestoneService.list_milestones(db, project_id)
    return [MilestoneResponse.model_validate(m) for m in milestones]


@router.post(
    "/projects/{project_id}/milestones",
    response_model=MilestoneResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create Milestone",
)
async def create_milestone(
    project_id: uuid.UUID,
    data: MilestoneCreate,
    user: AuthenticatedUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> MilestoneResponse:
    await verify_project_access(project_id, user, db, require_write=True)
    m = MilestoneService.create_milestone(db, project_id, data)
    return MilestoneResponse.model_validate(m)


@router.get(
    "/milestones/{milestone_id}",
    response_model=MilestoneResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Milestone Details",
)
async def get_milestone(
    milestone_id: uuid.UUID,
    user: AuthenticatedUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> MilestoneResponse:
    m = MilestoneService.get_milestone(db, milestone_id)
    await verify_project_access(m.project_id, user, db)
    return MilestoneResponse.model_validate(m)


@router.patch(
    "/milestones/{milestone_id}",
    response_model=MilestoneResponse,
    status_code=status.HTTP_200_OK,
    summary="Update Milestone",
)
async def update_milestone(
    milestone_id: uuid.UUID,
    data: MilestoneUpdate,
    user: AuthenticatedUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> MilestoneResponse:
    m = MilestoneService.get_milestone(db, milestone_id)
    await verify_project_access(m.project_id, user, db, require_write=True)
    if data.name:
        m.name = data.name
    if data.description:
        m.description = data.description
    if data.status:
        m.status = data.status
    if data.planned_start_date:
        m.planned_start_date = data.planned_start_date
    if data.planned_end_date:
        m.planned_end_date = data.planned_end_date
    db.commit()
    db.refresh(m)
    return MilestoneResponse.model_validate(m)


@router.post(
    "/milestones/{milestone_id}/criteria",
    response_model=AcceptanceCriterionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Add Acceptance Criterion",
)
async def add_criterion(
    milestone_id: uuid.UUID,
    data: AcceptanceCriterionCreate,
    user: AuthenticatedUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> AcceptanceCriterionResponse:
    m = MilestoneService.get_milestone(db, milestone_id)
    await verify_project_access(m.project_id, user, db, require_write=True)
    criterion = MilestoneService.add_criterion(db, milestone_id, data, user.id)
    return AcceptanceCriterionResponse.model_validate(criterion)


@router.post(
    "/milestones/{milestone_id}/review-decisions",
    response_model=ReviewDecisionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Record Human Review Decision",
)
async def record_review_decision(
    milestone_id: uuid.UUID,
    data: ReviewDecisionCreate,
    user: AuthenticatedUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ReviewDecisionResponse:
    m = MilestoneService.get_milestone(db, milestone_id)
    # Auditor or Project Manager required for review decisions
    await verify_project_access(m.project_id, user, db, allowed_roles={"project_auditor", "project_manager", "org_admin"})
    decision = ReviewService.record_decision(db, milestone_id, user.id, data)
    return ReviewDecisionResponse.model_validate(decision)


@router.get(
    "/milestones/{milestone_id}/clearance-eligibility",
    response_model=ClearanceEligibilityResponse,
    status_code=status.HTTP_200_OK,
    summary="Check Milestone Clearance Eligibility",
)
async def check_clearance_eligibility(
    milestone_id: uuid.UUID,
    user: AuthenticatedUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ClearanceEligibilityResponse:
    m = MilestoneService.get_milestone(db, milestone_id)
    await verify_project_access(m.project_id, user, db)
    return ReviewService.check_eligibility(db, milestone_id)


@router.post(
    "/milestones/{milestone_id}/certificates",
    response_model=CertificateResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Issue Clearance Certificate",
)
async def issue_clearance_certificate(
    milestone_id: uuid.UUID,
    data: CertificateIssueRequest,
    user: AuthenticatedUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> CertificateResponse:
    m = MilestoneService.get_milestone(db, milestone_id)
    # Only designated auditor or org admin can issue certificate
    await verify_project_access(m.project_id, user, db, allowed_roles={"project_auditor", "org_admin"})
    cert = ReviewService.issue_certificate(db, milestone_id, user.id, data)
    return CertificateResponse.model_validate(cert)
