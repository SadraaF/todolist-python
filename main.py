"""Main entry point for the ToDo List API."""

from fastapi import FastAPI

from src.app.api.controllers import projects_controller

app = FastAPI(
    title="ToDo List API",
    description="A simple API to manage projects and tasks.",
    version="0.1.0",
)


app.include_router(projects_controller.router, prefix="/api/v1")

@app.get("/", tags=["Root"])
def read_root():
    """A simple root endpoint to confirm the API is running."""
    return {"message": "Welcome to the ToDo List API!"}