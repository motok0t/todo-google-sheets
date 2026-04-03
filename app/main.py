"""FastAPI приложение для управления списком задач."""

from fastapi import FastAPI

from app.routes import tasks

app = FastAPI(title="To-Do API with Google Sheets")

# Подключение маршрутов
app.include_router(tasks.router)
