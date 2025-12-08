"""Service Layer (Business Logic) for Tasks."""

from datetime import datetime, date

from src.app.exceptions.base import (
    TaskLimitExceededError,
    ValidationError,
)
from src.app.models.task import Task, TaskStatus
from src.app.repositories.project_repository import IProjectRepository
from src.app.repositories.task_repository import ITaskRepository


class TaskService:
    """Handles task business logic."""

    def __init__(self, task_repo: ITaskRepository, project_repo: IProjectRepository, max_tasks: int):
        """Initialize the TaskService.

        :param task_repo: An instance of a class that implements ITaskRepository.
        :param project_repo: An instance of a class that implements IProjectRepository.
        :param max_tasks: The maximum number of tasks allowed per project.
        """
        self._task_repo = task_repo
        self._project_repo = project_repo
        self._max_tasks = max_tasks

    async def add_task_to_project(self, project_id: int, title: str,
                                  description: str | None, deadline: date | None) -> Task:
        """Add a task to an existing project after validation.

        :param project_id: The ID of the project to add the task to.
        :param title: The title of the new task.
        :param description: The description of the new task.
        :param deadline: The deadline for the new task.
        :raises EntityDoesNotExistError: If the project is not found.
        :raises TaskLimitExceededError: If the project's task limit is reached.
        :raises ValidationError: If title or description lengths are invalid.
        :return: The newly created Task object.
        """
        project = await self._project_repo.find_project_by_id(project_id)

        if len(project.tasks) >= self._max_tasks:
            raise TaskLimitExceededError(f"Project '{project.name}' cannot have more tasks.")
        if not title or len(title) > 30:
            raise ValidationError("Task title must be between 1 and 30 characters.")
        if description and len(description) > 150:
            raise ValidationError("Task description must be 150 characters or less.")

        return await self._task_repo.create_task(project_id, title, description, deadline)

    async def change_task_status(self, project_id: int, task_id: int, new_status_str: str) -> Task:
        """Change the status of a task and updates closed_at timestamp.

        :param project_id: The ID of the parent project.
        :param task_id: The ID of the task to update.
        :param new_status_str: The new status string ('todo', 'doing', 'done').
        :raises EntityDoesNotExistError: If project or task is not found.
        :raises ValidationError: If the status string is invalid.
        :return: The updated Task object.
        """
        await self._project_repo.find_project_by_id(project_id)
        task = await self._task_repo.find_task_in_project(project_id, task_id)

        if new_status_str not in ("todo", "doing", "done"):
            raise ValidationError("Task status must be either 'todo', 'doing' or 'done'.")

        new_status: TaskStatus = new_status_str

        new_closed_at = task.closed_at
        if new_status == "done" and task.status != "done":
            new_closed_at = datetime.now()
        elif new_status != "done" and task.status == "done":
            new_closed_at = None

        return await self._task_repo.update_task(
            task, task.title, task.description, new_status, task.deadline, new_closed_at
        )

    async def edit_task(self, project_id: int, task_id: int, new_title: str,
                        new_description: str | None, new_status_str: str,
                        new_deadline: date | None) -> Task:
        """Edit an existing task after validating business rules.

        Also handles updating the closed_at timestamp based on status changes.

        :param project_id: The ID of the parent project.
        :param task_id: The ID of the task to edit.
        :param new_title: The new title for the task.
        :param new_description: The new description for the task.
        :param new_status_str: The new status string for the task.
        :param new_deadline: The new deadline for the task.
        :raises EntityDoesNotExistError: If project or task is not found.
        :raises ValidationError: If any input data is invalid.
        :return: The updated Task object.
        """
        await self._project_repo.find_project_by_id(project_id)
        task = await self._task_repo.find_task_in_project(project_id, task_id)

        if not new_title or len(new_title) > 30:
            raise ValidationError("Task title must be between 1 and 30 characters.")
        if new_description and len(new_description) > 150:
            raise ValidationError("Task description must be 150 characters or less.")
        if new_status_str not in ("todo", "doing", "done"):
            raise ValidationError("Task status must be either 'todo', 'doing' or 'done'.")

        new_status: TaskStatus = new_status_str

        new_closed_at = task.closed_at
        if new_status == "done" and task.status != "done":
            new_closed_at = datetime.now()
        elif new_status != "done" and task.status == "done":
            new_closed_at = None

        return await self._task_repo.update_task(
            task, new_title, new_description, new_status, new_deadline, new_closed_at
        )

    async def delete_task(self, project_id: int, task_id: int) -> None:
        """Delete a task by its ID within a project.

        :param project_id: The ID of the parent project.
        :param task_id: The ID of the task to delete.
        :raises EntityDoesNotExistError: If the project or task is not found.
        """
        await self._project_repo.find_project_by_id(project_id)
        task = await self._task_repo.find_task_in_project(project_id, task_id)
        await self._task_repo.delete_task(task)

    async def autoclose_overdue_tasks(self) -> int:
        """Find and close all overdue tasks, setting their status to 'done'.

        Sets the closed_at timestamp to the current time for all affected tasks.

        :return: The number of tasks that were closed.
        """
        overdue_tasks = await self._task_repo.find_overdue_tasks()
        if not overdue_tasks:
            return 0

        now = datetime.now()
        for task in overdue_tasks:
            await self._task_repo.update_task(
                task=task,
                new_title=task.title,
                new_description=task.description,
                new_status="done",
                new_deadline=task.deadline,
                new_closed_at=now
            )
        return len(overdue_tasks)