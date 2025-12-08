"""Main API router aggregator."""

from fastapi import APIRouter

from src.app.api.controllers import projects_controller, tasks_controller

api_router = APIRouter()

# Include project routes
api_router.include_router(projects_controller.router)

# Include task routes
api_router.include_router(tasks_controller.router)