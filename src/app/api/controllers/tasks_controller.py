"""API controller for task-related endpoints."""

from fastapi import APIRouter, Depends, Response, status

from src.app.api.dependencies import get_project_service, get_task_service
from src.app.api.schemas.requests.task_schema import (
    TaskCreate,
    TaskStatusUpdate,
    TaskUpdate,
)
from src.app.api.schemas.responses.base import SuccessResponse
from src.app.api.schemas.responses.task_schema import TaskResponse
from src.app.services.project_service import ProjectService
from src.app.services.task_service import TaskService

router = APIRouter(prefix="/projects/{project_id}/tasks", tags=["Tasks"])


@router.get("", response_model=SuccessResponse[list[TaskResponse]])
async def list_tasks_for_project(
    project_id: int, project_service: ProjectService = Depends(get_project_service)
) -> dict:
    """Retrieve all tasks for a specific project.

    :param project_id: The ID of the project whose tasks are to be listed.
    :raises EntityDoesNotExistError: If the project does not exist (404).
    :param project_service: The project service dependency.
    :return: A success response containing a list of tasks for the project.
    """
    project = await project_service.find_project_by_id(project_id)
    return {"data": project.tasks}


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=SuccessResponse[TaskResponse],
)
async def create_task_for_project(
    project_id: int,
    task_in: TaskCreate,
    task_service: TaskService = Depends(get_task_service),
) -> dict:
    """Create a new task within a specific project.

    - The task title must be between 1 and 30 characters.

    :param project_id: The ID of the project to add the task to.
    :param task_in: The request body containing the new task's details.
    :raises EntityDoesNotExistError: If the project does not exist (404).
    :param task_service: The task service dependency.
    :return: A success response containing the newly created task.
    """

    task = await task_service.add_task_to_project(
        project_id=project_id,
        title=task_in.title,
        description=task_in.description,
        deadline=task_in.deadline,
    )
    return {"data": task}


@router.put("/{task_id}", response_model=SuccessResponse[TaskResponse])
async def update_task(
    project_id: int,
    task_id: int,
    task_in: TaskUpdate,
    task_service: TaskService = Depends(get_task_service),
) -> dict:
    """Update an existing task's details (full update).

    All fields (title, description, status, deadline) must be provided.

    :param project_id: The ID of the parent project.
    :param task_id: The ID of the task to update.
    :param task_in: The request body with the full new task details.
    :raises EntityDoesNotExistError: If the project or task does not exist (404).
    :param task_service: The task service dependency.
    :return: A success response containing the updated task.
    """

    task = await task_service.edit_task(
        project_id=project_id,
        task_id=task_id,
        new_title=task_in.title,
        new_description=task_in.description,
        new_status_str=task_in.status,
        new_deadline=task_in.deadline,
    )
    return {"data": task}


@router.patch("/{task_id}", response_model=SuccessResponse[TaskResponse])
async def update_task_status(
    project_id: int,
    task_id: int,
    task_in: TaskStatusUpdate,
    task_service: TaskService = Depends(get_task_service),
) -> dict:
    """Partially update a task to change its status.

    Valid statuses are 'todo', 'doing', or 'done'.

    :param project_id: The ID of the parent project.
    :param task_id: The ID of the task whose status is to be updated.
    :param task_in: The request body containing the new status.
    :raises EntityDoesNotExistError: If the project or task does not exist (404).
    :param task_service: The task service dependency.
    :return: A success response containing the updated task.
    """
    task = await task_service.change_task_status(
        project_id=project_id, task_id=task_id, new_status_str=task_in.status
    )
    return {"data": task}


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    project_id: int,
    task_id: int,
    task_service: TaskService = Depends(get_task_service),
) -> Response:
    """Delete a specific task from a project.

    :param project_id: The ID of the parent project.
    :param task_id: The ID of the task to delete.
    :raises EntityDoesNotExistError: If the project or task does not exist (404).
    :param task_service: The task service dependency.
    :return: An empty response with a 204 status code on success.
    """
    await task_service.delete_task(project_id=project_id, task_id=task_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)