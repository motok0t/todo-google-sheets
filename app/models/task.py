"""Модели задач."""

from typing import Optional
from pydantic import BaseModel


class Task(BaseModel):
    """Модель задачи."""

    id: Optional[int] = None
    task: str
    status: str = "pending"
