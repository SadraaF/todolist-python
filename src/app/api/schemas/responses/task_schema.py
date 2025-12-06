"""Pydantic schemas for Task API responses."""

from datetime import datetime
from pydantic import BaseModel, ConfigDict

from src.app.models.task import TaskStatus


class TaskResponse(BaseModel):
    """Schema for representing a task in API responses."""
    id: int
    project_id: int
    title: str
    description: str | None
    status: TaskStatus
    deadline: datetime | None
    created_at: datetime
    closed_at: datetime | None = None

    # Create the schema from an ORM model
    model_config = ConfigDict(from_attributes=True)