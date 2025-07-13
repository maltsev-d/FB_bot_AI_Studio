# FB Bot AI Studio

## 📦 Описание

Цифровой менеджер для Facebook Messenger, созданный AI Bots Studio.
Бот умеет приветствовать новых пользователей, показывать кнопки с вариантами
действий, логировать сообщения в Google Sheets и уведомлять администратора elegram.

---
## Возможности

- ✉️ Обработка сообщений и postback-событий
- 🌐 Приветствие новых пользователей
- ⌚ Логирование в Google Sheets (в т.ч. ID, имя, сообщение, payload)
- 💬 Уведомление в Telegram о новом пользователе
- 🔹 Две группы кнопок ("Что вас интересует?" и "Можно почитать:")
---
## 🧠 Структура проекта

```
.
├── bot.py                 
├── handlers.py         
├── utils.py               
├── .env                   
├── responses.py 
├── logger.py          
├── .gitignore             
└── README.md              
```

## 🚀 Бысткий старт

### 1. Клонируй репозиторий

```bash
git https://github.com/maltsev-d/FB_bot_AI_Studio
cd FB_bot_AI_Studio
```

### 2. Установи зависимости

```bash
pip install -r requirements.txt
```
---

## Запуск


1. Скопируй .env.example в .env и заполни:
```
 FB_VERIFY_TOKEN=...
 FB_PAGE_TOKEN=...
 TG_BOT_TOKEN=...
 TG_ADMIN_ID=...
 GOOGLE_CREDS_BASE64=...
- ```

2. Укажи Google Sheet по имени (в logger.py)
3. Убедись, что creds.json от Google API преобразован в BASE64 и внесён в .env
4. Запусти:
```
python bot.py
```
5. А если через Render:

- Укажи build команду: pip install -r requirements.txt
- Start command: gunicorn handlers:app
- Все переменные окружения внести вручную
---
## 🧠 Автор

Проект разработан AI Bots Studio — мы делаем Telegram, WhatsApp, Instagram и Web-ботов, AI-агентов и голосовые интерфейсы под задачи бизнеса.

Telegram: [@AIBotStudio_bot](https://t.me/AIBotStudio_bot)
GitHub: [maltsev-d](github.com/maltsev-d) 😎