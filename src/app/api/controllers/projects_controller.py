"""API controller for project-related endpoints."""

from fastapi import APIRouter, Depends, Response, status

from src.app.api.dependencies import get_project_service
from src.app.api.schemas.requests.project_schema import (
    ProjectCreate,
    ProjectUpdate,
)
from src.app.api.schemas.responses.base import SuccessResponse
from src.app.api.schemas.responses.project_schema import ProjectResponse
from src.app.services.project_service import ProjectService

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.get("", response_model=SuccessResponse[list[ProjectResponse]])
async def list_projects(
    service: ProjectService = Depends(get_project_service),
) -> dict:
    """Retrieve a list of all projects.

    Returns a list of all projects in the system, sorted by their creation date.
    If no projects exist, an empty list is returned.

    :param service: The project service dependency.
    :return: A success response containing a list of projects.
    """
    projects = await service.get_all_projects()
    return {"data": projects}


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=SuccessResponse[ProjectResponse],
)
async def create_project(
    project_in: ProjectCreate,
    service: ProjectService = Depends(get_project_service),
) -> dict:
    """Create a new project.

    - A project name must be unique.
    - The name must be between 1 and 30 characters.
    - The description must be 150 characters or less.
    - Returns a 409 Conflict error if the project name already exists.

    :param project_in: The request body containing project details.
    :param service: The project service dependency.
    :return: A success response containing the newly created project.
    """
    project = await service.create_project(
        name=project_in.name, description=project_in.description
    )
    return {"data": project}


@router.get("/{project_id}", response_model=SuccessResponse[ProjectResponse])
async def get_project(
    project_id: int, service: ProjectService = Depends(get_project_service)
) -> dict:
    """Retrieve a single project by its ID.

    :param project_id: The integer ID of the project to retrieve.
    :raises EntityDoesNotExistError: If the project does not exist (404).
    :param service: The project service dependency.
    :return: A success response containing the requested project.
    """
    project = await service.find_project_by_id(project_id)
    return {"data": project}


@router.put("/{project_id}", response_model=SuccessResponse[ProjectResponse])
async def update_project(
    project_id: int,
    project_in: ProjectUpdate,
    service: ProjectService = Depends(get_project_service),
) -> dict:
    """Update an existing project's name and description.

    - The new name must not conflict with another existing project.

    :param project_id: The ID of the project to update.
    :param project_in: The request body with the new project details.
    :raises EntityDoesNotExistError: If the project does not exist (404).
    :raises DuplicateProjectNameError: If the new name is already in use (409).
    :param service: The project service dependency.
    :return: A success response containing the updated project.
    """
    project = await service.edit_project(
        project_id=project_id,
        new_name=project_in.name,
        new_description=project_in.description,
    )
    return {"data": project}


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    project_id: int, service: ProjectService = Depends(get_project_service)
) -> Response:
    """Delete a project and all of its associated tasks.

    This action performs a cascade delete on all tasks within the project.

    :param project_id: The ID of the project to delete.
    :raises EntityDoesNotExistError: If the project does not exist (404).
    :param service: The project service dependency.
    :return: An empty response with a 204 status code on success.
    """
    await service.delete_project(project_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)