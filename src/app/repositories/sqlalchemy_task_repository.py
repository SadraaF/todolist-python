"""SQLAlchemy implementation of the task repository."""

from collections.abc import Sequence
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from src.app.exceptions.base import EntityDoesNotExistError
from src.app.models.task import Task, TaskStatus
from .task_repository import ITaskRepository


class SqlAlchemyTaskRepository(ITaskRepository):
    """SQLAlchemy-based repository for tasks."""

    def __init__(self, session: AsyncSession):
        self._session = session

    async def create_task(
        self, project_id: int, title: str, description: str | None, deadline: datetime | None
    ) -> Task:
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
        """Fetch a task by ID within a project or raise an exception."""
        stmt = select(Task).where(Task.project_id == project_id, Task.id == task_id)
        result = await self._session.execute(stmt)
        task = result.scalar_one_or_none()
        if not task:
            raise EntityDoesNotExistError("Task", task_id)
        return task

    async def update_task_status(self, task: Task, new_status: TaskStatus) -> Task:
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
        task.title = new_title
        task.description = new_description
        task.status = new_status
        task.deadline = new_deadline
        task.closed_at = new_closed_at
        await self._session.commit()
        await self._session.refresh(task)
        return task

    async def delete_task(self, task: Task) -> None:
        await self._session.delete(task)
        await self._session.commit()

    async def find_overdue_tasks(self) -> Sequence[Task]:
        """Returns a list of all tasks that are past their deadline and not done."""
        now = datetime.now()
        stmt = select(Task).where(Task.deadline < now, Task.status != "done")
        result = await self._session.execute(stmt)
        return result.scalars().all()