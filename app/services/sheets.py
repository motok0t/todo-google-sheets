"""Сервис для работы с Google Sheets."""

from app.core.database import sheet
from app.models.task import Task


def get_next_id() -> int:
    """
    Вычисление следующего доступного идентификатора задачи.

    Returns:
        int: следующий ID (максимальный существующий + 1,
            или 1 при пустой таблице).
    """
    records = sheet.get_all_records()
    if not records:
        return 1
    return max(row.get("id", 0) for row in records) + 1


def get_all_tasks() -> list[Task]:
    """Получение всех задач из Google Sheets."""
    records = sheet.get_all_records()
    tasks = []
    for row in records:
        tasks.append(
            Task(
                id=row.get("id"),
                task=row.get("task"),
                status=row.get("status")
            )
        )
    return tasks


def create_task(task: Task) -> Task:
    """Создание новой задачи в таблице."""
    new_id = get_next_id()
    row = [new_id, task.task, task.status]
    sheet.append_row(row)
    task.id = new_id
    return task


def update_task_status(task_id: int, new_status: str) -> bool:
    """Обновление статуса задачи."""
    cell = sheet.find(str(task_id), in_column=1)
    if not cell:
        return False
    sheet.update_cell(cell.row, 3, new_status)
    return True


def delete_task(task_id: int) -> bool:
    """Удаление задачи из таблицы."""
    cell = sheet.find(str(task_id), in_column=1)
    if not cell:
        return False
    sheet.delete_rows(cell.row)
    return True
