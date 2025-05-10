# run_ngrok.py
import os
from dotenv import load_dotenv
from pyngrok import ngrok

load_dotenv()

NGROK_AUTH_TOKEN = os.getenv("NGROK_AUTH_TOKEN")

print("[🔄] Подключаю ngrok...")
ngrok.set_auth_token(NGROK_AUTH_TOKEN)

# Открываем туннель на порт 5000
public_url = ngrok.connect(5000, "http")

print(f"[✅] ngrok запущен! Публичный URL для webhook: {public_url}")
print("[🧩] Не забудь указать этот URL в настройках webhook на Facebook.")

# Блокируем поток, чтобы не завершался скрипт
input("\n[🛑] Нажми Enter для остановки ngrok...\n")
ngrok.kill()
