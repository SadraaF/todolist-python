"""Interface for project data storage and retrieval."""

from abc import ABC, abstractmethod
from collections.abc import Sequence

from src.app.models.project import Project


class IProjectRepository(ABC):
    """Interface defining the contract for project repository implementations."""

    @abstractmethod
    async def create_project(self, name: str, description: str) -> Project:
        """Create a new project and persist it.

        :param name: The name for the new project.
        :param description: The description for the new project.
        :return: The newly created Project object.
        """
        pass

    @abstractmethod
    async def list_projects(self) -> Sequence[Project]:
        """Retrieve all projects, sorted by creation time.

        :return: A sequence of all Project objects.
        """
        pass

    @abstractmethod
    async def find_project_by_id(self, id: int) -> Project:
        """Find a single project by its unique ID.

        :param id: The ID of the project to find.
        :raises EntityDoesNotExistError: If no project with the given ID exists.
        :return: The found Project object.
        """
        pass

    @abstractmethod
    async def find_project_by_name(self, name: str) -> Project | None:
        """Find a single project by its unique name.

        :param name: The name of the project to find.
        :return: The found Project object, or None if it does not exist.
        """
        pass

    @abstractmethod
    async def update_project(self, project: Project, new_name: str, new_description: str) -> Project:
        """Update an existing project's details.

        :param project: The Project object to update.
        :param new_name: The new name for the project.
        :param new_description: The new description for the project.
        :return: The updated Project object.
        """
        pass

    @abstractmethod
    async def delete_project(self, project: Project) -> None:
        """Delete an existing project from storage.

        :param project: The Project object to delete.
        """
        pass