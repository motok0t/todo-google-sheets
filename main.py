"""
FastAPI приложение для управления списком задач (To-Do) с хранением данных в Google Sheets.

Эндпоинты:
- GET /tasks - получение всех задач
- POST /tasks - создание новой задачи
- PUT /tasks/{task_id} - обновление статуса задачи
- DELETE /tasks/{task_id} - удаление задачи
"""

import os
from typing import List, Optional

import gspread
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from oauth2client.service_account import ServiceAccountCredentials
from pydantic import BaseModel

# Загрузка переменных окружения из файла .env
load_dotenv()

# Настройки приложения
SHEET_ID = os.getenv("SHEET_ID")
SHEET_NAME = os.getenv("SHEET_NAME", "Лист1")

# Подключение к Google Sheets через сервисный аккаунт
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]
creds = ServiceAccountCredentials.from_json_keyfile_name(
    "credentials.json", scope
)
client = gspread.authorize(creds)
sheet = client.open_by_key(SHEET_ID).worksheet(SHEET_NAME)

app = FastAPI(title="To-Do API with Google Sheets")


class Task(BaseModel):
    """Модель задачи."""
    id: Optional[int] = None
    task: str
    status: str = "pending"


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


@app.get("/tasks", response_model=List[Task])
def get_tasks() -> List[Task]:
    """Возврат всех задач из Google Sheets."""
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


@app.post("/tasks", response_model=Task, status_code=201)
def create_task(task: Task) -> Task:
    """Создание новой задачи и добавление её в таблицу."""
    new_id = get_next_id()
    row = [new_id, task.task, task.status]
    sheet.append_row(row)
    task.id = new_id
    return task


@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: Task) -> dict:
    """
    Обновление статуса задачи.

    Args:
        task_id: идентификатор задачи.
        task: объект с новым статусом.

    Raises:
        HTTPException: 404 при отсутствии задачи.
    """
    cell = sheet.find(str(task_id), in_column=1)
    if not cell:
        raise HTTPException(status_code=404, detail="Task not found")
    # Обновление статуса в третьей колонке (status)
    sheet.update_cell(cell.row, 3, task.status)
    return {"message": "Task updated"}


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int) -> dict:
    """
    Удаление задачи из таблицы.

    Args:
        task_id: идентификатор задачи.

    Raises:
        HTTPException: 404 при отсутствии задачи.
    """
    cell = sheet.find(str(task_id), in_column=1)
    if not cell:
        raise HTTPException(status_code=404, detail="Task not found")
    sheet.delete_rows(cell.row)
    return {"message": "Task deleted"}
