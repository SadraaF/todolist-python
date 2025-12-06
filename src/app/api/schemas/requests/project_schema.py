"""Pydantic schemas for Project API requests."""

from pydantic import BaseModel, Field


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