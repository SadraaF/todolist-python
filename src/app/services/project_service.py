"""Service Layer (Business Logic) for Projects."""

from collections.abc import Sequence

from src.app.exceptions.base import (
    DuplicateProjectNameError,
    ProjectLimitExceededError,
    ValidationError,
)
from src.app.models.project import Project
from src.app.repositories.project_repository import IProjectRepository


class ProjectService:
    """Handles project business logic."""

    def __init__(self, repo: IProjectRepository, max_projects: int):
        self._repo = repo
        self._max_projects = max_projects

    async def create_project(self, name: str, description: str) -> Project:
        """Create a new project after validating business rules."""
        if not name or len(name) > 30:
            raise ValidationError("Project name must be between 1 and 30 characters.")
        if description and len(description) > 150:
            raise ValidationError("Project description must be 150 characters or less.")

        projects = await self._repo.list_projects()
        if len(projects) >= self._max_projects:
            raise ProjectLimitExceededError(f"Cannot create more than {self._max_projects} projects.")

        if await self._repo.find_project_by_name(name) is not None:
            raise DuplicateProjectNameError(name)

        return await self._repo.create_project(name, description)

    async def get_all_projects(self) -> Sequence[Project]:
        """Get all projects."""
        return await self._repo.list_projects()

    async def find_project_by_id(self, id: int) -> Project:
        """Find a project by its ID."""
        return await self._repo.find_project_by_id(id)

    async def edit_project(self, project_id: int, new_name: str, new_description: str) -> Project:
        """Edit an existing project after validating business rules."""
        project = await self._repo.find_project_by_id(project_id)

        if not new_name or len(new_name) > 30:
            raise ValidationError("Project name must be between 1 and 30 characters.")
        if new_description and len(new_description) > 150:
            raise ValidationError("Project description must be 150 characters or less.")

        existing_project = await self._repo.find_project_by_name(new_name)
        if existing_project is not None and existing_project.id != project_id:
            raise DuplicateProjectNameError(new_name)

        return await self._repo.update_project(project, new_name, new_description)

    async def delete_project(self, project_id: int) -> None:
        """Delete a project by its ID."""
        project = await self._repo.find_project_by_id(project_id)
        await self._repo.delete_project(project)