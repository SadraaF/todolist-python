"""Main entry point for the ToDo List API."""

from fastapi import FastAPI

from src.app.api.exception_handlers import (
    entity_not_found_exception_handler,
    validation_exception_handler,
)
from src.app.api.routers import api_router
from src.app.exceptions.base import (
    EntityDoesNotExistError,
    ProjectLimitExceededError,  
    TaskLimitExceededError,
    ValidationError,
)

app = FastAPI(
    title="ToDo List API",
    description="A simple API to manage projects and tasks.",
    version="0.1.0",
)

app.add_exception_handler(ValidationError, validation_exception_handler)
app.add_exception_handler(EntityDoesNotExistError, entity_not_found_exception_handler)

app.add_exception_handler(ProjectLimitExceededError, validation_exception_handler)
app.add_exception_handler(TaskLimitExceededError, validation_exception_handler)

app.include_router(api_router, prefix="/api/v1")


@app.get("/", tags=["Root"])
def read_root():
    """A simple root endpoint to confirm the API is running."""
    return {"message": "Welcome to the ToDo List API!"}