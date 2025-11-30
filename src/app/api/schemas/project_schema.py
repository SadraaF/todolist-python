"""Pydantic schemas for Project resources."""

from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field

from .task_schema import TaskResponse


class ProjectBase(BaseModel):
    """Base schema for a project, containing common fields."""
    name: str = Field(..., min_length=1, max_length=30)
    description: str | None = Field(default=None, max_length=150)


class ProjectCreate(ProjectBase):
    """Schema used for creating a new project."""
    pass


class ProjectUpdate(ProjectBase):
    """Schema used for updating an existing project."""
    pass


class ProjectResponse(ProjectBase):
    """Schema for representing a project in API responses."""
    id: int
    created_at: datetime
    tasks: list[TaskResponse] = [] 

    model_config = ConfigDict(from_attributes=True)