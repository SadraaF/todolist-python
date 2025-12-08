"""SQLAlchemy implementation of the project repository."""

from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from src.app.exceptions.base import EntityDoesNotExistError
from src.app.models.project import Project
from .project_repository import IProjectRepository


class SqlAlchemyProjectRepository(IProjectRepository):
    """SQLAlchemy-based repository for projects."""

    def __init__(self, session: Session):
        """Initialize the repository with an async database session.

        :param session: An SQLAlchemy AsyncSession instance.
        """
        self._session = session

    async def create_project(self, name: str, description: str) -> Project:
        """Create a new project and persist it to the database.

        :param name: The name for the new project.
        :param description: The description for the new project.
        :return: The newly created Project object.
        """
        project = Project(name=name, description=description)
        self._session.add(project)
        await self._session.commit()
        await self._session.refresh(project, attribute_names=["tasks"])
        return project

    async def list_projects(self) -> Sequence[Project]:
        """Retrieve all projects from the database, sorted by creation time.

        :return: A sequence of all Project objects.
        """
        # Use joinedload to eagerly load related tasks in a single query.
        # This prevents the "N+1" problem where accessing each project's tasks
        # would trigger a separate database query.
        stmt = select(Project).options(joinedload(Project.tasks)).order_by(Project.created_at)
        result = await self._session.execute(stmt)
        return result.unique().scalars().all()

    async def find_project_by_id(self, id: int) -> Project:
        """Find a single project by its unique ID in the database.

        :param id: The ID of the project to find.
        :raises EntityDoesNotExistError: If no project with the given ID exists.
        :return: The found Project object.
        """
        # Use joinedload to eagerly load the tasks relationship.
        project = await self._session.get(Project, id, options=[joinedload(Project.tasks)])
        if not project:
            raise EntityDoesNotExistError("Project", id)
        return project

    async def find_project_by_name(self, name: str) -> Project | None:
        """Find a single project by its unique name in the database.

        :param name: The name of the project to find.
        :return: The found Project object, or None if it does not exist.
        """
        stmt = select(Project).where(Project.name == name)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def update_project(self, project: Project, new_name: str, new_description: str) -> Project:
        """Update an existing project's details in the database.

        :param project: The Project object to update.
        :param new_name: The new name for the project.
        :param new_description: The new description for the project.
        :return: The updated Project object.
        """
        project.name = new_name
        project.description = new_description
        await self._session.commit()
        await self._session.refresh(project, attribute_names=["tasks"])
        return project

    async def delete_project(self, project: Project) -> None:
        """Delete an existing project from the database.

        :param project: The Project object to delete.
        """
        await self._session.delete(project)
        await self._session.commit()