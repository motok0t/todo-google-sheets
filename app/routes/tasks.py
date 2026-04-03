"""Маршруты для работы с задачами."""

from fastapi import APIRouter, HTTPException

from app.models.task import Task
from app.services import sheets

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/", response_model=list[Task])
def get_tasks():
    """Получение всех задач."""
    return sheets.get_all_tasks()


@router.post("/", response_model=Task, status_code=201)
def create_task(task: Task):
    """Создание новой задачи."""
    return sheets.create_task(task)


@router.put("/{task_id}")
def update_task(task_id: int, task: Task):
    """Обновление статуса задачи."""
    success = sheets.update_task_status(task_id, task.status)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task updated"}


@router.delete("/{task_id}")
def delete_task(task_id: int):
    """Удаление задачи."""
    success = sheets.delete_task(task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted"}
