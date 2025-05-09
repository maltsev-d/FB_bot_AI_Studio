import requests
import json
import time
from dotenv import load_dotenv
import os
import subprocess
import re

load_dotenv()  # Загружаем переменные из .env

PAGE_ACCESS_TOKEN = os.getenv("PAGE_ACCESS_TOKEN")  # Получаем ACCESS_TOKEN из .env
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")  # Получаем VERIFY_TOKEN из .env

# Ждём ngrok
time.sleep(2)

# Получаем публичный URL
result = subprocess.run(["curl", "http://localhost:4040/api/tunnels"], capture_output=True)
urls = result.stdout.decode()
match = re.search(r'"public_url":"(https:[^"]+)"', urls)
if not match:
    raise Exception("ngrok URL not found!")

ngrok_url = match.group(1)
print("Public ngrok URL:", ngrok_url)

# Обновляем webhook
url = f"https://graph.facebook.com/v19.0/APP_ID/subscriptions"
headers = {"Content-Type": "application/json"}
payload = {
    "object": "page",
    "callback_url": f"{ngrok_url}/webhook",
    "verify_token": VERIFY_TOKEN,
    "fields": "messages,messaging_postbacks",
    "access_token": PAGE_ACCESS_TOKEN
}
r = requests.post(url, headers=headers, data=json.dumps(payload))
print("FB webhook response:", r.text)
