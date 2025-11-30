"""API controller for task-related endpoints."""

from collections.abc import Sequence

from fastapi import APIRouter, Depends, Response, status 
from src.app.api.dependencies import get_project_service
from src.app.api.schemas.task_schema import (
    TaskCreate,
    TaskResponse,
    TaskStatusUpdate, 
    TaskUpdate       
)
from src.app.services.project_service import ProjectService

router = APIRouter(prefix="/projects/{project_id}/tasks", tags=["Tasks"])


@router.get("", response_model=list[TaskResponse])
def list_tasks_for_project(
    project_id: int, service: ProjectService = Depends(get_project_service)
) -> Sequence[TaskResponse]:
    """Retrieve all tasks for a specific project."""
    project = service.find_project_by_id(project_id)
    return project.tasks


@router.post("", status_code=status.HTTP_201_CREATED, response_model=TaskResponse)
def create_task_for_project(
    project_id: int,
    task_in: TaskCreate,
    service: ProjectService = Depends(get_project_service),
) -> TaskResponse:
    """Create a new task within a specific project."""
    deadline_str = task_in.deadline.strftime("%Y-%m-%d") if task_in.deadline else None

    task = service.add_task_to_project(
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
    service: ProjectService = Depends(get_project_service),
) -> TaskResponse:
    """Update an existing task."""
    deadline_str = task_in.deadline.strftime("%Y-%m-%d") if task_in.deadline else None
    task = service.edit_task(
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
    service: ProjectService = Depends(get_project_service),
) -> TaskResponse:
    """Update the status of an existing task."""
    task = service.change_task_status(
        project_id=project_id, task_id=task_id, new_status_str=task_in.status
    )
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    project_id: int,
    task_id: int,
    service: ProjectService = Depends(get_project_service),
) -> Response:
    """Delete a task."""
    service.delete_task(project_id=project_id, task_id=task_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)