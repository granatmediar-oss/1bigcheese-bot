import os

# Railway Variables (Settings -> Variables)
# Required:
# BOT_TOKEN = token from @BotFather
# ADMIN_CHAT_ID = Telegram ID of Darya / admin chat
# Optional:
# PDF_LINK, BOOKING_LINK

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID", "292828575"))
PDF_LINK = os.getenv("PDF_LINK", "https://b1gcheese.ru/30phrases.pdf")
BOOKING_LINK = os.getenv("BOOKING_LINK", "https://b1gcheese.ru/#start")
