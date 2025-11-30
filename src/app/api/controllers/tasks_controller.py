"""API controller for task-related endpoints."""

from collections.abc import Sequence

from fastapi import APIRouter, Depends, status

from src.app.api.dependencies import get_project_service
from src.app.api.schemas.task_schema import TaskCreate, TaskResponse
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