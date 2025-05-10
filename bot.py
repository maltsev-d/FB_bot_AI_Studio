import os
import requests
from flask import Flask, request, jsonify
import json

app = Flask(__name__)

# Убедитесь, что вы установили переменные окружения с токеном и верификационным кодом
VERIFY_TOKEN = os.getenv("FB_VERIFY_TOKEN", "your_verify_token")  # Замените на ваш токен
PAGE_ACCESS_TOKEN = os.getenv("FB_PAGE_TOKEN", "your_page_access_token")  # Замените на ваш токен страницы

# Facebook Webhook Verification
@app.route('/webhook', methods=['GET'])
def verify():
    # Проверка верификационного кода
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return request.args["hub.challenge"], 200
        return "Verification token mismatch", 403
    return "Hello, this is the webhook", 200

# Обработка входящих сообщений
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    print(f"Received data: {json.dumps(data, indent=2)}")  # Логирование входящих данных для отладки

    if data.get("object") == "page":
        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:
                sender_id = messaging_event["sender"]["id"]
                if messaging_event.get("message"):
                    # Приветствие при получении сообщения
                    send_greeting(sender_id)
                    send_buttons(sender_id)
                    send_quick_replies(sender_id)

    return "OK", 200

# Отправка приветствия
def send_greeting(recipient_id):
    message_data = {
        "recipient": {"id": recipient_id},
        "message": {
            "text": "Привет! Добро пожаловать в нашу шаурму-империю! 🍗"
        }
    }
    call_send_api(message_data)

# Отправка кнопок
def send_buttons(recipient_id):
    message_data = {
        "recipient": {"id": recipient_id},
        "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "button",
                    "text": "Что вы хотите заказать?",
                    "buttons": [
                        {
                            "type": "postback",
                            "title": "Шаурма с курицей",
                            "payload": "SHAVERMA_CHICKEN"
                        },
                        {
                            "type": "postback",
                            "title": "Шаурма с говядиной",
                            "payload": "SHAVERMA_BEEF"
                        },
                        {
                            "type": "postback",
                            "title": "Шаурма с овощами",
                            "payload": "SHAVERMA_VEG"
                        }
                    ]
                }
            }
        }
    }
    call_send_api(message_data)

# Отправка quick replies
def send_quick_replies(recipient_id):
    message_data = {
        "recipient": {"id": recipient_id},
        "message": {
            "text": "Вы хотите заказать сейчас?",
            "quick_replies": [
                {
                    "content_type": "text",
                    "title": "Да, хочу!",
                    "payload": "ORDER_YES"
                },
                {
                    "content_type": "text",
                    "title": "Не сейчас",
                    "payload": "ORDER_NO"
                }
            ]
        }
    }
    call_send_api(message_data)

# Функция отправки сообщения через API
def call_send_api(message_data):
    response = requests.post(
        f'https://graph.facebook.com/v12.0/me/messages?access_token={PAGE_ACCESS_TOKEN}',
        json=message_data
    )
    if response.status_code != 200:
        print(f"Failed to send message: {response.text}")

if __name__ == '__main__':
    app.run(debug=True, port=5000)