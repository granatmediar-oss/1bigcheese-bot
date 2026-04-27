# Big Cheese Languages — Telegram Bot

Автоматическая 7-дневная воронка с сегментацией по цели.

---

## Что делает бот

- Приветствует нового подписчика и сразу даёт PDF
- Спрашивает цель: Переезд / Карьера / Другое
- Отправляет персональный контент на 2-й, 4-й, 6-й и 7-й день
- На 6-й день — главный оффер (бесплатный урок)
- На 7-й день — дожим только тем, кто не записался
- Все вопросы от учеников пересылает Дарье в Telegram

---

## Шаг 1 — Создать бота в Telegram

1. Открыть Telegram → найти @BotFather
2. Написать `/newbot`
3. Придумать название: `Big Cheese Languages`
4. Придумать username (только латиница, оканчивается на bot): `bigcheese_languages_bot`
5. BotFather пришлёт **токен** — скопировать его

---

## Шаг 2 — Узнать свой Telegram ID (для Дарьи)

1. Написать в Telegram: @userinfobot
2. Бот ответит вашим ID — скопировать число

---

## Шаг 3 — Заполнить config.py

Открыть файл `config.py` и заполнить:

```python
BOT_TOKEN = "ваш_токен_от_BotFather"
ADMIN_CHAT_ID = ваш_telegram_id  # число
PDF_LINK = "ссылка на PDF после загрузки на сайт"
BOOKING_LINK = "https://b1gcheese.ru/#form"
```

---

## Шаг 4 — Деплой на Railway (бесплатно)

Railway — бесплатный хостинг для Python-ботов. Бот работает 24/7.

### 4.1 Создать аккаунт
Зайти на [railway.app](https://railway.app) → Sign in with GitHub

### 4.2 Загрузить файлы на GitHub
1. Создать аккаунт на [github.com](https://github.com)
2. Создать новый репозиторий (New repository) → назвать `bigcheese-bot`
3. Загрузить все файлы: `bot.py`, `messages.py`, `config.py`, `requirements.txt`

### 4.3 Задеплоить на Railway
1. Railway → New Project → Deploy from GitHub repo
2. Выбрать репозиторий `bigcheese-bot`
3. Railway автоматически установит зависимости и запустит бота
4. В разделе Variables добавить переменную: `BOT_TOKEN` = ваш_токен

> ⚠️ Токен НЕ хранить в config.py при загрузке на GitHub.
> Использовать переменные окружения Railway.

### 4.4 Обновить config.py для Railway

```python
import os
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID", "0"))
PDF_LINK = os.getenv("PDF_LINK", "https://b1gcheese.ru/30phrases.pdf")
BOOKING_LINK = "https://b1gcheese.ru/#form"
```

---

## Шаг 5 — Добавить ссылку на бота везде

После деплоя ссылка на бот выглядит так:
```
https://t.me/bigcheese_languages_bot
```

Добавить:
- В закреплённое сообщение Telegram-канала
- В описание каждого YouTube-видео
- В шапку ВКонтакте
- На лендинг b1gcheese.ru как кнопку «Получить PDF бесплатно»

---

## Что настроить в messages.py

Открыть `messages.py` и заменить:
- `ССЫЛКА_НА_PDF` → реальная ссылка на PDF после загрузки
- `ССЫЛКА_НА_ФОРМУ_ЗАПИСИ` → ссылка на форму на сайте

---

## Структура файлов

```
bigcheese_bot/
├── bot.py           # Основная логика бота
├── messages.py      # Все тексты — редактировать здесь
├── config.py        # Токен и настройки
├── requirements.txt # Зависимости
└── README.md        # Эта инструкция
```

---

## Метрики — что смотреть

Через месяц работы бота:
- Подписчики бота > 50 → воронка работает
- Клики на форму (День 6) > 10% от подписчиков → хорошо
- Заявки на урок > 3 в неделю → пора масштабировать

Если заявок нет — переписываем текст Дня 6, а не весь бот.

---

Вопросы → @anastasia_russkih
