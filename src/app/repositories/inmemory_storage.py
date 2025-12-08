"""A shared, in-memory data store for testing and development."""

from src.app.models.project import Project
from src.app.models.task import Task

class InMemoryStorage:
    """Singleton class to hold in-memory data."""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(InMemoryStorage, cls).__new__(cls)
            cls._instance.projects: dict[int, Project] = {}
            cls._instance.tasks: dict[int, Task] = {}
            cls._instance.next_project_id: int = 1
            cls._instance.next_task_id: int = 1
        return cls._instance

    def clear(self):
        """Clears all data."""
        self.projects.clear()
        self.tasks.clear()
        self.next_project_id = 1
        self.next_task_id = 1

# Instantiate a single global storage object
storage = InMemoryStorage()