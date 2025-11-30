"""Custom exception handlers for the FastAPI application."""

from fastapi import Request, status
from fastapi.responses import JSONResponse

from src.app.exceptions.base import DuplicateProjectNameError, ValidationError

async def validation_exception_handler(request: Request, exc: ValidationError):
    """Handles validation errors from the service layer."""
    status_code = status.HTTP_400_BAD_REQUEST
    if isinstance(exc, DuplicateProjectNameError):
        status_code = status.HTTP_409_CONFLICT

    return JSONResponse(
        status_code=status_code,
        content={"detail": str(exc)},
    )