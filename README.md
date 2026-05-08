# Big Cheese Telegram Bot — TEST MODE package

This package is for fast QA testing of the 7-day funnel.

## Test schedule

After user selects a segment:

- Day 2 message: after 2 minutes
- Day 4 message: after 4 minutes
- Day 6 offer + CTA: after 6 minutes
- Day 7 follow-up: after 7 minutes, only if CTA was not clicked

The scheduler checks the queue every 1 minute.

## Railway Variables

Set these in Railway → Variables:

```
BOT_TOKEN=your_new_botfather_token
ADMIN_CHAT_ID=292828575
TEST_MODE=1
PDF_LINK=https://bigcheeses.org/30_phrases.pdf
BOOKING_LINK=https://bigcheeses.org/#start
```

Do not commit the real Telegram token to GitHub.

## Start Command

```
python bot.py
```

Root Directory must be empty if these files are in the repository root.

## Test flow

1. Redeploy Railway.
2. Open Telegram bot.
3. Send `/start`.
4. Choose RU or EN.
5. Choose one segment: relocation / career / other.
6. Wait 2, 4, 6, 7 minutes.
7. Check that all scheduled messages arrive.

## After test

Set Railway variable:

```
TEST_MODE=0
```

Then redeploy to return to production schedule:

- Day 2: 48 hours
- Day 4: 96 hours
- Day 6: 144 hours
- Day 7: 168 hours
```
