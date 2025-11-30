"""Main entry point for the ToDo List API."""

from fastapi import FastAPI
from src.app.api.exception_handlers import validation_exception_handler
from src.app.api.exception_handlers import (
    entity_not_found_exception_handler,  
    validation_exception_handler,
)
from src.app.exceptions.base import (
    EntityDoesNotExistError,  
    ValidationError,
)
from src.app.api.controllers import projects_controller

app = FastAPI(
    title="ToDo List API",
    description="A simple API to manage projects and tasks.",
    version="0.1.0",
)

app.add_exception_handler(ValidationError, validation_exception_handler)
app.add_exception_handler(EntityDoesNotExistError, entity_not_found_exception_handler)

app.include_router(projects_controller.router, prefix="/api/v1")

@app.get("/", tags=["Root"])
def read_root():
    """A simple root endpoint to confirm the API is running."""
    return {"message": "Welcome to the ToDo List API!"}