import os
import base64
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

GOOGLE_SHEET_NAME = "FB Messages Log"
GOOGLE_CREDS_PATH = "/tmp/creds.json"

def write_google_creds():
    creds_base64 = os.getenv("GOOGLE_CREDS_BASE64")
    if not creds_base64:
        raise Exception("GOOGLE_CREDS_BASE64 не установлена")

    with open(GOOGLE_CREDS_PATH, "wb") as f:
        f.write(base64.b64decode(creds_base64))


def get_sheet():
    if not os.path.exists(GOOGLE_CREDS_PATH):
        write_google_creds()

    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_CREDS_PATH, scope)
    client = gspread.authorize(creds)
    sheet = client.open(GOOGLE_SHEET_NAME).sheet1

    # Проверка на заголовки
    if not sheet.row_values(1):
        sheet.append_row(["Дата", "ID пользователя", "Имя", "Сообщение", "Payload"])

    return sheet


def log_message(user_id: str, name: str, message: str = "", payload: str = ""):
    sheet = get_sheet()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sheet.append_row([now, str(user_id), name, message, payload])


def is_new_user(user_id: str) -> bool:
    try:
        sheet = get_sheet()
        user_ids = sheet.col_values(2)[1:]  # колонка с ID, пропускаем заголовок
        return str(user_id) not in user_ids
    except Exception as e:
        print(f"[ERROR] is_new_user: {e}")
        return False
