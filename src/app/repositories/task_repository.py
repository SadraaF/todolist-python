"""Interface for task data storage."""

from abc import ABC, abstractmethod
from collections.abc import Sequence
from datetime import datetime

from src.app.models.task import Task, TaskStatus


class ITaskRepository(ABC):
    """Interface for a task repository."""

    @abstractmethod
    def create_task(self, project_id: int, title: str,
                    description: str | None, deadline: datetime | None) -> Task:
        """Creates a new task within a project."""
        pass

    @abstractmethod
    def find_task_in_project(self, project_id: int, task_id: int) -> Task:
        """Finds a task by its ID within a specific project."""
        pass

    @abstractmethod
    def update_task_status(self, task: Task, new_status: TaskStatus) -> Task:
        """Updates a task's status."""
        pass

    @abstractmethod
    def update_task(self, task: Task, new_title: str,
                    new_description: str | None, new_status: TaskStatus,
                    new_deadline: datetime | None, new_closed_at: datetime | None) -> Task:
        """Updates all attributes of a task."""
        pass

    @abstractmethod
    def delete_task(self, task: Task) -> None:
        """Deletes a task."""
        pass

    @abstractmethod
    def find_overdue_tasks(self) -> Sequence[Task]:
        """Returns a list of all tasks that are past their deadline and not done."""
        pass