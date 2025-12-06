"""SQLAlchemy implementation of the project repository."""

from collections.abc import Sequence

from sqlalchemy.orm import Session, joinedload

from src.app.exceptions.base import EntityDoesNotExistError
from src.app.models.project import Project
from .project_repository import IProjectRepository


class SqlAlchemyProjectRepository(IProjectRepository):
    """SQLAlchemy-based repository for projects."""

    def __init__(self, session: Session):
        self._session = session

    def create_project(self, name: str, description: str) -> Project:
        project = Project(name=name, description=description)
        self._session.add(project)
        self._session.commit()
        self._session.refresh(project)
        return project

    def list_projects(self) -> Sequence[Project]:
        return self._session.query(Project).options(joinedload(Project.tasks)).order_by(Project.created_at).all()

    def find_project_by_id(self, id: int) -> Project:
        project = self._session.query(Project).options(joinedload(Project.tasks)).get(id)
        if not project:
            raise EntityDoesNotExistError("Project", id)
        return project

    def find_project_by_name(self, name: str) -> Project | None:
        return self._session.query(Project).filter(Project.name == name).first()

    def update_project(self, project: Project, new_name: str, new_description: str) -> Project:
        project.name = new_name
        project.description = new_description
        self._session.commit()
        self._session.refresh(project)
        return project

    def delete_project(self, project: Project) -> None:
        self._session.delete(project)
        self._session.commit()