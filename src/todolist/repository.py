"""Data storage for the To-Do List Application.

This module defines the interface for data storage and provides an in-memory
implementation. The current design allows the storage backend to be swapped (e.g., to a
database for later phases of the project) without changing the business logic.
"""

import copy
from abc import ABC, abstractmethod
from collections.abc import Sequence
from datetime import datetime

from todolist.exceptions import EntityDoesNotExistError
from todolist.models import Project, Task

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

    # More abstract methods will be added later as needed

class InMemoryProjectRepository(IProjectRepository):
    """In-memory implementation of a project repository."""

    def __init__(self):
        self._projects: dict[int, Project] = {}
        self._next_project_id: int = 1
        self._next_task_id: int = 1

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

    def find_project_by_id(self, id: int) -> Project | None:
        if id not in self._projects:
            raise EntityDoesNotExistError(entity_name="Project", entity_id=id)
        return copy.deepcopy(self._projects[id])

    def find_project_by_name(self, name: str) -> Project | None:
        for project in self._projects.values():
            if project.name == name:
                return copy.deepcopy(project)
        return None

    def update_project(self, id: int, new_name: str, new_description: str) -> Project:
        project = self.find_project_by_id(id)
        project.name = new_name
        project.description = new_description
        self._projects[id] = project
        return copy.deepcopy(project)

    def delete_project(self, id: int) -> None:
        self.find_project_by_id(id) # To check for existence
        del self._projects[id]

    def create_task(self, project_id: int, title: str,
                    description: str, deadline: datetime | None) -> Task:

        self.find_project_by_id(project_id) # To check for existence (can't use returned
                                            # value because it's a copy.

        task = Task(id=self._next_task_id, title=title,
                    description=description, deadline=deadline)
        self._next_task_id += 1

        self._projects[project_id].tasks.append(task)
        return copy.deepcopy(task)



