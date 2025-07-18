import os
import requests

PAGE_ACCESS_TOKEN = os.getenv("FB_PAGE_TOKEN")
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

def send_buttons_1(recipient_id):
    payload = {
        "recipient": {"id": recipient_id},
        "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "button",
                    "text": "Что вас интересует?",
                    "buttons": [
                        {"type": "postback", "title": "📋 Кейсы", "payload": "CASES"},
                        {"type": "postback", "title": "🤖 Создать бота/агента", "payload": "CREATE_BOT"},
                        {"type": "postback", "title": "⚙️ Доработать бота/агента", "payload": "CONFIGURE_BOT"}

                    ]
                }
            }
        }
    }
    send_message(payload)

def send_buttons_2(recipient_id):
    payload = {
        "recipient": {"id": recipient_id},
        "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "button",
                    "text": "Можно почитать:",
                    "buttons": [
                        {"type": "postback", "title": "🧠 Что мы делаем", "payload": "CAPABILITIES"},
                        {"type": "postback", "title": "💸 Цены", "payload": "PRICING"},
                        {"type": "postback", "title": "❓ FAQ", "payload": "FAQ"}

                    ]
                }
            }
        }
    }
    send_message(payload)

# def send_quick_replies(recipient_id):
#     payload = {
#         "recipient": {"id": recipient_id},
#         "message": {
#             "text": "Быстрые действия:",  # текст обязателен для quick_replies
#             "quick_replies": [
#                 {"content_type": "text", "title": "Что мы делаем", "payload": "CAPABILITIES"},
#                 {"content_type": "text", "title": "Цены", "payload": "PRICING"},
#                 {"content_type": "text", "title": "FAQ", "payload": "FAQ"},
#             ]
#         }
#     }
#     send_message(payload)

