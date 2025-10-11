"""Custom exception types for the To-Do List application."""

class TodolistError(Exception):
    """Base exception class for all app-specific errors."""
    pass

class EntityDoesNotExist(TodolistError):
    """Raised when an entity (Project or Task) does not exist."""
    def __init__(self, entity_name: str, entity_id: int):
        super().__init__(f"Entity {entity_name} with ID `{entity_id} does not exist.")

