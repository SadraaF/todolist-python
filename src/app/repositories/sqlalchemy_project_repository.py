"""SQLAlchemy implementation of the project repository."""

from collections.abc import Sequence
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.exceptions.base import EntityDoesNotExistError
from src.app.models.project import Project
from .project_repository import IProjectRepository


class SqlAlchemyProjectRepository(IProjectRepository):
    """SQLAlchemy-based repository for projects."""

    def __init__(self, session: Session):
        self._session = session

    async def create_project(self, name: str, description: str) -> Project:
        project = Project(name=name, description=description)
        self._session.add(project)
        await self._session.commit()
        await self._session.refresh(project, attribute_names=["tasks"])
        return project

    async def list_projects(self) -> Sequence[Project]:
        stmt = select(Project).options(joinedload(Project.tasks)).order_by(Project.created_at)
        result = await self._session.execute(stmt)
        return result.unique().scalars().all()

    async def find_project_by_id(self, id: int) -> Project:
        project = await self._session.get(Project, id, options=[joinedload(Project.tasks)])
        if not project:
            raise EntityDoesNotExistError("Project", id)
        return project

    async def find_project_by_name(self, name: str) -> Project | None:
        stmt = select(Project).where(Project.name == name)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def update_project(self, project: Project, new_name: str, new_description: str) -> Project:
        project.name = new_name
        project.description = new_description
        await self._session.commit()
        await self._session.refresh(project, attribute_names=["tasks"])
        return project

    async def delete_project(self, project: Project) -> None:
        await self._session.delete(project)
        await self._session.commit()