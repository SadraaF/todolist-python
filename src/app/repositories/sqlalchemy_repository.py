"""SQLAlchemy implementation of the project repository."""

from collections.abc import Sequence
from datetime import datetime

from sqlalchemy.orm import Session, joinedload

from src.app.exceptions.base import EntityDoesNotExistError
from src.app.models.project import Project
from src.app.models.task import Task, TaskStatus
from .project_repository import IProjectRepository


class SqlAlchemyProjectRepository(IProjectRepository):
    """SQLAlchemy-based repository for projects and tasks."""

    def __init__(self, session: Session):
        self._session = session

    def _get_project_or_raise(self, id: int) -> Project:
        """Fetch a project by ID or raise an exception."""
        project = self._session.get(Project, id)
        if not project:
            raise EntityDoesNotExistError("Project", id)
        return project

    def _find_task_in_project_or_raise(self, project: Project, task_id: int) -> Task:
        """Fetch a task by ID within a project or raise an exception."""
        task = self._session.query(Task).filter_by(project_id=project.id, id=task_id).first()
        if not task:
            raise EntityDoesNotExistError("Task", task_id)
        return task

    def create_project(self, name: str, description: str) -> Project:
        project = Project(name=name, description=description)
        self._session.add(project)
        self._session.commit()
        self._session.refresh(project)
        return project

    def list_projects(self) -> Sequence[Project]:
        return self._session.query(Project).order_by(Project.created_at).all()

    def find_project_by_id(self, id: int) -> Project:
        # Eagerly load tasks to avoid extra queries when accessing project.tasks
        project = self._session.query(Project).options(joinedload(Project.tasks)).get(id)
        if not project:
            raise EntityDoesNotExistError("Project", id)
        return project

    def find_project_by_name(self, name: str) -> Project | None:
        return self._session.query(Project).filter(Project.name == name).first()

    def update_project(self, id: int, new_name: str, new_description: str) -> Project:
        project = self._get_project_or_raise(id)
        project.name = new_name
        project.description = new_description
        self._session.commit()
        self._session.refresh(project)
        return project

    def delete_project(self, id: int) -> None:
        project = self._get_project_or_raise(id)
        self._session.delete(project)
        self._session.commit()

    def create_task(
        self, project_id: int, title: str, description: str, deadline: datetime | None
    ) -> Task:
        # Ensure the project exists first
        self._get_project_or_raise(project_id)

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

    def update_task_status(
        self, project_id: int, task_id: int, new_status: TaskStatus
    ) -> Task:
        project = self._get_project_or_raise(project_id)
        task = self._find_task_in_project_or_raise(project, task_id)
        task.status = new_status
        self._session.commit()
        self._session.refresh(task)
        return task

    def update_task(
        self,
        project_id: int,
        task_id: int,
        new_title: str,
        new_description: str,
        new_status: TaskStatus,
        new_deadline: datetime | None,
    ) -> Task:
        project = self._get_project_or_raise(project_id)
        task = self._find_task_in_project_or_raise(project, task_id)
        task.title = new_title
        task.description = new_description
        task.status = new_status
        task.deadline = new_deadline
        self._session.commit()
        self._session.refresh(task)
        return task

    def delete_task(self, project_id: int, task_id: int) -> None:
        project = self._get_project_or_raise(project_id)
        task = self._find_task_in_project_or_raise(project, task_id)
        self._session.delete(task)
        self._session.commit()