from flask import Flask, request, abort, jsonify
from dotenv import load_dotenv
import os
import json

load_dotenv()

app = Flask(__name__)
VERIFY_TOKEN = os.getenv("FB_VERIFY_TOKEN")

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
        try:
            data = request.get_json(force=True)
            print("📩 Входящий POST-запрос:")
            print(json.dumps(data, indent=2, ensure_ascii=False))
            return jsonify({"status": "received"}), 200
        except Exception as e:
            print(f"❌ Ошибка обработки JSON: {e}")
            abort(400, description="Invalid JSON")

if __name__ == "__main__":
    app.run(port=5000, debug=True)
