"""Pydantic schemas for Project API responses."""

from datetime import datetime
from pydantic import BaseModel, ConfigDict

# Note the updated import path
from .task_schema import TaskResponse


class ProjectResponse(BaseModel):
    """Schema for representing a project in API responses."""
    id: int
    name: str
    description: str | None
    created_at: datetime
    tasks: list[TaskResponse] = []

    model_config = ConfigDict(from_attributes=True)