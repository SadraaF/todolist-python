"""In-memory implementation of the project repository."""
import copy
from collections.abc import Sequence
from datetime import datetime

from src.app.exceptions.base import EntityDoesNotExistError
from src.app.models.project import Project
from src.app.repositories.inmemory_storage import storage
from src.app.repositories.project_repository import IProjectRepository

class InMemoryProjectRepository(IProjectRepository):
    """In-memory implementation of a project repository."""

    def create_project(self, name: str, description: str) -> Project:
        project_id = storage.next_project_id
        project = Project(
            id=project_id,
            name=name,
            description=description,
            created_at=datetime.now(),
            tasks=[]
        )
        storage.projects[project_id] = project
        storage.next_project_id += 1
        return copy.deepcopy(project)

    def list_projects(self) -> Sequence[Project]:
        all_projects = list(storage.projects.values())
        for p in all_projects:
            p.tasks = [copy.deepcopy(t) for t in storage.tasks.values() if t.project_id == p.id]
        sorted_projects = sorted(all_projects, key=lambda p: p.created_at)
        return sorted_projects

    def find_project_by_id(self, id: int) -> Project:
        project = storage.projects.get(id)
        if not project:
            raise EntityDoesNotExistError("Project", id)
        
        project_copy = copy.deepcopy(project)
        project_copy.tasks = [copy.deepcopy(t) for t in storage.tasks.values() if t.project_id == project_copy.id]
        return project_copy

    def find_project_by_name(self, name: str) -> Project | None:
        for project in storage.projects.values():
            if project.name == name:
                return copy.deepcopy(project)
        return None

    def update_project(self, project: Project, new_name: str, new_description: str) -> Project:
        stored_project = storage.projects.get(project.id)
        if not stored_project:
            raise EntityDoesNotExistError("Project", project.id)
        stored_project.name = new_name
        stored_project.description = new_description
        return copy.deepcopy(stored_project)

    def delete_project(self, project: Project) -> None:
        if project.id not in storage.projects:
            raise EntityDoesNotExistError("Project", project.id)
        
        tasks_to_delete = [task_id for task_id, task in storage.tasks.items() if task.project_id == project.id]
        for task_id in tasks_to_delete:
            del storage.tasks[task_id]

        del storage.projects[project.id]