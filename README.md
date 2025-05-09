# Facebook Messenger Bot с Flask и ngrok

## 📦 Описание

Этот проект — простой бот для Facebook Messenger, который:
- обрабатывает входящие сообщения
- отвечает в зависимости от текста
- работает через Flask и ngrok

Идеально подходит для демонстрации бота работодателю или на собеседовании.

---

## 🚀 Бысткий старт

### 1. Клонируй репозиторий

```bash
git clone https://github.com/yourusername/facebook-bot-demo.git
cd facebook-bot-demo
```

### 2. Установи зависимости

```bash
pip install -r requirements.txt
```

### 3. Создай файл `.env`

```ini
PAGE_ACCESS_TOKEN=твой_page_access_token
VERIFY_TOKEN=твой_verify_token
NGROK_AUTH_TOKEN=твой_ngrok_auth_token
APP_ID=твой_app_id_из_facebook
```

### 4. Запусти бота

Используй `.bat` файл, чтобы запустить Flask, ngrok и обновить webhook за один шаг:

```bash
start_bot.bat
```

---

## 🧠 Структура проекта

```
.
├── app.py                  # Основной Flask-приложение
├── ngrok_start.py         # Запуск туннеля ngrok
├── update_fb_webhook.py   # Установка webhook для Facebook
├── .env                   # Хранение токенов (не пушим в Git)
├── start_bot.bat          # Скрипт запуска всего стека
├── .gitignore             # Исключения для Git
└── README.md              # Этот файл
```

---

## 📬 Как работает бот

1. Пользователь пишет сообщение на Facebook-страницу.
2. Facebook шлёт `POST` на `https://<ngrok>.ngrok-free.app/webhook`.
3. Flask ловит событие и:
   - если сообщение содержит "привет", отвечает: **"Привет! Рад тебя видеть 😎"**
   - иначе спрашивает: **"Какой у тебя опыт работы?"**

---

## ⚠️ Важно

- **ngrok URL временный**. Чтобы он не менялся, можно оплатить платный аккаунт и получить постоянный домен.
- Facebook требует HTTPS — именно поэтому используется ngrok.

---

## 🧼 .gitignore

```gitignore
.env
ngrok_start.py
start_bot.bat
__pycache__/
*.pyc
```

---

## 🧠 Автор

Собрано братаном под ключ, чтоб можно было запускать и радоваться 😎