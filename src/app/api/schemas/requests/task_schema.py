"""Pydantic schemas for Task API requests."""

from datetime import datetime
from pydantic import BaseModel, Field

from src.app.models.task import TaskStatus


class TaskBase(BaseModel):
    """Base schema for a task, containing common fields."""
    title: str = Field(..., min_length=1, max_length=30)
    description: str | None = Field(default=None, max_length=150)
    deadline: datetime | None = None


class TaskCreate(TaskBase):
    """Schema used for creating a new task."""
    pass


class TaskUpdate(TaskBase):
    """Schema used for updating an existing task (PUT)."""
    status: TaskStatus


class TaskStatusUpdate(BaseModel):
    """Schema used for partially updating a task's status (PATCH)."""
    status: TaskStatus