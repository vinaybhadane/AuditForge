import json
import logging
import sys
from contextvars import ContextVar
from datetime import datetime, timezone
from typing import Any, Dict

# Context variable for request correlation ID
request_id_ctx: ContextVar[str] = ContextVar("request_id", default="")

# Sensitive key names to redact
REDACTED_KEYS = {"password", "token", "authorization", "secret", "key", "signature", "signed_url"}


class JSONLogFormatter(logging.Formatter):
    """Structured JSON formatter with request ID correlation and sensitive data redaction."""

    def format(self, record: logging.LogRecord) -> str:
        log_obj: Dict[str, Any] = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        # Add correlation ID if present
        req_id = request_id_ctx.get()
        if req_id:
            log_obj["request_id"] = req_id

        # Add extra attributes
        if hasattr(record, "extra") and isinstance(record.extra, dict):
            for k, v in record.extra.items():
                if k.lower() in REDACTED_KEYS:
                    log_obj[k] = "[REDACTED]"
                else:
                    log_obj[k] = v

        if record.exc_info:
            log_obj["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_obj)


def setup_logging(log_level: str = "INFO") -> None:
    """Configure structured JSON logging for the application."""
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))

    # Clear existing handlers
    root_logger.handlers.clear()

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JSONLogFormatter())
    root_logger.addHandler(handler)


def get_logger(name: str) -> logging.Logger:
    """Get a named logger."""
    return logging.getLogger(name)
