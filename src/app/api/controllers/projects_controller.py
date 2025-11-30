"""API controller for project-related endpoints."""

from collections.abc import Sequence

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.app.api.schemas.project_schema import ProjectResponse
from src.app.core.config import get_settings
from src.app.db.session import get_db
from src.app.repositories.sqlalchemy_repository import SqlAlchemyProjectRepository
from src.app.services.project_service import ProjectService

router = APIRouter(prefix="/projects", tags=["Projects"])

def get_project_service(db: Session = Depends(get_db)) -> ProjectService:
    """Dependency injector for the ProjectService."""
    settings = get_settings()
    repo = SqlAlchemyProjectRepository(session=db)
    return ProjectService(
        repo=repo,
        max_projects=settings.MAX_NUMBER_OF_PROJECT,
        max_tasks=settings.MAX_NUMBER_OF_TASK,
    )

@router.get("", response_model=list[ProjectResponse])
def list_projects(
    service: ProjectService = Depends(get_project_service),
) -> Sequence[ProjectResponse]:
    """Retrieve a list of all projects."""
    projects = service.get_all_projects()
    return projects