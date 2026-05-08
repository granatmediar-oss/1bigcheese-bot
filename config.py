import os

# Railway Variables
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID", "292828575"))
PDF_LINK = os.getenv("PDF_LINK", "https://bigcheeses.org/30phrases.pdf")
BOOKING_LINK = os.getenv("BOOKING_LINK", "https://bigcheeses.org/#start")

# Test funnel schedule.
# TEST_MODE=1: Day2/4/6/7 messages are sent after 2/4/6/7 minutes.
# TEST_MODE=0: production schedule is 48/96/144/168 hours.
TEST_MODE = os.getenv("TEST_MODE", "1")
