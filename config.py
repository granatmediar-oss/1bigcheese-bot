import os

# Читаем из Railway Variables (Settings → Variables)
# Если переменная не задана — используем значение по умолчанию для теста
BOT_TOKEN    = os.getenv("BOT_TOKEN", "")
ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID", "292828575"))
PDF_LINK     = os.getenv("PDF_LINK", "https://bigcheeses.org/30phrases.pdf")
BOOKING_LINK = os.getenv("BOOKING_LINK", "https://bigcheeses.org/#start")
