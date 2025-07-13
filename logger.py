import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

GOOGLE_CREDS_FILE = "creds.json"  # путь к твоему JSON-ключу
GOOGLE_SHEET_NAME = "FB Messages Log"  # название Google-таблицы

def get_sheet():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_CREDS_FILE, scope)
    client = gspread.authorize(creds)
    sheet = client.open(GOOGLE_SHEET_NAME).sheet1

    # Проверим, есть ли заголовки
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
