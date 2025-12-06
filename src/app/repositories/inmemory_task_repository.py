"""In-memory implementation of the task repository."""
import copy
from collections.abc import Sequence
from datetime import datetime

from src.app.exceptions.base import EntityDoesNotExistError
from src.app.models.task import Task, TaskStatus
from src.app.repositories.inmemory_storage import storage
from src.app.repositories.task_repository import ITaskRepository

class InMemoryTaskRepository(ITaskRepository):
    """In-memory implementation of a task repository."""

    def create_task(self, project_id: int, title: str,
                    description: str | None, deadline: datetime | None) -> Task:
        if project_id not in storage.projects:
            raise EntityDoesNotExistError("Project", project_id)

        task_id = storage.next_task_id
        task = Task(
            id=task_id,
            project_id=project_id,
            title=title,
            description=description,
            deadline=deadline,
            status="todo",
            created_at=datetime.now()
        )
        storage.tasks[task_id] = task
        storage.next_task_id += 1
        return copy.deepcopy(task)

    def find_task_in_project(self, project_id: int, task_id: int) -> Task:
        task = storage.tasks.get(task_id)
        if not task or task.project_id != project_id:
            raise EntityDoesNotExistError("Task", task_id)
        return copy.deepcopy(task)

    def update_task_status(self, task: Task, new_status: TaskStatus) -> Task:
        stored_task = storage.tasks.get(task.id)
        if not stored_task:
            raise EntityDoesNotExistError("Task", task.id)
        stored_task.status = new_status
        if new_status == "done" and stored_task.closed_at is None:
            stored_task.closed_at = datetime.now()
        elif new_status != "done":
            stored_task.closed_at = None
        return copy.deepcopy(stored_task)

    def update_task(self, task: Task, new_title: str,
                    new_description: str | None, new_status: TaskStatus,
                    new_deadline: datetime | None, new_closed_at: datetime | None) -> Task:
        stored_task = storage.tasks.get(task.id)
        if not stored_task:
            raise EntityDoesNotExistError("Task", task.id)
        
        stored_task.title = new_title
        stored_task.description = new_description
        stored_task.status = new_status
        stored_task.deadline = new_deadline
        stored_task.closed_at = new_closed_at
        return copy.deepcopy(stored_task)

    def delete_task(self, task: Task) -> None:
        if task.id in storage.tasks:
            del storage.tasks[task.id]

    def find_overdue_tasks(self) -> Sequence[Task]:
        now = datetime.now()
        overdue_tasks = []
        for task in storage.tasks.values():
            if task.deadline and task.deadline < now and task.status != "done":
                overdue_tasks.append(copy.deepcopy(task))
        return overdue_tasks