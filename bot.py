from flask import Flask, request, jsonify, abort
from dotenv import load_dotenv
import os
import json
import requests

load_dotenv()
app = Flask(__name__)

VERIFY_TOKEN = os.getenv("FB_VERIFY_TOKEN")
PAGE_ACCESS_TOKEN = os.getenv("FB_PAGE_TOKEN")
FB_API_URL = "https://graph.facebook.com/v18.0/me/messages"


@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        if token == VERIFY_TOKEN:
            return challenge, 200
        else:
            abort(403, description="Verification token mismatch")

    elif request.method == "POST":
        data = request.get_json()
        print("📩 Входящий запрос:")
        print(json.dumps(data, indent=2, ensure_ascii=False))

        # Обработка события "messages"
        if data.get("object") == "page":
            for entry in data.get("entry", []):
                for messaging_event in entry.get("messaging", []):
                    if "message" in messaging_event:
                        sender_id = messaging_event["sender"]["id"]
                        message_text = messaging_event["message"].get("text")
                        if message_text:
                            send_message(sender_id, f"Ты написал: {message_text}")
        return jsonify({"status": "ok"}), 200


def send_message(recipient_id, message_text):
    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": message_text}
    }
    headers = {
        "Content-Type": "application/json"
    }
    params = {
        "access_token": PAGE_ACCESS_TOKEN
    }

    response = requests.post(FB_API_URL, headers=headers, params=params, json=payload)
    if response.ok:
        print("✅ Ответ отправлен.")
    else:
        print("❌ Ошибка при отправке:", response.text)


if __name__ == "__main__":
    app.run(port=5000)
