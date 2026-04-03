"""Подключение к Google Sheets."""

import gspread
from oauth2client.service_account import ServiceAccountCredentials

from app.core.config import settings

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]

creds = ServiceAccountCredentials.from_json_keyfile_name(
    settings.CREDENTIALS_FILE, scope
)
client = gspread.authorize(creds)
sheet = client.open_by_key(settings.SHEET_ID).worksheet(settings.SHEET_NAME)
