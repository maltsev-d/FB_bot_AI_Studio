# curl_test.py
import requests
import json

NGROK_URL = "https://7005-103-43-77-30.ngrok-free.app"
VERIFY_TOKEN = "2wsFqml3NhORsfhRDCAzSepIt0Z_3pKrssGkRiAGDAXNwWyv8"


def log_response(label, response):
    print(f"\n[{label}]")
    print(f"URL: {response.url}")
    print(f"Status: {response.status_code}")
    print("Headers:", dict(response.headers))
    print("Response Body:\n", response.text)


def test_get_verification():
    print("\n[🔍] Тестируем GET верификацию webhook'а...")
    params = {
        "hub.mode": "subscribe",
        "hub.verify_token": VERIFY_TOKEN,
        "hub.challenge": "12345"
    }
    headers = {
        "ngrok-skip-browser-warning": "true"
    }
    response = requests.get(NGROK_URL, params=params, headers=headers)
    log_response("GET /verify", response)


def test_post_message():
    print("\n[💬] Тестируем POST сообщение (как будто пользователь написал боту)...")
    payload = {
        "object": "page",
        "entry": [
            {
                "messaging": [
                    {
                        "sender": {"id": "1234567890"},
                        "message": {"text": "Йо, бот! Ты работаешь?"}
                    }
                ]
            }
        ]
    }

    headers = {
        "Content-Type": "application/json",
        "ngrok-skip-browser-warning": "true"
    }

    response = requests.post(NGROK_URL, headers=headers, json=payload)
    log_response("POST /message", response)


if __name__ == "__main__":
    test_get_verification()
    test_post_message()
