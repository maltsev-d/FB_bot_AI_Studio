import os
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)


VERIFY_TOKEN = os.getenv("FB_VERIFY_TOKEN", "your_verify_token")
PAGE_ACCESS_TOKEN = os.getenv("FB_PAGE_TOKEN", "your_page_access_token")

# Верификация webhook от Facebook
@app.route('/webhook', methods=['GET'])
def verify():
    mode = request.args.get("hub.mode")
    challenge = request.args.get("hub.challenge")
    token = request.args.get("hub.verify_token")
    if mode == "subscribe" and challenge:
        if token == VERIFY_TOKEN:
            return challenge, 200
        else:
            return "Verification token mismatch", 403
    return "Hello from AI Bots Studio", 200

# Отправка сообщений в Facebook Messenger
def send_message(recipient_id, message_data):
    if not PAGE_ACCESS_TOKEN or PAGE_ACCESS_TOKEN == "your_page_access_token":
        print("PAGE_ACCESS_TOKEN не задан, сообщение не отправлено.")
        return
    url = f"https://graph.facebook.com/v15.0/me/messages?access_token={PAGE_ACCESS_TOKEN}"
    payload = {
        "recipient": {"id": recipient_id},
        "message": message_data
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code != 200:
        print(f"Ошибка отправки сообщения: {response.text}")

# Обработка сообщений и меню
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    print(f"Incoming data: {data}")

    if data.get("object") == "page":
        for entry in data.get("entry", []):
            for messaging_event in entry.get("messaging", []):
                sender_id = messaging_event["sender"]["id"]
                # Проверяем есть ли текстовое сообщение
                if messaging_event.get("message") and "text" in messaging_event["message"]:
                    text = messaging_event["message"]["text"].lower()
                    handle_message(sender_id, text)
                elif messaging_event.get("postback") and "payload" in messaging_event["postback"]:
                    payload = messaging_event["postback"]["payload"]
                    handle_postback(sender_id, payload)

    return "OK", 200

# Обработка текстовых сообщений
def handle_message(sender_id, text):
    greeting_keywords = ["привет", "здравствуй", "hello", "hi"]
    if any(word in text for word in greeting_keywords):
        send_welcome(sender_id)
    elif text in ["1", "создать нового бота", "создать"]:
        send_text(sender_id, "Отлично, расскажи вкратце, что хочешь автоматизировать? Чем точнее — тем лучше.")
        send_main_menu(sender_id)
    elif text in ["2", "настроить существующего", "настроить"]:
        send_text(sender_id, "Покажи, с чем возникли сложности. Поможем довести до ума и добавить фишек.")
        send_main_menu(sender_id)
    elif text in ["3", "узнать про возможности", "возможности"]:
        send_text(sender_id, "Мы работаем с Python, GPT, Telethon, голосовыми интерфейсами и интеграциями с любыми сервисами. Можем почти всё.")
        send_main_menu(sender_id)
    elif text in ["4", "связаться с экспертом", "эксперт"]:
        send_text(sender_id, "Оставь контакты — с тобой свяжется реальный человек, а не бот (ну, почти).")
        send_main_menu(sender_id)
    else:
        send_text(sender_id, "Извини, не понял. Выбери пункт из меню ниже.")
        send_main_menu(sender_id)

# Обработка нажатий на кнопки postback
def handle_postback(sender_id, payload):
    if payload == "CREATE_BOT":
        send_text(sender_id, "Отлично, расскажи вкратце, что хочешь автоматизировать? Чем точнее — тем лучше.")
        send_main_menu(sender_id)
    elif payload == "CONFIGURE_BOT":
        send_text(sender_id, "Покажи, с чем возникли сложности. Поможем довести до ума и добавить фишек.")
        send_main_menu(sender_id)
    elif payload == "LEARN_CAPABILITIES":
        send_text(sender_id, "Мы работаем с Python, GPT, Telethon, голосовыми интерфейсами и интеграциями с любыми сервисами. Можем почти всё.")
        send_main_menu(sender_id)
    elif payload == "CONTACT_EXPERT":
        send_text(sender_id, "Оставь контакты — с тобой свяжется реальный человек, а не бот (ну, почти).")
        send_main_menu(sender_id)
    else:
        send_text(sender_id, "Неизвестная команда. Пожалуйста, выбери опцию из меню.")
        send_main_menu(sender_id)

# Приветственное сообщение + кнопки меню
def send_welcome(recipient_id):
    text = ("Привет! Ты в AI Bots Studio — здесь рождаются умные агенты, которые автоматизируют, интегрируют и дают результат. "
            "Что сегодня собираемся прокачать?")
    buttons = [
        {"type": "postback", "title": "🚀 Создать нового бота", "payload": "CREATE_BOT"},
        {"type": "postback", "title": "🔧 Настроить существующего", "payload": "CONFIGURE_BOT"},
        {"type": "postback", "title": "📚 Узнать про возможности", "payload": "LEARN_CAPABILITIES"},
        {"type": "postback", "title": "📞 Связаться с экспертом", "payload": "CONTACT_EXPERT"}
    ]
    send_button_template(recipient_id, text, buttons)

# Основное меню (то же самое)
def send_main_menu(recipient_id):
    text = "Выбери действие из меню ниже:"
    buttons = [
        {"type": "postback", "title": "🚀 Создать нового бота", "payload": "CREATE_BOT"},
        {"type": "postback", "title": "🔧 Настроить существующего", "payload": "CONFIGURE_BOT"},
        {"type": "postback", "title": "📚 Узнать про возможности", "payload": "LEARN_CAPABILITIES"},
        {"type": "postback", "title": "📞 Связаться с экспертом", "payload": "CONTACT_EXPERT"}
    ]
    send_button_template(recipient_id, text, buttons)

# Отправка текста
def send_text(recipient_id, text):
    message = {"text": text}
    send_message(recipient_id, message)

# Отправка кнопок шаблона
def send_button_template(recipient_id, text, buttons):
    message = {
        "attachment": {
            "type": "template",
            "payload": {
                "template_type": "button",
                "text": text,
                "buttons": buttons
            }
        }
    }
    send_message(recipient_id, message)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
