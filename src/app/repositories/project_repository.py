"""Interface for project data storage."""

from abc import ABC, abstractmethod
from collections.abc import Sequence

from src.app.models.project import Project


class IProjectRepository(ABC):
    """Interface for a project repository."""

    @abstractmethod
    async def create_project(self, name: str, description: str) -> Project:
        """Creates a new project with the given name and description."""
        pass

    @abstractmethod
    async def list_projects(self) -> Sequence[Project]:
        """Returns a list of all projects (sorted by creation time)."""
        pass

    @abstractmethod
    async def find_project_by_id(self, id: int) -> Project:
        """Returns the project with the id. Raises EntityDoesNotExist if not found."""
        pass

    @abstractmethod
    async def find_project_by_name(self, name: str) -> Project | None:
        """Returns the project with the given name. Returns None if not found."""
        pass

    @abstractmethod
    async def update_project(self, project: Project, new_name: str, new_description: str) -> Project:
        """Edits an existing project's details."""
        pass

    @abstractmethod
    async def delete_project(self, project: Project) -> None:
        """Deletes an existing project."""
        pass