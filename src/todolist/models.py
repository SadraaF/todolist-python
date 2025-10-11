"""Defines the core data models for the ToDo List application.

This module defines the two primary data structures used in the ToDo List application,
which are Project and Task. These models are simple data structures (using dataclasses)
and are used throughout the application's various parts.
"""

from typing import Literal
from datetime import datetime
from dataclasses import dataclass, field

TaskStatus = Literal["todo", "doing", "done"] # Defining a specific type for type safety

@dataclass
class Task:
    """A single task within a project."""
    id: int
    title: str
    description: str
    status: TaskStatus
    deadline: datetime | None = None # Deadline is optional

@dataclass
class Project:
    """A single project that can contain multiple tasks."""
    id: int
    title: str
    description: str
    tasks: list[Task] = field(default_factory=list)
    
