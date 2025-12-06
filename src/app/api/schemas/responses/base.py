"""Base Pydantic models for standardized API responses."""

from typing import Generic, TypeVar

from pydantic import BaseModel
from pydantic.generics import GenericModel

DataType = TypeVar("DataType")


class SuccessResponse(GenericModel, Generic[DataType]):
    """Standard success response wrapper."""
    status: str = "success"
    data: DataType


class ErrorResponse(BaseModel):
    """Standard error response wrapper."""
    status: str = "error"
    message: str
    code: int