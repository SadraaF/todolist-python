"""Interface for task data storage."""

from abc import ABC, abstractmethod
from collections.abc import Sequence
from datetime import datetime

from src.app.models.task import Task, TaskStatus


class ITaskRepository(ABC):
    """Interface for a task repository."""

    @abstractmethod
    async def create_task(self, project_id: int, title: str,
                    description: str | None, deadline: datetime | None) -> Task:
        """Create a new task within a project and persist it.

        :param project_id: The ID of the parent project.
        :param title: The title for the new task.
        :param description: The description for the new task.
        :param deadline: The optional deadline for the new task.
        :return: The newly created Task object.
        """
        pass

    @abstractmethod
    async def find_task_in_project(self, project_id: int, task_id: int) -> Task:
        """Find a single task by its ID within a specific project.

        :param project_id: The ID of the parent project.
        :param task_id: The ID of the task to find.
        :raises EntityDoesNotExistError: If no task with the given ID exists in the project.
        :return: The found Task object.
        """
        pass

    @abstractmethod
    async def update_task_status(self, task: Task, new_status: TaskStatus) -> Task:
        """Update only the status of a task.

        :param task: The Task object to update.
        :param new_status: The new status for the task.
        :return: The updated Task object.
        """
        pass

    @abstractmethod
    async def update_task(self, task: Task, new_title: str,
                    new_description: str | None, new_status: TaskStatus,
                    new_deadline: datetime | None, new_closed_at: datetime | None) -> Task:
        """Update all attributes of an existing task.

        :param task: The Task object to update.
        :param new_title: The new title for the task.
        :param new_description: The new description for the task.
        :param new_status: The new status for the task.
        :param new_deadline: The new deadline for the task.
        :param new_closed_at: The new closed_at timestamp for the task.
        :return: The updated Task object.
        """
        pass

    @abstractmethod
    async def delete_task(self, task: Task) -> None:
        """Delete an existing task from storage.

        :param task: The Task object to delete.
        """
        pass

    @abstractmethod
    async def find_overdue_tasks(self) -> Sequence[Task]:
        """Retrieve all tasks that are past their deadline and not 'done'.

        :return: A sequence of overdue Task objects.
        """
        pass