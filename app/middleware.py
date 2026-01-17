"""
Exception Handlers and Custom Middleware
Maps to: Documentation - Error catalog
"""
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Handle validation errors
    Maps to: Documentation - Error catalog
    """
    logger.error(f"Validation error: {exc.errors()}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "Validation Error",
            "detail": exc.errors(),
            "status_code": status.HTTP_422_UNPROCESSABLE_ENTITY,
            "timestamp": datetime.utcnow().isoformat()
        }
    )


async def general_exception_handler(request: Request, exc: Exception):
    """
    Handle general exceptions
    Maps to: Requirements & Planning - Understand Constraints
    """
    logger.exception(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal Server Error",
            "detail": "An unexpected error occurred",
            "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "timestamp": datetime.utcnow().isoformat()
        }
    )
