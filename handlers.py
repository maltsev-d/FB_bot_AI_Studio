from flask import Flask, request
import json
from utils import send_text, send_buttons, send_quick_replies
from responses import RESPONSES

app = Flask(__name__)

def handle_postback(sender_id, payload):
    response = RESPONSES.get(payload.lower())
    if response:
        send_text(sender_id, response)
    else:
        send_text(sender_id, "Выбери, пожалуйста, кнопку ниже.")
    send_buttons(sender_id)

def handle_message(sender_id, message):
    text = message.get("text", "").lower()
    quick_payload = message.get("quick_reply", {}).get("payload", "").upper()

    if any(greet in text for greet in ["привет", "hi", "hello"]):
        send_text(sender_id, RESPONSES["greeting"])
        send_buttons(sender_id)
        send_quick_replies(sender_id)

    elif quick_payload == "CALL_ME":
        send_text(sender_id, "👌 Я уже вас заметил, жди ответа!")

    elif quick_payload in RESPONSES:
        send_text(sender_id, RESPONSES[quick_payload])
        send_buttons(sender_id)

    else:
        send_text(sender_id, "Не понял тебя, выбери из кнопок ниже.")
        send_buttons(sender_id)
        send_quick_replies(sender_id)

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
