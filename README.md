# Big Cheese Languages — Telegram Bot

Clean Railway-ready package.

## Files in repository root

Upload ONLY these files to GitHub repository root:

- `bot.py`
- `config.py`
- `messages.py`
- `requirements.txt`
- `Procfile`
- `runtime.txt`
- `30_phrases.pdf`
- `30_phrases_en.pdf`
- `README.md`

Do NOT upload:

- `users.db`
- old `.zip` archives
- duplicate `bot/` folder
- Apps Script files

## Railway variables

Add these variables in Railway → Service → Variables:

```text
BOT_TOKEN=your_new_token_from_BotFather
ADMIN_CHAT_ID=292828575
PDF_LINK=https://b1gcheese.ru/30_phrases.pdf
BOOKING_LINK=https://b1gcheese.ru/#start
```

Important: do not store the Telegram token inside `config.py` or README.

## Railway settings

Use:

```text
Root Directory: empty
Start Command: python bot.py
```

`Procfile` also contains:

```text
worker: python bot.py
```

## Expected logs after deploy

```text
🤖 Bot v3 starting (RU/EN)...
DB ready: /app/users.db
✅ Scheduler started
⏰ Tick | users:0 seg:0
```

## Telegram test

Open the bot and send:

```text
/start
```

Expected first response:

```text
Выбери язык / Choose language:
```

with buttons:

- 🇷🇺 Русский
- 🇬🇧 English

## Notes

The bot creates `users.db` automatically on Railway. Do not upload `users.db` to GitHub.
