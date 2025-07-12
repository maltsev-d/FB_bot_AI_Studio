import os
import requests

PAGE_ACCESS_TOKEN = os.getenv("FB_PAGE_TOKEN", "your_page_access_token")
FB_API_URL = f"https://graph.facebook.com/v18.0/me/messages?access_token={PAGE_ACCESS_TOKEN}"

def send_message(payload):
    response = requests.post(FB_API_URL, json=payload)
    if response.status_code != 200:
        print(f"[ERROR] Failed to send: {response.status_code} {response.text}")
    else:
        print("[SENT] Message delivered")

def send_text(recipient_id, text):
    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": text}
    }
    send_message(payload)

def send_buttons(recipient_id):
    payload = {
        "recipient": {"id": recipient_id},
        "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "button",
                    "text": "Что тебя интересует? 👇",
                    "buttons": [
                        {"type": "postback", "title": "Что мы делаем", "payload": "CAPABILITIES"},
                        {"type": "postback", "title": "Цены", "payload": "PRICING"},
                        {"type": "postback", "title": "Создать бота", "payload": "CREATE_BOT"}
                    ]
                }
            }
        }
    }
    send_message(payload)

def send_quick_replies(recipient_id):
    payload = {
        "recipient": {"id": recipient_id},
        "message": {
            "text": "👇 Быстрые действия:",
            "quick_replies": [
                {"content_type": "text", "title": "Создать бота", "payload": "CREATE_BOT"},
                {"content_type": "text", "title": "Доработать бота", "payload": "CONFIGURE_BOT"},
                {"content_type": "text", "title": "Кейсы", "payload": "CASES"},
                {"content_type": "text", "title": "Цены", "payload": "PRICING"},
                {"content_type": "text", "title": "Позвать кожанного", "payload": "CALL_ME"},
                {"content_type": "text", "title": "FAQ", "payload": "FAQ"},
            ]
        }
    }
    send_message(payload)
