"""Shared dependencies for API controllers."""

from sqlalchemy.orm import Session
from fastapi import Depends

from src.app.core.config import get_settings
from src.app.db.session import get_db
from src.app.repositories.sqlalchemy_repository import SqlAlchemyProjectRepository
from src.app.services.project_service import ProjectService


def get_project_service(db: Session = Depends(get_db)) -> ProjectService:
    """Dependency injector for the ProjectService."""
    settings = get_settings()
    repo = SqlAlchemyProjectRepository(session=db)
    return ProjectService(
        repo=repo,
        max_projects=settings.MAX_NUMBER_OF_PROJECT,
        max_tasks=settings.MAX_NUMBER_OF_TASK,
    )