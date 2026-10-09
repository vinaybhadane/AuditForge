from typing import List, Optional, Union

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """AuditForge Centralized Application Settings.
    
    Loads configuration from environment variables or .env files,
    validating types and providing secure, deterministic defaults for development.
    """
    model_config = SettingsConfigDict(
        env_file=(".env", ".env.local"),
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    # Application Basics
    APP_ENV: str = "development"
    APP_NAME: str = "AuditForge API"
    API_V1_PREFIX: str = "/api/v1"
    BACKEND_HOST: str = "127.0.0.1"
    BACKEND_PORT: int = 8000
    LOG_LEVEL: str = "INFO"
    REQUEST_ID_HEADER: str = "X-Request-ID"

    # CORS
    FRONTEND_ORIGINS: Union[List[str], str] = ["http://localhost:3000"]

    @field_validator("FRONTEND_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",") if origin.strip()]
        return v

    # Supabase & PostgreSQL Configuration
    SUPABASE_URL: Optional[str] = "https://YOUR_PROJECT.supabase.co"
    SUPABASE_ANON_KEY: Optional[str] = "YOUR_PUBLIC_ANON_KEY"
    SUPABASE_JWT_ISSUER: Optional[str] = "https://YOUR_PROJECT.supabase.co/auth/v1"
    SUPABASE_SERVICE_ROLE_KEY: Optional[str] = None
    DATABASE_URL: Optional[str] = "postgresql+psycopg://postgres:postgres@localhost:5432/auditforge"

    # Storage Buckets and Limits
    EVIDENCE_BUCKET: str = "auditforge-evidence"
    REPORTS_BUCKET: str = "auditforge-reports"
    SIGNED_URL_TTL_SECONDS: int = 300
    MAX_UPLOAD_BYTES: int = 20971520  # 20 MB
    MAX_PDF_PAGES: int = 100
    MAX_IMAGE_PIXELS: int = 40000000

    # AI Provider Configuration
    GOOGLE_GEMINI_API_KEY: Optional[str] = None
    GEMINI_MODEL_ID: Optional[str] = None
    AI_REQUEST_TIMEOUT_SECONDS: int = 60
    AI_MAX_RETRIES: int = 3
    AI_MAX_INPUT_BYTES: int = 15000000

    # OCR & Background Processing
    OCR_PROVIDER: str = "paddleocr"
    OCR_LANGUAGE: str = "en"
    PDF_TEXT_EXTRACTION_ENABLED: bool = True
    PROCESSING_WORKER_ENABLED: bool = True
    JOB_POLL_INTERVAL_SECONDS: int = 2
    JOB_MAX_ATTEMPTS: int = 4
    JOB_LEASE_SECONDS: int = 180

    # Rate Limiting
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_REQUESTS_PER_MINUTE: int = 120
    UPLOAD_RATE_LIMIT_PER_HOUR: int = 30
    AI_RATE_LIMIT_PER_HOUR: int = 30


settings = Settings()
