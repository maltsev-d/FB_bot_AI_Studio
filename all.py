import requests
from flask import Flask, request, jsonify
import json

app = Flask(__name__)

# Токен страницы Facebook (для отправки сообщений)
PAGE_ACCESS_TOKEN = 'EAAIfHFVq0ZA4BOw27q6PBvHsO83wC5O2MYUzZCpzxk74CI4fqIRl3jtUql6KOXxZCQDWRAQwZC9XJPiEPcpJH8EZC1p4bHjODqlAe9f3E2WFM6zHShTHDZAw5pI7pzPLNBL4e72FhiNSczlf3cyWreQRgBA8Cd6kxyY5HMULoid1IXJ98ZB3uhCEzAwCOgSHpQKjD8RaCgCPMNZC6ckoqQZDZD'

# Токен вебхука (для подтверждения подключения)
WEBHOOK_VERIFY_TOKEN = '2wsFqml3NhORsfhRDCAzSepIt0Z_3pKrssGkRiAGDAXNwWyv8'
#recipient_id = 30254061267518561

# Функция отправки сообщения
def send_message(recipient_id, message_data):
    url = f'https://graph.facebook.com/v15.0/me/messages?access_token={PAGE_ACCESS_TOKEN}'
    payload = {
        'recipient': {'id': recipient_id},
        'message': message_data
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code != 200:
        print(f"Ошибка отправки сообщения: {response.text}")
    else:
        print("Сообщение отправлено!")


# Обработка GET-запроса для верификации вебхука
@app.route('/webhook', methods=['GET'])
def verify_webhook():
    # Получаем параметры запроса
    mode = request.args.get('hub.mode')
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')

    # Проверяем токен вебхука
    if mode == 'subscribe' and token == WEBHOOK_VERIFY_TOKEN:
        print('Верификация прошла успешно!')
        return str(challenge), 200
    else:
        print('Ошибка верификации')
        return 'Forbidden', 403


# Обработка POST-запроса от Facebook
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    print(json.dumps(data, indent=2, ensure_ascii=False))
    if 'entry' in data:
        for entry in data['entry']:
            for messaging_event in entry['messaging']:
                sender_id = messaging_event['sender']['id']

                # Приветственное сообщение
                send_message(sender_id, {"text": "Привет! Добро пожаловать в нашу шаурму-империю! 🍗"})
                # # Отправка сообщений по очереди
                # send_postback_message(sender_id)
                # send_image_message(sender_id)
                # #send_video_message(sender_id) #Нужна ссылка мр4
                # #send_audio_message(sender_id) #Нужна ссылка мр3
                # send_file_message(sender_id) #Только в мессенджер
                # send_button_template(sender_id)
                # send_generic_template(sender_id)
                # #send_list_template(sender_id) #Непонятная ошибка
                # #send_media_template(sender_id) #Нужна ссылка Facebook #Что это?
                # send_receipt_message(sender_id)
                # send_web_url_button(sender_id)
                # send_phone_number_button(sender_id)
                # #send_account_link_button(sender_id) #Что это?
                # #send_account_unlink_button(sender_id) #Что это?
                # #send_game_play_button(sender_id) #Что это?
                # #send_element_share_button(sender_id) #Устарела в API 4.0, нужно новую добавить
                # send_quick_replies(sender_id)

    return 'ok', 200


# Функции для различных типов сообщений

def send_postback_message(recipient_id):
    message = {
        "text": "Тест текстовое сообщение..."
    }
    send_message(recipient_id, message)


def send_image_message(recipient_id):
    image_url = 'https://shaurmama.com.ua/image/cache/catalog/assorti-450x280.jpg'  # Замени на реальный URL
    message = {
        "attachment": {
            "type": "image",
            "payload": {
                "url": image_url,
                "is_reusable": True
            }
        }
    }
    send_message(recipient_id, message)


def send_video_message(recipient_id):
    video_url = 'https://example.com/video.mp4'  # Замени на реальный URL
    message = {
        "attachment": {
            "type": "video",
            "payload": {
                "url": video_url,
                "is_reusable": True
            }
        }
    }
    send_message(recipient_id, message)


def send_audio_message(recipient_id):
    audio_url = 'https://example.com/audio.mp3'  # Замени на реальный URL
    message = {
        "attachment": {
            "type": "audio",
            "payload": {
                "url": audio_url,
                "is_reusable": True
            }
        }
    }
    send_message(recipient_id, message)


def send_file_message(recipient_id):
    file_url = 'https://zagorie.ru/upload/iblock/4ea/4eae10bf98dde4f7356ebef161d365d5.pdf'  # Замени на реальный URL
    message = {
        "attachment": {
            "type": "file",
            "payload": {
                "url": file_url
            }
        }
    }
    send_message(recipient_id, message)


def send_button_template(recipient_id):
    message = {
        "attachment": {
            "type": "template",
            "payload": {
                "template_type": "button",
                "text": "Выберите вариант:",
                "buttons": [
                    {"type": "postback", "title": "Первая кнопка", "payload": "FIRST_BUTTON"},
                    {"type": "postback", "title": "Вторая кнопка", "payload": "SECOND_BUTTON"},
                    {"type": "postback", "title": "Третья кнопка", "payload": "THIRD_BUTTON"}
                ]
            }
        }
    }
    send_message(recipient_id, message)


def send_generic_template(recipient_id):
    message = {
        "attachment": {
            "type": "template",
            "payload": {
                "template_type": "generic",
                "elements": [
                    {
                        "title": "Пример товара 1",
                        "subtitle": "Очень вкусная шаурма",
                        "image_url": "https://vseopecheni.ru/assets/cache_image/images/new/shaurma_535x400_968.webp",
                        "buttons": [{"type": "web_url", "url": "https://recipes.vseopecheni.ru/shaurma-s-ryiboj", "title": "Узнать больше"}]
                    },
                    {
                        "title": "Пример товара 2",
                        "subtitle": "Острая шаурма",
                        "image_url": "https://cafesahara.ru/upload/resize_cache/iblock/514/1200_1200_1/514a5898917fabf5e25e0cf0121fb77c.jpg",
                        "buttons": [{"type": "web_url", "url": "https://cafesahara.ru/dostavka/v-syrnom/iz-yagnyenka-v-syrnom-lavashe", "title": "Узнать больше"}]
                    },
                    {
                        "title": "Пример товара 2",
                        "subtitle": "Острая шаурма",
                        "image_url": "https://cafesahara.ru/upload/resize_cache/iblock/514/1200_1200_1/514a5898917fabf5e25e0cf0121fb77c.jpg",
                        "buttons": [{"type": "web_url", "url": "https://cafesahara.ru/dostavka/v-syrnom/iz-yagnyenka-v-syrnom-lavashe", "title": "Узнать больше"}]
                    },
                    {
                        "title": "Пример товара 2",
                        "subtitle": "Острая шаурма",
                        "image_url": "https://cafesahara.ru/upload/resize_cache/iblock/514/1200_1200_1/514a5898917fabf5e25e0cf0121fb77c.jpg",
                        "buttons": [{"type": "web_url", "url": "https://cafesahara.ru/dostavka/v-syrnom/iz-yagnyenka-v-syrnom-lavashe", "title": "Узнать больше"}]
                    },
                    {
                        "title": "Пример товара 2",
                        "subtitle": "Острая шаурма",
                        "image_url": "https://cafesahara.ru/upload/resize_cache/iblock/514/1200_1200_1/514a5898917fabf5e25e0cf0121fb77c.jpg",
                        "buttons": [{"type": "web_url", "url": "https://cafesahara.ru/dostavka/v-syrnom/iz-yagnyenka-v-syrnom-lavashe", "title": "Узнать больше"}]
                    },
                    {
                        "title": "Пример товара 2",
                        "subtitle": "Острая шаурма",
                        "image_url": "https://cafesahara.ru/upload/resize_cache/iblock/514/1200_1200_1/514a5898917fabf5e25e0cf0121fb77c.jpg",
                        "buttons": [{"type": "web_url", "url": "https://cafesahara.ru/dostavka/v-syrnom/iz-yagnyenka-v-syrnom-lavashe", "title": "Узнать больше"}]
                    }
                ]
            }
        }
    }
    send_message(recipient_id, message)


def send_list_template(recipient_id):
    message = {
        "attachment": {
            "type": "template",
            "payload": {
                "template_type": "list",
                "elements": [
                    {
                        "title": "Шаурма с курицей",
                        "subtitle": "Очень вкусная куриная шаурма",
                        "image_url": "https://st28.styapokupayu.ru/images/blog_posts/covers/000/317/229_large.jpg",
                        "buttons": [{"type": "postback", "title": "Добавить в корзину", "payload": "ADD_TO_CART"}]
                    },
                    {
                        "title": "Шаурма с говядиной",
                        "subtitle": "Очень сочная говяжья шаурма",
                        "image_url": "https://st28.styapokupayu.ru/images/blog_posts/covers/000/317/229_large.jpg",
                        "buttons": [{"type": "postback", "title": "Добавить в корзину", "payload": "ADD_TO_CART"}]
                    }
                ]
            }
        }
    }
    send_message(recipient_id, message)


def send_media_template(recipient_id):
    message = {
        "attachment": {
            "type": "template",
            "payload": {
                "template_type": "media",
                "elements": [
                    {
                        "media_type": "image",
                        "url": "https://st28.styapokupayu.ru/images/blog_posts/covers/000/317/229_large.jpg",
                        "buttons": [{"type": "postback", "title": "Посмотреть подробнее", "payload": "MORE_INFO"}]
                    }
                ]
            }
        }
    }
    send_message(recipient_id, message)


def send_receipt_message(recipient_id):
    message = {
        "attachment": {
            "type": "template",
            "payload": {
                "template_type": "receipt",
                "recipient_name": "Иван",
                "order_number": "123456",
                "currency": "USD",
                "payment_method": "Visa 1234",
                "order_url": "https://media-cdn.tripadvisor.com/media/photo-s/09/57/37/2b/caption.jpg",
                "timestamp": "1428444852",
                "elements": [
                    {"title": "Шаурма с курицей", "price": 10.00, "quantity": 1},
                    {"title": "Шаурма с говядиной", "price": 12.00, "quantity": 2}
                ],
                "address": {"street_1": "123 Main Street", "city": "Vientiane capital","state": "Vientiane", "country": "Laos", "postal_code": "01030"},
                "summary": {"subtotal": 34.00, "total_cost": 39.00}
            }
        }
    }
    send_message(recipient_id, message)

def send_web_url_button(recipient_id):
    message = {
        "attachment": {
            "type": "template",
            "payload": {
                "template_type": "button",
                "text": "Перейти на сайт",
                "buttons": [{"type":"web_url", "url": "https://www.gastronom.ru", "title": "Перейти"}]
            }
        }
    }
    send_message(recipient_id, message)


def send_phone_number_button(recipient_id):
    message = {
        "attachment": {
            "type": "template",
            "payload": {
                "template_type": "button",
                "text": "Позвоните нам",
                "buttons": [{"type": "phone_number", "title": "Позвонить", "payload": "+8562023456789"}]
            }
        }
    }
    send_message(recipient_id, message)


def send_account_link_button(recipient_id): # НЕ ПОНЯТНО ЧТО ЭТО
    message = {
        "attachment": {
            "type": "template",
            "payload": {
                "template_type": "button",
                "text": "Связать аккаунт",
                "buttons": [{"type": "account_link", "url": "https://www.facebook.com/profile.php?id=61556526222721", "title": "Связать"}]
            }
        }
    }
    send_message(recipient_id, message)


def send_account_unlink_button(recipient_id):
    message = {
        "attachment": {
            "type": "template",
            "payload": {
                "template_type": "button",
                "text": "Отключить аккаунт",
                "buttons": [{"type": "account_link", "url": "https://www.facebook.com/profile.php?id=61556526222721", "title": "Отключить"}]
            }
        }
    }
    send_message(recipient_id, message)


def send_game_play_button(recipient_id):
    message = {
        "attachment": {
            "type": "template",
            "payload": {
                "template_type": "button",
                "text": "Играть в игру",
                "buttons": [{"type": "game_play", "title": "Начать игру", "payload": "START_GAME"}]
            }
        }
    }
    send_message(recipient_id, message)


def send_element_share_button(recipient_id): # НЕ РАБОТАЕТ (API 4)
    message = {
        "attachment": {
            "type": "template",
            "payload": {
                "template_type": "button",
                "text": "Поделиться элементом",
                "buttons": [{"type": "element_share", "title": "Поделиться", "payload": "SHARE"}]
            }
        }
    }
    send_message(recipient_id, message)


def send_quick_replies(recipient_id):
    message = {
        "text": "Выберите действие",
        "quick_replies": [
            {"content_type": "text", "title": "Посмотреть меню", "payload": "MENU"},
            {"content_type": "text", "title": "Заказать сейчас", "payload": "ORDER_NOW"},
            {"content_type": "text", "title": "Контакты", "payload": "CONTACTS"}
        ]
    }
    send_message(recipient_id, message)

# Запуск приложения
if __name__ == '__main__':
    app.run(port=5000)