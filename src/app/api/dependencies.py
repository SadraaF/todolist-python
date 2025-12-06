"""Shared dependencies for API controllers."""

from fastapi import Depends
from sqlalchemy.orm import Session

from src.app.core.config import get_settings
from src.app.db.session import get_db
from src.app.repositories.sqlalchemy_project_repository import \
    SqlAlchemyProjectRepository
from src.app.repositories.sqlalchemy_task_repository import \
    SqlAlchemyTaskRepository
from src.app.services.project_service import ProjectService
from src.app.services.task_service import TaskService


def get_project_service(db: Session = Depends(get_db)) -> ProjectService:
    """Dependency injector for the ProjectService."""
    settings = get_settings()
    repo = SqlAlchemyProjectRepository(session=db)
    return ProjectService(
        repo=repo,
        max_projects=settings.MAX_NUMBER_OF_PROJECT,
    )


def get_task_service(db: Session = Depends(get_db)) -> TaskService:
    """Dependency injector for the TaskService."""
    settings = get_settings()
    project_repo = SqlAlchemyProjectRepository(session=db)
    task_repo = SqlAlchemyTaskRepository(session=db)
    return TaskService(
        task_repo=task_repo,
        project_repo=project_repo,
        max_tasks=settings.MAX_NUMBER_OF_TASK,
    )