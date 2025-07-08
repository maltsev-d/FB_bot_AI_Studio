from flask import Flask, request
import json
from utils import send_text, send_buttons, send_quick_replies
from responses import RESPONSES

app = Flask(__name__)

# handle_postback — обрабатывает нажатия кнопок с payload из Facebook
def handle_postback(sender_id, payload):
    print(f"[handle_postback] sender_id={sender_id}, payload={payload}")

    if payload == "CREATE_BOT":
        send_text(sender_id, RESPONSES["create_bot"])
    elif payload == "CONFIGURE_BOT":
        send_text(sender_id, RESPONSES["configure_bot"])
    elif payload == "PRICE_INFO":
        send_text(sender_id, RESPONSES["pricing"])
    elif payload == "SHOW_CASES":
        send_text(sender_id, RESPONSES["cases"])
    elif payload == "CONTACT_US":
        send_text(sender_id, RESPONSES["contact"])
    else:
        send_text(sender_id, "🤔 Извини, я не понял эту команду. Попробуй выбрать одну из кнопок.")
        send_buttons(sender_id)


# handle_message — обрабатывает любые входящие сообщения (текст, quick_replies и др.)
def handle_message(sender_id, message):
    print(f"[handle_message] sender_id={sender_id}, message={message}")

    # Попробуем получить текст из сообщения
    text = message.get("text", "").strip().lower() if isinstance(message, dict) else ""

    # Если пользователь выбрал быстрый ответ (quick reply)
    if "quick_reply" in message:
        payload = message["quick_reply"].get("payload")
        if payload:
            handle_postback(sender_id, payload)
            return

    # Простая логика на ключевые слова
    if "привет" in text or "hi" in text or "hello" in text:
        send_text(sender_id, RESPONSES["greeting"])
        send_quick_replies(sender_id)
    elif text in ["создать бота", "create bot", "create_bot"]:
        send_text(sender_id, RESPONSES["create_bot"])
    elif text in ["доработать бота", "configure bot", "configure_bot"]:
        send_text(sender_id, RESPONSES["configure_bot"])
    elif text in ["кейсы", "cases"]:
        send_text(sender_id, RESPONSES["cases"])
    elif text in ["цены", "цена", "price"]:
        send_text(sender_id, RESPONSES["pricing"])
    elif text in ["связаться", "контакты", "contact"]:
        send_text(sender_id, RESPONSES["contact"])
    else:
        send_text(sender_id, "Я не понял твоё сообщение. Попробуй выбрать одну из кнопок.")
        send_buttons(sender_id)

@app.route('/webhook', methods=['GET'])
def verify():
    from os import getenv
    VERIFY_TOKEN = getenv("FB_VERIFY_TOKEN", "your_verify_token")
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200
    return "Verification failed", 403

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    print(f"[LOG] Incoming: {json.dumps(data, indent=2, ensure_ascii=False)}")
    if data.get("object") == "page":
        for entry in data.get("entry", []):
            for event in entry.get("messaging", []):
                sender_id = event["sender"]["id"]
                if event.get("postback"):
                    payload = event["postback"].get("payload")
                    if payload:
                        handle_postback(sender_id, payload)
                elif event.get("message"):
                    handle_message(sender_id, event["message"])
    return "ok", 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
