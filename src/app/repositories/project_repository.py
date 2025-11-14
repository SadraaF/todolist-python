"""Data storage for the ToDo List Application.

This module defines the interface for data storage and provides an in-memory
implementation. The current design allows the storage backend to be swapped (e.g., to a
database for later phases of the project) without changing the business logic.
"""

import copy
from abc import ABC, abstractmethod
from collections.abc import Sequence
from datetime import datetime

from src.app.exceptions.base import EntityDoesNotExistError
from src.app.models.project import Project
from src.app.models.task import Task, TaskStatus


class IProjectRepository(ABC):
    """Interface for a project and task repository."""

    @abstractmethod
    def create_project(self, name: str, description: str) -> Project:
        """Creates a new project with the given name and description."""
        pass

    @abstractmethod
    def list_projects(self) -> Sequence[Project]:
        """Returns a list of all projects (sorted by creation time)."""
        pass

    @abstractmethod
    def find_project_by_id(self, id: int) -> Project:
        """Returns the project with the id. Raises EntityDoesNotExist if not found."""
        pass

    @abstractmethod
    def find_project_by_name(self, name: str) -> Project | None:
        """Returns the project with the given name. This method does not raise an
         exception, as finding nothing is a valid result (e.g., when verifying that the
         name of a new project isn't a duplicate)."""
        pass

    @abstractmethod
    def update_project(self, id: int, new_name: str, new_description: str) -> Project:
        """Edits an existing project's details."""
        pass

    @abstractmethod
    def delete_project(self, id: int) -> None:
        """Deletes an existing project and all of its tasks."""
        pass

    @abstractmethod
    def create_task(self, project_id: int, title: str,
                    description: str, deadline: datetime | None) -> Task:
        """Creates a new task within a project."""
        pass

    @abstractmethod
    def update_task_status(self, project_id: int,
                           task_id: int, new_status: TaskStatus) -> Task:
        """Finds a task by its ID and updates its status."""
        pass

    @abstractmethod
    def update_task(self, project_id: int, task_id: int, new_title: str,
                    new_description: str, new_status: TaskStatus,
                    new_deadline: datetime | None, new_closed_at: datetime | None) -> Task:

        """Finds a task and updates all its attributes."""
        pass

    @abstractmethod
    def delete_task(self, project_id: int, task_id: int) -> None:
        """Deletes a task by its ID within a project."""
        pass

    @abstractmethod
    def find_overdue_tasks(self) -> Sequence[Task]:
        """Returns a list of all tasks that are past their deadline and not done."""
        pass

class InMemoryProjectRepository(IProjectRepository):
    """In-memory implementation of a project repository."""

    def __init__(self):
        self._projects: dict[int, Project] = {}
        self._next_project_id: int = 1

    def _get_project_or_raise(self, id: int) -> Project:
        """Return a project by its ID or raise EntityDoesNotExistError."""
        project = self._projects.get(id)
        if not project:
            raise EntityDoesNotExistError("Project", id)
        return project

    @staticmethod
    def _find_task_or_raise(project: Project, task_id: int) -> Task:
        """Find a task in a project by its ID or raise EntityDoesNotExistError."""
        for task in project.tasks:
            if task.id == task_id:
                return task
        raise EntityDoesNotExistError("Task", task_id)

    def create_project(self, name: str, description: str) -> Project:
        project_id = self._next_project_id
        project = Project(id=project_id, name=name, description=description)
        self._projects[project_id] = project
        self._next_project_id += 1
        return copy.deepcopy(project)

    def list_projects(self) -> Sequence[Project]:
        all_projects = self._projects.values()
        sorted_projects = sorted(all_projects, key=lambda p: p.creation_date)
        return [copy.deepcopy(project) for project in sorted_projects]

    def find_project_by_id(self, id: int) -> Project:
        # The difference between this method and _get_project_or_raise is the deep copy.
        return copy.deepcopy(self._get_project_or_raise(id))

    def find_project_by_name(self, name: str) -> Project | None:
        for project in self._projects.values():
            if project.name == name:
                return copy.deepcopy(project)
        return None

    def update_project(self, id: int, new_name: str, new_description: str) -> Project:
        project = self._get_project_or_raise(id)
        project.name = new_name
        project.description = new_description
        return copy.deepcopy(project)

    def delete_project(self, id: int) -> None:
        self._get_project_or_raise(id) # To check for existence
        del self._projects[id]

    def create_task(self, project_id: int, title: str,
                    description: str, deadline: datetime | None) -> Task:

        project = self._get_project_or_raise(project_id)

        task = Task(id=project._next_task_id, title=title,
                    description=description, deadline=deadline)
        project._next_task_id += 1

        project.tasks.append(task)
        return copy.deepcopy(task)

    def update_task_status(self, project_id: int,
                           task_id: int, new_status: TaskStatus) -> Task:
        project = self._get_project_or_raise(project_id)

        task = self._find_task_or_raise(project, task_id)
        task.status = new_status
        return copy.deepcopy(task)

    def update_task(self, project_id: int, task_id: int, new_title: str,
                    new_description: str, new_status: TaskStatus,
                    new_deadline: datetime | None, new_closed_at: datetime | None) -> Task:

        project = self._get_project_or_raise(project_id)
        task = self._find_task_or_raise(project, task_id)

        task.title = new_title
        task.description = new_description
        task.status = new_status
        task.deadline = new_deadline
        task.closed_at = new_closed_at

        return copy.deepcopy(task)

    def delete_task(self, project_id: int, task_id: int) -> None:
        project = self._get_project_or_raise(project_id)
        task = self._find_task_or_raise(project, task_id)
        project.tasks.remove(task)

    def find_overdue_tasks(self) -> Sequence[Task]:
        """Returns a list of all tasks that are past their deadline and not done."""
        now = datetime.now()
        overdue_tasks = []
        for project in self._projects.values():
            for task in project.tasks:
                if task.deadline and task.deadline < now and task.status != "done":
                    overdue_tasks.append(copy.deepcopy(task))
        return overdue_tasks
