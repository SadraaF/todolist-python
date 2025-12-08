"""Custom exception handlers for the FastAPI application.

These handlers catch specific custom exceptions raised from the service layer
and convert them into standardized JSON error responses.
"""

from fastapi import Request, status
from fastapi.responses import JSONResponse

from src.app.api.schemas.responses.base import ErrorResponse
from src.app.exceptions.base import (
    DuplicateProjectNameError,
    EntityDoesNotExistError,
    ProjectLimitExceededError,
    TaskLimitExceededError,
    ValidationError,
)


async def validation_exception_handler(request: Request, exc: ValidationError) -> JSONResponse:
    """Handle business logic validation errors.

    Maps different validation errors to appropriate HTTP status codes.

    :param request: The incoming FastAPI request object.
    :param exc: The caught ValidationError instance.
    :return: A standardized JSONResponse for the error.
    """
    status_code = status.HTTP_400_BAD_REQUEST
    if isinstance(exc, DuplicateProjectNameError):
        status_code = status.HTTP_409_CONFLICT
    if isinstance(exc, (ProjectLimitExceededError, TaskLimitExceededError)):
        status_code = status.HTTP_400_BAD_REQUEST

    error_response = ErrorResponse(message=str(exc), code=status_code)
    return JSONResponse(
        status_code=status_code,
        content=error_response.dict(),
    )


async def entity_not_found_exception_handler(
    request: Request, exc: EntityDoesNotExistError
) -> JSONResponse:
    """Handle errors for entities that do not exist in the database.

    Responds with a 404 Not Found status code.

    :param request: The incoming FastAPI request object.
    :param exc: The caught EntityDoesNotExistError instance.
    :return: A standardized JSONResponse for the error.
    """
    status_code = status.HTTP_404_NOT_FOUND
    error_response = ErrorResponse(message=str(exc), code=status_code)
    return JSONResponse(
        status_code=status_code,
        content=error_response.dict(),
    )