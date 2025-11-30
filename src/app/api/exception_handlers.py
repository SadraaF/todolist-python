"""Custom exception handlers for the FastAPI application."""

from fastapi import Request, status
from fastapi.responses import JSONResponse

from src.app.exceptions.base import (
    DuplicateProjectNameError,
    EntityDoesNotExistError,
    ValidationError,
)

async def validation_exception_handler(request: Request, exc: ValidationError):
    """Handles validation errors from the service layer."""
    status_code = status.HTTP_400_BAD_REQUEST
    if isinstance(exc, DuplicateProjectNameError):
        status_code = status.HTTP_409_CONFLICT

    return JSONResponse(
        status_code=status_code,
        content={"detail": str(exc)},
    )

async def entity_not_found_exception_handler(
    request: Request, exc: EntityDoesNotExistError
):
    """Handles entity not found errors from the service layer."""
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": str(exc)},
    )