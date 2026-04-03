"""Tests for To-Do API."""

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_get_tasks_empty():
    """Проверка получения списка задач."""
    response = client.get("/tasks")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_task():
    """Проверка создания задачи."""
    task_data = {"task": "Купить хлеб", "status": "pending"}
    response = client.post("/tasks", json=task_data)
    assert response.status_code == 201
    data = response.json()
    assert data["task"] == "Купить хлеб"
    assert data["status"] == "pending"
    assert "id" in data


def test_update_task():
    """Проверка обновления задачи."""
    # Создание задачи
    task_data = {"task": "Позвонить другу", "status": "pending"}
    create_response = client.post("/tasks", json=task_data)
    task_id = create_response.json()["id"]

    # Обновление статуса
    update_data = {"task": "Позвонить другу", "status": "done"}
    response = client.put(f"/tasks/{task_id}", json=update_data)
    assert response.status_code == 200
    assert response.json()["message"] == "Task updated"


def test_delete_task():
    """Проверка удаления задачи."""
    # Создание задачи
    task_data = {"task": "Временная задача", "status": "pending"}
    create_response = client.post("/tasks", json=task_data)
    task_id = create_response.json()["id"]

    # Удаление задачи
    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Task deleted"

    # Проверка отсутствия задачи
    get_response = client.get("/tasks")
    tasks = get_response.json()
    task_ids = [task["id"] for task in tasks]
    assert task_id not in task_ids
