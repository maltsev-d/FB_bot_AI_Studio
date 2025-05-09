from flask import Flask, request
import requests
import os
from dotenv import load_dotenv

load_dotenv()  # Загружаем переменные из .env

app = Flask(__name__)

VERIFY_TOKEN = os.getenv('VERIFY_TOKEN')  # Получаем VERIFY_TOKEN из .env
PAGE_ACCESS_TOKEN = os.getenv('PAGE_ACCESS_TOKEN')  # Получаем PAGE_ACCESS_TOKEN из .env


@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")

        print(f"GET request received. Mode: {mode}, Token: {token}, Challenge: {challenge}")  # Логирование GET запроса

        if mode == "subscribe" and token == VERIFY_TOKEN:
            print("WEBHOOK VERIFIED")  # Подтверждение вебхука
            return challenge, 200
        else:
            print("Verification token mismatch!")  # Ошибка в токене
            return "Verification token mismatch", 403

    if request.method == 'POST':
        data = request.get_json()
        print(f"POST request received. Data: {data}")  # Логирование POST запроса

        for entry in data.get('entry', []):
            for message_event in entry.get('messaging', []):
                sender_id = message_event['sender']['id']
                print(f"Received message from sender ID: {sender_id}")  # Логирование отправителя

                if 'message' in message_event:
                    message_text = message_event['message'].get('text')
                    if message_text:
                        print(f"Received message text: {message_text}")  # Логирование текста сообщения
                        if 'привет' in message_text.lower():
                            send_message(sender_id, "Привет! Рад тебя видеть 😎")
                        else:
                            send_message(sender_id, "Какой у тебя опыт работы?")

        return "EVENT_RECEIVED", 200


def send_message(recipient_id, message_text):
    url = 'https://graph.facebook.com/v17.0/me/messages'
    headers = {'Content-Type': 'application/json'}
    payload = {
        'recipient': {'id': recipient_id},
        'message': {'text': message_text},
        'messaging_type': 'RESPONSE',
        'access_token': PAGE_ACCESS_TOKEN
    }
    response = requests.post(url, headers=headers, json=payload)
    print("Message sent:", response.status_code, response.text)  # Логирование отправки сообщения


if __name__ == '__main__':
    app.run(debug=False, port=5000)
