import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import os

# Название таблицы в Google Sheets
GOOGLE_SHEET_NAME = "FB Messages Log"

# Путь к json-ключу
GOOGLE_CREDS_FILE = "creds.json"

# Настраиваем авторизацию
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_CREDS_FILE, scope)
client = gspread.authorize(creds)

# Получаем таблицу и первый лист
sheet = client.open(GOOGLE_SHEET_NAME).sheet1

# Если первая строка пустая — добавим заголовки
if not sheet.row_values(1):
    sheet.append_row(["Дата", "ID пользователя", "Имя", "Сообщение", "Payload"])

def log_message(user_id: str, name: str, message: str = "", payload: str = ""):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sheet.append_row([now, str(user_id), name, message, payload])
