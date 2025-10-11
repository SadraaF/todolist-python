"""Service Layer (Business Logic) for the ToDo List application.

This module contains the core business logic and handles the interaction between the
user interface layer and the data layer (repository). It is responsible for enforcing
business rules such as validation and data constraints.
"""

from datetime import datetime
from collections.abc import Sequence

from todolist.exceptions import (
    DuplicateProjectNameError,
    EntityDoesNotExistError,
    ProjectLimitExceededError,
    TaskLimitExceededError,
    ValidationError,
)
from todolist.models import Project, Task, TaskStatus
from todolist.repository import IProjectRepository

class ProjectService:
    """Handles projects and tasks, enforcing rules."""

    def __init__(self, repo: IProjectRepository, max_projects: int, max_tasks: int):
        """Initialize the service with a repository and configuration.

        :param repo: The repository that contains the projects.
        :param max_projects: The maximum number of projects allowed.
        :param max_tasks: The maximum number of tasks per project allowed.
        """
        self._repo = repo
        self._max_projects = max_projects
        self._max_tasks = max_tasks

    @staticmethod
    def _parse_deadline(deadline_str: str | None) -> datetime | None:
        """Parse a deadline string into a datetime object."""
        if deadline_str is None:
            return None
        try:
            return datetime.strptime(deadline_str, "%Y-%m-%d")
        except ValueError:
            raise ValidationError(f"Invalid deadline format. Use YYYY-MM-DD")

    def create_project(self, name: str, description: str) -> Project:
        """Create a new project after validating business rules."""
        if len(name) > 30:
            raise ValidationError("Project name must be 30 characters or less.")
        if len(description) > 150:
            raise ValidationError("Project description must be 150 characters or less.")

        if len(self._repo.list_projects()) >= self._max_projects:
            raise ProjectLimitExceededError(f"Cannot create more than "
                                            f"{self._max_projects} projects.")

        if self._repo.find_project_by_name(name) is not None:
            raise DuplicateProjectNameError(name)

        return self._repo.create_project(name, description)

    def add_task_to_project(self, project_id: int, title: str,
                            description: str, deadline_str: str | None) -> Task:
        """Add a task to an existing project after validation."""
        project = self._repo.find_project_by_id(project_id)

        if len(project.tasks) >= self._max_tasks:
            raise TaskLimitExceededError(f"Project '{project.name}' cannot have"
                                         f"more tasks.")
        if len(title) > 30:
            raise ValidationError("Task title must be 30 characters or less.")
        if len(description) > 150:
            raise ValidationError("Task description must be 150 characters or less.")

        deadline = self._parse_deadline(deadline_str)

        return self._repo.create_task(project_id, title, description, deadline)

    def get_all_projects(self) -> Sequence[Project]:
        """Get all projects."""
        return self._repo.list_projects()

    def find_project_by_id(self, id: int) -> Project:
        """Find a project by its ID."""
        return self._repo.find_project_by_id(id)
    
    def edit_project(self, project_id: int, new_name: str,
                     new_description: str) -> Project:
        """Edit an existing project after validating business rules."""
        self._repo.find_project_by_id(project_id) # To check for existence

        if len(new_name) > 30:
            raise ValidationError("Project name must be 30 characters or less.")
        if len(new_description) > 150:
            raise ValidationError("Project description must be 150 characters or less.")

        existing_project = self._repo.find_project_by_name(new_name)
        if existing_project is not None and existing_project.id != project_id:
            raise DuplicateProjectNameError(new_name)

        return self._repo.update_project(project_id, new_name, new_description)

    def delete_project(self, project_id: int) -> None:
        """Delete a project by its ID."""
        self._repo.delete_project(project_id)

    def change_task_status(self, project_id: int, task_id: int,
                           new_status_str: str) -> Task:
        """Change the status of a task after validating."""
        if new_status_str not in ("todo", "doing", "done"):
            raise ValidationError("Task status must be either"
                                  " 'todo', 'doing' or 'done'.")

        new_status: TaskStatus = new_status_str
        return self._repo.update_task_status(project_id, task_id, new_status)


