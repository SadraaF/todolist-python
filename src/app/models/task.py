"""ORM model for a Task."""

from datetime import datetime
from typing import Literal

from sqlalchemy import DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from src.app.db.base import Base

TaskStatus = Literal["todo", "doing", "done"] # Defining a specific type for type safety

class Task(Base):
    """A single task within a project."""
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    project_id: Mapped[int] = mapped_column(Integer, ForeignKey("projects.id"))
    title: Mapped[str] = mapped_column(String(30), nullable=False)
    description: Mapped[str] = mapped_column(String(150), nullable=True)
    status: Mapped[TaskStatus] = mapped_column(String, default="todo", nullable=False)
    deadline: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    closed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


    def __repr__(self) -> str:
        return f"<Task(id={self.id}, title='{self.title}')>"