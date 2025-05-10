# bot.py
import os
import json
import requests
from dotenv import load_dotenv
from flask import Flask, request

load_dotenv()

app = Flask(__name__)

VERIFY_TOKEN = os.getenv("FB_VERIFY_TOKEN")
PAGE_ACCESS_TOKEN = os.getenv("FB_PAGE_TOKEN")


def log_request(req):
    print("\n[📨] Запрос:")
    print(f"URL: {req.url}")
    print(f"Headers: {dict(req.headers)}")
    print(f"Body: {req.get_data(as_text=True)}")


@app.route("/", methods=["GET"])
def verify():
    log_request(request)
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    if mode == "subscribe" and token == VERIFY_TOKEN:
        print("[🔓] Webhook подтверждён!")
        return challenge, 200
    else:
        print("[❌] Неверный VERIFY_TOKEN")
        return "Forbidden", 403


@app.route("/", methods=["POST"])
def webhook():
    log_request(request)
    data = request.get_json()
    print(f"[🔍] Получено событие: {json.dumps(data, indent=2, ensure_ascii=False)}")

    if data.get("object") == "page":
        for entry in data.get("entry", []):
            for messaging_event in entry.get("messaging", []):
                sender_id = messaging_event["sender"]["id"]
                if "message" in messaging_event:
                    message_text = messaging_event["message"].get("text", "")
                    send_message(sender_id, f"Привет! Ты написал: {message_text}")
                elif "postback" in messaging_event:
                    payload = messaging_event["postback"]["payload"]
                    send_message(sender_id, f"Ты нажал кнопку: {payload}")

    return "OK", 200


def send_message(recipient_id, text):
    url = "https://graph.facebook.com/v18.0/me/messages"
    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": text}
    }
    params = {"access_token": PAGE_ACCESS_TOKEN}
    print(f"[➡️] Отправка сообщения пользователю {recipient_id}: {text}")
    response = requests.post(url, params=params, json=payload)
    print(f"[✅] Ответ Facebook: {response.status_code} {response.text}")


if __name__ == "__main__":
    print("[🚀] Бот запущен на http://localhost:5000")
    app.run(port=5000)
