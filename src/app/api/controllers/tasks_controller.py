"""API controller for task-related endpoints."""

from collections.abc import Sequence

from fastapi import APIRouter, Depends, Response, status
from src.app.api.dependencies import get_project_service, get_task_service
from src.app.api.schemas.task_schema import (
    TaskCreate,
    TaskResponse,
    TaskStatusUpdate,
    TaskUpdate,
)
from src.app.services.project_service import ProjectService
from src.app.services.task_service import TaskService

router = APIRouter(prefix="/projects/{project_id}/tasks", tags=["Tasks"])


@router.get("", response_model=list[TaskResponse])
def list_tasks_for_project(
    project_id: int, project_service: ProjectService = Depends(get_project_service)
) -> Sequence[TaskResponse]:
    """
    Retrieve all tasks for a specific project.

    - A 404 Not Found error is returned if the project does not exist.
    """
    project = project_service.find_project_by_id(project_id)
    return project.tasks


@router.post("", status_code=status.HTTP_201_CREATED, response_model=TaskResponse)
def create_task_for_project(
    project_id: int,
    task_in: TaskCreate,
    task_service: TaskService = Depends(get_task_service),
) -> TaskResponse:
    """
    Create a new task within a specific project.

    - The task title must be between 1 and 30 characters.
    - A 404 Not Found error is returned if the project does not exist.
    """
    deadline_str = task_in.deadline.strftime("%Y-%m-%d") if task_in.deadline else None

    task = task_service.add_task_to_project(
        project_id=project_id,
        title=task_in.title,
        description=task_in.description,
        deadline_str=deadline_str,
    )
    return task


@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    project_id: int,
    task_id: int,
    task_in: TaskUpdate,
    task_service: TaskService = Depends(get_task_service),
) -> TaskResponse:
    """
    Update an existing task's details.

    - All fields (title, description, status, deadline) must be provided in the request.
    - A 404 Not Found error is returned if the project or task does not exist.
    """
    deadline_str = task_in.deadline.strftime("%Y-%m-%d") if task_in.deadline else None
    task = task_service.edit_task(
        project_id=project_id,
        task_id=task_id,
        new_title=task_in.title,
        new_description=task_in.description,
        new_status_str=task_in.status,
        new_deadline_str=deadline_str,
    )
    return task


@router.patch("/{task_id}", response_model=TaskResponse)
def update_task_status(
    project_id: int,
    task_id: int,
    task_in: TaskStatusUpdate,
    task_service: TaskService = Depends(get_task_service),
) -> TaskResponse:
    """
    Partially update a task to change its status.

    - Valid statuses are 'todo', 'doing', or 'done'.
    - A 404 Not Found error is returned if the project or task does not exist.
    """
    task = task_service.change_task_status(
        project_id=project_id, task_id=task_id, new_status_str=task_in.status
    )
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    project_id: int,
    task_id: int,
    task_service: TaskService = Depends(get_task_service),
) -> Response:
    """
    Delete a specific task from a project.

    - Returns a 204 No Content response on success.
    - A 404 Not Found error is returned if the project or task does not exist.
    """
    task_service.delete_task(project_id=project_id, task_id=task_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)