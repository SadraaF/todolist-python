"""API controller for project-related endpoints."""

from collections.abc import Sequence

from fastapi import APIRouter, Depends, Response, status
from src.app.api.schemas.requests.project_schema import (
    ProjectCreate,
    ProjectUpdate,
)
from src.app.api.schemas.responses.base import SuccessResponse
from src.app.api.schemas.responses.project_schema import ProjectResponse
from src.app.services.project_service import ProjectService
from src.app.api.dependencies import get_project_service

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.get("", response_model=SuccessResponse[list[ProjectResponse]])
def list_projects(
    service: ProjectService = Depends(get_project_service),
) -> Sequence[ProjectResponse]:
    """
    Retrieve a list of all projects.

    Returns a list of all projects in the system, sorted by their creation date.
    If no projects exist, an empty list is returned.
    """
    projects = service.get_all_projects()
    return {"data": projects}


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=SuccessResponse[ProjectResponse],
)
def create_project(
    project_in: ProjectCreate,
    service: ProjectService = Depends(get_project_service),
) -> ProjectResponse:
    """
    Create a new project.

    - A project name must be unique.
    - The name must be between 1 and 30 characters.
    - The description must be 150 characters or less.
    - Returns a 409 Conflict error if the project name already exists.
    """
    project = service.create_project(
        name=project_in.name, description=project_in.description
    )
    return {"data": project}


@router.get("/{project_id}", response_model=SuccessResponse[ProjectResponse])
def get_project(
    project_id: int, service: ProjectService = Depends(get_project_service)
) -> ProjectResponse:
    """
    Retrieve a single project by its ID.

    - project_id: The integer ID of the project to retrieve.
    - Returns a 404 Not Found error if the project does not exist.
    """
    project = service.find_project_by_id(project_id)
    return {"data": project}


@router.put("/{project_id}", response_model=SuccessResponse[ProjectResponse])
def update_project(
    project_id: int,
    project_in: ProjectUpdate,
    service: ProjectService = Depends(get_project_service),
) -> ProjectResponse:
    """
    Update an existing project's name and description.

    - The new name must not conflict with another existing project.
    - Returns a 404 Not Found error if the project does not exist.
    - Returns a 409 Conflict error if the new name is already in use.
    """
    project = service.edit_project(
        project_id=project_id,
        new_name=project_in.name,
        new_description=project_in.description,
    )
    return {"data": project}


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(
    project_id: int, service: ProjectService = Depends(get_project_service)
) -> Response:
    """
    Delete a project and all of its associated tasks.

    - This action performs a cascade delete on all tasks within the project.
    - Returns a 204 No Content response on success.
    - Returns a 404 Not Found error if the project does not exist.
    """
    service.delete_project(project_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)