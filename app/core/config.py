"""Настройки приложения."""

import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Класс настроек."""

    SHEET_ID = os.getenv("SHEET_ID")
    SHEET_NAME = os.getenv("SHEET_NAME", "Лист1")
    CREDENTIALS_FILE = os.getenv("CREDENTIALS_FILE", "credentials.json")


settings = Settings()
