"""SQLAlchemy implementation of the task repository."""

from collections.abc import Sequence
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.exceptions.base import EntityDoesNotExistError
from src.app.models.task import Task, TaskStatus
from .task_repository import ITaskRepository


class SqlAlchemyTaskRepository(ITaskRepository):
    """SQLAlchemy-based repository for tasks."""

    def __init__(self, session: AsyncSession):
        """Initialize the repository with an async database session.

        :param session: An SQLAlchemy AsyncSession instance.
        """
        self._session = session

    async def create_task(
        self, project_id: int, title: str, description: str | None, deadline: datetime | None
    ) -> Task:
        """Create a new task and persist it to the database.

        :param project_id: The ID of the parent project.
        :param title: The title for the new task.
        :param description: The description for the new task.
        :param deadline: The optional deadline for the new task.
        :return: The newly created Task object.
        """
        task = Task(
            project_id=project_id,
            title=title,
            description=description,
            deadline=deadline,
        )
        self._session.add(task)
        await self._session.commit()
        await self._session.refresh(task)
        return task

    async def find_task_in_project(self, project_id: int, task_id: int) -> Task:
        """Find a single task by its ID within a specific project in the database.

        :param project_id: The ID of the parent project.
        :param task_id: The ID of the task to find.
        :raises EntityDoesNotExistError: If no task with the given ID exists in the project.
        :return: The found Task object.
        """
        stmt = select(Task).where(Task.project_id == project_id, Task.id == task_id)
        result = await self._session.execute(stmt)
        task = result.scalar_one_or_none()
        if not task:
            raise EntityDoesNotExistError("Task", task_id)
        return task

    async def update_task_status(self, task: Task, new_status: TaskStatus) -> Task:
        """Update only the status of a task in the database.

        :param task: The Task object to update.
        :param new_status: The new status for the task.
        :return: The updated Task object.
        """
        task.status = new_status
        await self._session.commit()
        await self._session.refresh(task)
        return task

    async def update_task(
        self,
        task: Task,
        new_title: str,
        new_description: str | None,
        new_status: TaskStatus,
        new_deadline: datetime | None,
        new_closed_at: datetime | None
    ) -> Task:
        """Update all attributes of an existing task in the database.

        :param task: The Task object to update.
        :param new_title: The new title for the task.
        :param new_description: The new description for the task.
        :param new_status: The new status for the task.
        :param new_deadline: The new deadline for the task.
        :param new_closed_at: The new closed_at timestamp for the task.
        :return: The updated Task object.
        """
        task.title = new_title
        task.description = new_description
        task.status = new_status
        task.deadline = new_deadline
        task.closed_at = new_closed_at
        await self._session.commit()
        await self._session.refresh(task)
        return task

    async def delete_task(self, task: Task) -> None:
        """Delete an existing task from the database.

        :param task: The Task object to delete.
        """
        await self._session.delete(task)
        await self._session.commit()

    async def find_overdue_tasks(self) -> Sequence[Task]:
        """Retrieve all tasks from the database that are past their deadline and not 'done'.

        :return: A sequence of overdue Task objects.
        """
        now = datetime.now()
        stmt = select(Task).where(Task.deadline < now, Task.status != "done")
        result = await self._session.execute(stmt)
        return result.scalars().all()