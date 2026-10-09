import uuid
from datetime import datetime, timedelta, timezone
from typing import AsyncGenerator, Generator

import jwt
import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.config import settings
from app.db.base import Base
from app.db.models.auth import (
    Organization,
    OrganizationMembership,
    OrgRole,
    UserProfile,
)
from app.db.models.projects import Milestone, Project
from app.db.session import get_db
from app.main import app

# Shared in-memory SQLite engine for tests
test_engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture(autouse=True)
def setup_test_database():
    """Create all tables before each test and drop them after."""
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture
def db() -> Generator[Session, None, None]:
    """Database session fixture using in-memory SQLite."""
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
async def client(db: Session) -> AsyncGenerator[AsyncClient, None]:
    """Async test client with get_db dependency overridden."""
    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://testserver",
    ) as ac:
        yield ac
    app.dependency_overrides.clear()


def mint_jwt(
    sub: str,
    email: str = "user@example.com",
    role: str = "authenticated",
    expires_in_seconds: int = 3600,
    secret: str = None,
) -> str:
    """Helper to mint cryptographically valid test JWTs."""
    now = datetime.now(timezone.utc)
    payload = {
        "sub": str(sub),
        "email": email,
        "aud": "authenticated",
        "role": role,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(seconds=expires_in_seconds)).timestamp()),
        "user_metadata": {"full_name": "Test User"},
    }
    return jwt.encode(payload, secret or settings.SUPABASE_JWT_SECRET, algorithm="HS256")


@pytest.fixture
def test_data(db: Session):
    """Seed two distinct organizations and users for tenant isolation tests."""
    user_a_id = uuid.uuid4()
    user_b_id = uuid.uuid4()
    viewer_id = uuid.uuid4()

    # User Profiles
    user_a = UserProfile(id=user_a_id, display_name="Admin User A", email="admin_a@auditforge.test")
    user_b = UserProfile(id=user_b_id, display_name="Admin User B", email="admin_b@auditforge.test")
    viewer_a = UserProfile(id=viewer_id, display_name="Viewer User A", email="viewer_a@auditforge.test")
    db.add_all([user_a, user_b, viewer_a])
    db.flush()

    # Organizations
    org_a = Organization(id=uuid.uuid4(), name="Acme Construction A", slug="acme-a", created_by=user_a_id)
    org_b = Organization(id=uuid.uuid4(), name="Beta Construction B", slug="beta-b", created_by=user_b_id)
    db.add_all([org_a, org_b])
    db.flush()

    # Memberships
    db.add(OrganizationMembership(organization_id=org_a.id, user_id=user_a_id, role=OrgRole.ORG_ADMIN.value))
    db.add(OrganizationMembership(organization_id=org_a.id, user_id=viewer_id, role=OrgRole.VIEWER.value))
    db.add(OrganizationMembership(organization_id=org_b.id, user_id=user_b_id, role=OrgRole.ORG_ADMIN.value))
    db.flush()

    # Projects
    proj_a = Project(
        id=uuid.uuid4(),
        organization_id=org_a.id,
        name="Tower Alpha Project",
        project_code="PRJ-A",
        timezone="Asia/Kolkata",
        currency_code="INR",
        created_by=user_a_id,
    )
    proj_b = Project(
        id=uuid.uuid4(),
        organization_id=org_b.id,
        name="Tower Beta Project",
        project_code="PRJ-B",
        timezone="Asia/Kolkata",
        currency_code="INR",
        created_by=user_b_id,
    )
    db.add_all([proj_a, proj_b])
    db.flush()

    # Milestone in Project A
    ms_a = Milestone(
        id=uuid.uuid4(),
        project_id=proj_a.id,
        code="MS-01-FOUNDATION",
        name="Foundation Pouring",
        status="in_progress",
    )
    db.add(ms_a)
    db.commit()

    return {
        "user_a_id": user_a_id,
        "token_a": mint_jwt(str(user_a_id), email=user_a.email),
        "user_b_id": user_b_id,
        "token_b": mint_jwt(str(user_b_id), email=user_b.email),
        "viewer_id": viewer_id,
        "token_viewer": mint_jwt(str(viewer_id), email=viewer_a.email),
        "org_a_id": org_a.id,
        "org_b_id": org_b.id,
        "project_a_id": proj_a.id,
        "project_b_id": proj_b.id,
        "milestone_a_id": ms_a.id,
    }
