"""Pydantic schemas for Task resources."""

from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field

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


class TaskResponse(TaskBase):
    """Schema for representing a task in API responses."""
    id: int
    project_id: int
    status: TaskStatus
    created_at: datetime
    closed_at: datetime | None = None

    # Create the schema from an ORM model
    model_config = ConfigDict(from_attributes=True)