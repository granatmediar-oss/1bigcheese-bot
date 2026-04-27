"""
Big Cheese Languages — Telegram Bot
Автоматическая 7-дневная воронка с сегментацией
Запуск: python bot.py
"""

import logging
import sqlite3
import asyncio
import os
from datetime import datetime, timedelta
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, filters, ContextTypes
)
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import config
import messages as msg

# Путь к PDF (в той же папке что и bot.py)
PDF_PATH = os.path.join(os.path.dirname(__file__), "30_phrases.pdf")

# ── ЛОГИРОВАНИЕ ──────────────────────────────────────────────────────────────
logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(message)s",
    level=logging.INFO
)
log = logging.getLogger(__name__)

# ── БАЗА ДАННЫХ ───────────────────────────────────────────────────────────────
def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id     INTEGER PRIMARY KEY,
            username    TEXT,
            first_name  TEXT,
            segment     TEXT DEFAULT NULL,
            subscribed  TEXT DEFAULT CURRENT_TIMESTAMP,
            day2_sent   INTEGER DEFAULT 0,
            day4_sent   INTEGER DEFAULT 0,
            day6_sent   INTEGER DEFAULT 0,
            day7_sent   INTEGER DEFAULT 0,
            clicked_cta INTEGER DEFAULT 0,
            stage       TEXT DEFAULT 'new'
        )
    """)
    conn.commit()
    conn.close()

def save_user(user_id, username, first_name):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("""
        INSERT OR IGNORE INTO users (user_id, username, first_name)
        VALUES (?, ?, ?)
    """, (user_id, username, first_name))
    conn.commit()
    conn.close()

def set_segment(user_id, segment):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("UPDATE users SET segment=?, stage='segmented' WHERE user_id=?",
              (segment, user_id))
    conn.commit()
    conn.close()

def mark_cta_clicked(user_id):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("UPDATE users SET clicked_cta=1 WHERE user_id=?", (user_id,))
    conn.commit()
    conn.close()

def get_users_for_day(day_col, hours_min, hours_max):
    """Возвращает юзеров у которых пора отправлять сообщение"""
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute(f"""
        SELECT user_id, segment, clicked_cta FROM users
        WHERE {day_col} = 0
        AND segment IS NOT NULL
        AND datetime(subscribed, '+{hours_min} hours') <= datetime('now')
        AND datetime(subscribed, '+{hours_max} hours') > datetime('now')
    """)
    rows = c.fetchall()
    conn.close()
    return rows

def mark_day_sent(user_id, day_col):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute(f"UPDATE users SET {day_col}=1 WHERE user_id=?", (user_id,))
    conn.commit()
    conn.close()

def get_all_unsegmented():
    """Юзеры кто подписался но не выбрал сегмент — напомнить"""
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("""
        SELECT user_id FROM users
        WHERE segment IS NULL
        AND datetime(subscribed, '+2 hours') <= datetime('now')
    """)
    rows = c.fetchall()
    conn.close()
    return rows

# ── КЛАВИАТУРЫ ────────────────────────────────────────────────────────────────
def kb_segment():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🏠 Переезд за рубеж",   callback_data="seg_relocation")],
        [InlineKeyboardButton("💼 Карьера и работа",   callback_data="seg_career")],
        [InlineKeyboardButton("🌍 Другое",             callback_data="seg_other")],
    ])

def kb_when_moving():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📅 До 3 месяцев",    callback_data="when_soon")],
        [InlineKeyboardButton("📅 Через полгода",   callback_data="when_half")],
        [InlineKeyboardButton("🤔 Пока думаю",      callback_data="when_thinking")],
    ])

def kb_career_goal():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🎤 Говорить свободно",       callback_data="goal_speak")],
        [InlineKeyboardButton("📝 Писать письма",           callback_data="goal_write")],
        [InlineKeyboardButton("💼 Пройти собеседование",    callback_data="goal_interview")],
    ])

def kb_other_selfcheck():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ Да, это про меня",          callback_data="other_yes")],
        [InlineKeyboardButton("❌ Нет, у меня другая ситуация", callback_data="other_no")],
    ])

def kb_cta():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ Записаться на урок",  callback_data="cta_book")],
        [InlineKeyboardButton("❓ Есть вопрос",         callback_data="cta_question")],
    ])

# ── ХЭНДЛЕРЫ ─────────────────────────────────────────────────────────────────
async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    save_user(user.id, user.username, user.first_name)
    log.info(f"New user: {user.id} @{user.username}")

    # Сообщение 0.1 — Приветствие + PDF как файл
    await update.message.reply_text(
        msg.DAY0_WELCOME.format(name=f" {user.first_name}" if user.first_name else ""),
        parse_mode="HTML"
    )

    # Отправляем PDF прямо в чат — файл скачивают в 3x чаще чем переходят по ссылке
    await asyncio.sleep(1)
    try:
        with open(PDF_PATH, "rb") as pdf_file:
            await update.message.reply_document(
                document=pdf_file,
                filename="BigCheese_30_фраз.pdf",
                caption="📄 Сохрани — пригодится. 30 фраз для аренды, банка, врача и соседей.\n\n🇪🇸 Испанский · 🇮🇹 Итальянский · 🇬🇧 Английский"
            )
    except FileNotFoundError:
        log.warning("PDF not found — sending text fallback")
        await update.message.reply_text(f"📄 PDF: {config.PDF_LINK}")

    await asyncio.sleep(2)

    # Сообщение 0.2 — Сегментация
    await update.message.reply_text(
        msg.DAY0_SEGMENT,
        reply_markup=kb_segment(),
        parse_mode="HTML"
    )

async def handle_segment(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    data = query.data

    segment_map = {
        "seg_relocation": "relocation",
        "seg_career":     "career",
        "seg_other":      "other",
    }

    if data in segment_map:
        segment = segment_map[data]
        set_segment(user_id, segment)

        confirm_map = {
            "relocation": "🏠 Отлично! Буду присылать самое важное для переезда.",
            "career":     "💼 Понял! Сфокусируемся на языке для карьеры и работы.",
            "other":      "🌍 Хорошо! Пришлю универсальный контент — найдём что тебе нужно.",
        }
        await query.edit_message_text(
            confirm_map[segment] + "\n\n" + msg.DAY0_CONFIRM,
            parse_mode="HTML"
        )
        log.info(f"User {user_id} → segment: {segment}")

async def handle_day2_answers(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    responses = {
        "when_soon":    "Значит, времени немного. Правильно что начинаешь сейчас — за 8 недель можно выйти на разговорный уровень ✅",
        "when_half":    "Полгода — хорошо. Успеем подготовиться основательно. Главное начать ✅",
        "when_thinking":"Думать — нормально. Но чем раньше начнёшь — тем спокойнее будет сам переезд ✅",
        "goal_speak":   "Говорить свободно — это и есть главное. Именно на это мы и тренируем с первого урока ✅",
        "goal_write":   "Деловая переписка — это конкретный навык. Отработаем шаблоны и формулировки ✅",
        "goal_interview":"Собеседование — чёткая цель. Будем готовиться именно к этому формату ✅",
        "other_yes":    "Слышим тебя. Именно с этим мы и работаем 🙂",
        "other_no":     "Расскажи в чём ситуация — Дарья ответит лично. Напиши просто текстом 👇",
    }

    if data in responses:
        await query.edit_message_text(responses[data], parse_mode="HTML")

async def handle_cta(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    data = query.data

    if data == "cta_book":
        mark_cta_clicked(user_id)
        await query.edit_message_text(
            msg.CTA_BOOKED,
            parse_mode="HTML"
        )
        log.info(f"User {user_id} → CTA clicked (booked)")

    elif data == "cta_question":
        await query.edit_message_text(
            "Напиши свой вопрос — Дарья ответит лично в течение 24 часов 🙂",
            parse_mode="HTML"
        )

async def handle_free_text(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    """Любое текстовое сообщение от пользователя"""
    user = update.effective_user
    text = update.message.text
    log.info(f"Message from {user.id}: {text[:50]}")

    # Пересылаем Дарье (в личку или в отдельный чат)
    try:
        await ctx.bot.send_message(
            chat_id=config.ADMIN_CHAT_ID,
            text=f"💬 Сообщение от @{user.username or user.id}:\n\n{text}"
        )
    except Exception as e:
        log.warning(f"Can't forward to admin: {e}")

    await update.message.reply_text(
        "Получила! Дарья ответит тебе в течение 24 часов 🙂\n\n"
        "Пока — посмотри PDF со фразами если ещё не смотрела 👉 " + config.PDF_LINK
    )

# ── SCHEDULER — АВТОМАТИЧЕСКИЕ СООБЩЕНИЯ ─────────────────────────────────────
async def send_scheduled(bot):
    """Запускается каждый час — проверяет кому пора что отправить"""

    # День 2 (48–72 часа после подписки)
    for user_id, segment, _ in get_users_for_day("day2_sent", 48, 72):
        try:
            text_map = {
                "relocation": (msg.DAY2_RELOCATION, kb_when_moving()),
                "career":     (msg.DAY2_CAREER, kb_career_goal()),
                "other":      (msg.DAY2_OTHER, kb_other_selfcheck()),
            }
            text, kb = text_map.get(segment, (msg.DAY2_OTHER, kb_other_selfcheck()))
            await bot.send_message(user_id, text, reply_markup=kb, parse_mode="HTML")
            mark_day_sent(user_id, "day2_sent")
            log.info(f"Day2 sent to {user_id} [{segment}]")
        except Exception as e:
            log.warning(f"Day2 error for {user_id}: {e}")

    # День 4 (96–120 часов)
    for user_id, segment, _ in get_users_for_day("day4_sent", 96, 120):
        try:
            text_map = {
                "relocation": msg.DAY4_RELOCATION,
                "career":     msg.DAY4_CAREER,
                "other":      msg.DAY4_OTHER,
            }
            text = text_map.get(segment, msg.DAY4_OTHER)
            await bot.send_message(user_id, text, parse_mode="HTML")
            mark_day_sent(user_id, "day4_sent")
            log.info(f"Day4 sent to {user_id} [{segment}]")
        except Exception as e:
            log.warning(f"Day4 error for {user_id}: {e}")

    # День 6 (144–168 часов) — главный оффер
    for user_id, segment, _ in get_users_for_day("day6_sent", 144, 168):
        try:
            await bot.send_message(user_id, msg.DAY6_OFFER,
                                   reply_markup=kb_cta(), parse_mode="HTML")
            mark_day_sent(user_id, "day6_sent")
            log.info(f"Day6 sent to {user_id}")
        except Exception as e:
            log.warning(f"Day6 error for {user_id}: {e}")

    # День 7 (168–192 часа) — дожим, только если не кликнул CTA
    for user_id, segment, clicked in get_users_for_day("day7_sent", 168, 192):
        if not clicked:
            try:
                await bot.send_message(user_id, msg.DAY7_FOLLOWUP,
                                       reply_markup=kb_cta(), parse_mode="HTML")
                mark_day_sent(user_id, "day7_sent")
                log.info(f"Day7 sent to {user_id} (no CTA click)")
            except Exception as e:
                log.warning(f"Day7 error for {user_id}: {e}")

# ── MAIN ──────────────────────────────────────────────────────────────────────
def main():
    init_db()
    log.info("Database initialized")

    app = Application.builder().token(config.BOT_TOKEN).build()

    # Хэндлеры
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_segment,    pattern="^seg_"))
    app.add_handler(CallbackQueryHandler(handle_day2_answers, pattern="^(when_|goal_|other_)"))
    app.add_handler(CallbackQueryHandler(handle_cta,        pattern="^cta_"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_free_text))

    # Планировщик
    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        lambda: asyncio.create_task(send_scheduled(app.bot)),
        "interval",
        hours=1,
        id="daily_sender"
    )

    async def post_init(application):
        scheduler.start()
        log.info("Scheduler started — checking every hour")

    app.post_init = post_init

    log.info("Bot started. Press Ctrl+C to stop.")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
