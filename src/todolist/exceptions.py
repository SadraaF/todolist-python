"""Custom exception types for the ToDo List application."""

class TodolistError(Exception):
    """Base exception class for all app-specific errors."""
    pass

class EntityDoesNotExistError(TodolistError):
    """Raised when an entity (Project or Task) does not exist."""
    def __init__(self, entity_name: str, entity_id: int):
        super().__init__(f"Entity {entity_name} with ID {entity_id} does not exist.")

class ValidationError(TodolistError):
    """Raised when a business rule or data constraint is violated."""
    pass

class DuplicateProjectNameError(ValidationError):
    """Raised when a project name already exists."""
    def __init__(self, project_name: str):
        super().__init__(f"A project with the name '{project_name}' already exists.")

class ProjectLimitExceededError(ValidationError):
    """Raised when the maximum number of projects is exceeded."""
    pass

class TaskLimitExceededError(ValidationError):
    """Raised when the maximum number of tasks for a project is exceeded."""
    pass
