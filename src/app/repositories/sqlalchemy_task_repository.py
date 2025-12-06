"""SQLAlchemy implementation of the task repository."""

from collections.abc import Sequence
from datetime import datetime

from sqlalchemy.orm import Session

from src.app.exceptions.base import EntityDoesNotExistError
from src.app.models.task import Task, TaskStatus
from .task_repository import ITaskRepository


class SqlAlchemyTaskRepository(ITaskRepository):
    """SQLAlchemy-based repository for tasks."""

    def __init__(self, session: Session):
        self._session = session

    def create_task(
        self, project_id: int, title: str, description: str | None, deadline: datetime | None
    ) -> Task:
        task = Task(
            project_id=project_id,
            title=title,
            description=description,
            deadline=deadline,
        )
        self._session.add(task)
        self._session.commit()
        self._session.refresh(task)
        return task

    def find_task_in_project(self, project_id: int, task_id: int) -> Task:
        """Fetch a task by ID within a project or raise an exception."""
        task = self._session.query(Task).filter_by(project_id=project_id, id=task_id).first()
        if not task:
            raise EntityDoesNotExistError("Task", task_id)
        return task

    def update_task_status(self, task: Task, new_status: TaskStatus) -> Task:
        task.status = new_status
        self._session.commit()
        self._session.refresh(task)
        return task

    def update_task(
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
        self._session.commit()
        self._session.refresh(task)
        return task

    def delete_task(self, task: Task) -> None:
        self._session.delete(task)
        self._session.commit()

    def find_overdue_tasks(self) -> Sequence[Task]:
        """Returns a list of all tasks that are past their deadline and not done."""
        now = datetime.now()
        return (
            self._session.query(Task)
            .filter(Task.deadline < now, Task.status != "done")
            .all()
        )