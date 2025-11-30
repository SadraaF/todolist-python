"""API controller for project-related endpoints."""

from collections.abc import Sequence

from fastapi import APIRouter, Depends, Response, status 
from src.app.api.schemas.project_schema import (
    ProjectCreate,
    ProjectResponse,
    ProjectUpdate
)

from src.app.core.config import get_settings
from src.app.db.session import get_db
from src.app.repositories.sqlalchemy_repository import SqlAlchemyProjectRepository
from src.app.services.project_service import ProjectService
from src.app.api.dependencies import get_project_service
from sqlalchemy.orm import Session


router = APIRouter(prefix="/projects", tags=["Projects"])


@router.get("", response_model=list[ProjectResponse])
def list_projects(
    service: ProjectService = Depends(get_project_service),
) -> Sequence[ProjectResponse]:
    """Retrieve a list of all projects."""
    projects = service.get_all_projects()
    return projects

@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=ProjectResponse
)
def create_project(
    project_in: ProjectCreate,
    service: ProjectService = Depends(get_project_service),
) -> ProjectResponse:
    """Create a new project."""
    project = service.create_project(
        name=project_in.name, description=project_in.description
    )
    return project

@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(
    project_id: int, service: ProjectService = Depends(get_project_service)
) -> ProjectResponse:
    """Retrieve a single project by its ID."""
    project = service.find_project_by_id(project_id)
    return project

@router.put("/{project_id}", response_model=ProjectResponse)
def update_project(
    project_id: int,
    project_in: ProjectUpdate,
    service: ProjectService = Depends(get_project_service),
) -> ProjectResponse:
    """Update an existing project."""
    project = service.edit_project(
        project_id=project_id,
        new_name=project_in.name,
        new_description=project_in.description,
    )
    return project

@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(
    project_id: int, service: ProjectService = Depends(get_project_service)
) -> Response:
    """Delete a project."""
    service.delete_project(project_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)