"""
Big Cheese Languages — Telegram Bot v2
Исправления:
- Окна отправки: >= hours_min (без верхней границы — не пропускаем)
- Планировщик запускается через post_init (правильный способ для PTB 20.7)
- Полное логирование каждого шага
- Первый прогон сразу при запуске
"""

import logging
import sqlite3
import asyncio
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, filters, ContextTypes
)
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import config
import messages as msg

PDF_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "30_phrases.pdf")
DB_PATH  = os.path.join(os.path.dirname(os.path.abspath(__file__)), "users.db")

logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(message)s",
    level=logging.INFO
)
log = logging.getLogger(__name__)

# ── БД ───────────────────────────────────────────────────────────────────────
def init_db():
    conn = sqlite3.connect(DB_PATH)
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
    log.info("DB ready: %s", DB_PATH)

def save_user(user_id, username, first_name):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO users (user_id, username, first_name) VALUES (?,?,?)",
              (user_id, username, first_name))
    conn.commit()
    conn.close()

def set_segment(user_id, segment):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE users SET segment=?, stage='segmented' WHERE user_id=?", (segment, user_id))
    conn.commit()
    conn.close()

def mark_cta_clicked(user_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE users SET clicked_cta=1 WHERE user_id=?", (user_id,))
    conn.commit()
    conn.close()

def get_users_for_day(day_col, hours_min):
    """ИСПРАВЛЕНО: >= hours_min, нет верхней границы — не пропускаем при сбоях"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(f"""
        SELECT user_id, segment, clicked_cta FROM users
        WHERE {day_col} = 0
          AND segment IS NOT NULL
          AND datetime(subscribed, '+{hours_min} hours') <= datetime('now')
    """)
    rows = c.fetchall()
    conn.close()
    return rows

def mark_day_sent(user_id, day_col):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(f"UPDATE users SET {day_col}=1 WHERE user_id=?", (user_id,))
    conn.commit()
    conn.close()

def db_stats():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM users")
    total = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM users WHERE segment IS NOT NULL")
    segmented = c.fetchone()[0]
    conn.close()
    return total, segmented

# ── КЛАВИАТУРЫ ───────────────────────────────────────────────────────────────
def kb_segment():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🏠 Переезд за рубеж",  callback_data="seg_relocation")],
        [InlineKeyboardButton("💼 Карьера и работа",  callback_data="seg_career")],
        [InlineKeyboardButton("🌍 Другое",            callback_data="seg_other")],
    ])
def kb_when_moving():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📅 До 3 месяцев",  callback_data="when_soon")],
        [InlineKeyboardButton("📅 Через полгода", callback_data="when_half")],
        [InlineKeyboardButton("🤔 Пока думаю",    callback_data="when_thinking")],
    ])
def kb_career_goal():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🎤 Говорить свободно",     callback_data="goal_speak")],
        [InlineKeyboardButton("📝 Писать письма",         callback_data="goal_write")],
        [InlineKeyboardButton("💼 Пройти собеседование",  callback_data="goal_interview")],
    ])
def kb_other():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ Да, это про меня",            callback_data="other_yes")],
        [InlineKeyboardButton("❌ Нет, другая ситуация",        callback_data="other_no")],
    ])
def kb_cta():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ Записаться на урок", callback_data="cta_book")],
        [InlineKeyboardButton("❓ Есть вопрос",        callback_data="cta_question")],
    ])

# ── ХЭНДЛЕРЫ ─────────────────────────────────────────────────────────────────
async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    save_user(user.id, user.username, user.first_name)
    log.info("START: %s @%s", user.id, user.username)

    await update.message.reply_text(
        msg.DAY0_WELCOME.format(name=f" {user.first_name}" if user.first_name else ""),
        parse_mode="HTML"
    )
    await asyncio.sleep(1)

    try:
        with open(PDF_PATH, "rb") as f:
            await update.message.reply_document(
                document=f, filename="BigCheese_30_фраз.pdf",
                caption="📄 Сохрани — пригодится.\n30 фраз для аренды, банка, врача и соседей.\n\n🇪🇸 Испанский · 🇮🇹 Итальянский · 🇬🇧 Английский"
            )
    except FileNotFoundError:
        log.warning("PDF not found: %s", PDF_PATH)

    await asyncio.sleep(1)
    await update.message.reply_text(msg.DAY0_SEGMENT, reply_markup=kb_segment(), parse_mode="HTML")

async def handle_segment(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    uid = query.from_user.id
    seg_map = {"seg_relocation":"relocation","seg_career":"career","seg_other":"other"}
    seg = seg_map.get(query.data)
    if seg:
        set_segment(uid, seg)
        confirm = {
            "relocation": "🏠 Отлично! Буду присылать самое важное для переезда.",
            "career":     "💼 Понял! Сфокусируемся на языке для карьеры.",
            "other":      "🌍 Хорошо! Пришлю полезный контент.",
        }
        await query.edit_message_text(confirm[seg]+"\n\n"+msg.DAY0_CONFIRM, parse_mode="HTML")
        log.info("Segment: %s → %s", uid, seg)

async def handle_answers(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    r = {
        "when_soon":"Значит, времени немного. Правильно что начинаешь сейчас ✅",
        "when_half":"Полгода — хорошо. Успеем подготовиться основательно ✅",
        "when_thinking":"Думать — нормально. Но чем раньше начнёшь — тем спокойнее переезд ✅",
        "goal_speak":"Говорить свободно — именно это тренируем с первого урока ✅",
        "goal_write":"Деловая переписка — конкретный навык. Отработаем ✅",
        "goal_interview":"Собеседование — чёткая цель. Готовим именно к этому ✅",
        "other_yes":"Слышим тебя. Именно с этим работаем 🙂",
        "other_no":"Расскажи свою ситуацию — Дарья ответит лично. Напиши текстом 👇",
    }
    if query.data in r:
        await query.edit_message_text(r[query.data])

async def handle_cta(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    uid = query.from_user.id

    if query.data == "cta_book":
        mark_cta_clicked(uid)
        await query.edit_message_text(msg.CTA_BOOKED, parse_mode="HTML")
        log.info("CTA booked: %s", uid)

        # Уведомление Дарье — получает данные пользователя
        try:
            user = query.from_user
            # Получаем сегмент из БД
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute("SELECT segment, subscribed FROM users WHERE user_id=?", (uid,))
            row = c.fetchone()
            conn.close()
            segment = row[0] if row else "unknown"
            subscribed = row[1][:10] if row else "—"

            mention = f"<a href='tg://user?id={uid}'>{user.first_name or uid}</a>"
            username = user.username or str(uid)
            seg_label = msg.SEGMENT_LABELS.get(segment, segment)

            await ctx.bot.send_message(
                chat_id=config.ADMIN_CHAT_ID,
                text=msg.ADMIN_NOTIFICATION.format(
                    mention=mention,
                    segment=seg_label,
                    subscribed=subscribed,
                    username=username
                ),
                parse_mode="HTML"
            )
            log.info("Admin notified about CTA: %s", uid)
        except Exception as e:
            log.warning("Admin notification error: %s", e)

    elif query.data == "cta_question":
        await query.edit_message_text("Напиши свой вопрос — Дарья ответит лично в течение 24 часов 🙂")

async def handle_text(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = update.message.text
    try:
        await ctx.bot.send_message(
            config.ADMIN_CHAT_ID,
            f"💬 @{user.username or user.id} ({user.first_name}):\n\n{text}"
        )
    except Exception as e:
        log.warning("Admin forward error: %s", e)
    await update.message.reply_text(
        "Получила! Дарья ответит в течение 24 часов 🙂\n\n"
        "Пока ждёшь — посмотри наш канал 👉 https://t.me/BigCheeseLanguages"
    )

# ── ПЛАНИРОВЩИК ──────────────────────────────────────────────────────────────
async def send_scheduled(bot):
    total, segmented = db_stats()
    log.info("⏰ Scheduler tick | users: %d | segmented: %d", total, segmented)

    async def send_day(label, day_col, hours_min, get_text_fn):
        users = get_users_for_day(day_col, hours_min)
        log.info("%s queue: %d users", label, len(users))
        for uid, segment, clicked in users:
            try:
                result = get_text_fn(segment, clicked)
                if result is None:
                    mark_day_sent(uid, day_col)
                    continue
                text, kb = result
                await bot.send_message(uid, text, reply_markup=kb, parse_mode="HTML")
                mark_day_sent(uid, day_col)
                log.info("%s sent → %d [%s]", label, uid, segment)
            except Exception as e:
                log.warning("%s error %d: %s", label, uid, e)

    def get_day2(seg, _):
        m = {"relocation":(msg.DAY2_RELOCATION,kb_when_moving()),
             "career":(msg.DAY2_CAREER,kb_career_goal()),
             "other":(msg.DAY2_OTHER,kb_other())}
        return m.get(seg, (msg.DAY2_OTHER, kb_other()))

    def get_day4(seg, _):
        m = {"relocation":msg.DAY4_RELOCATION,"career":msg.DAY4_CAREER,"other":msg.DAY4_OTHER}
        return (m.get(seg, msg.DAY4_OTHER), None)

    def get_day6(seg, _):
        return (msg.DAY6_OFFER, kb_cta())

    def get_day7(seg, clicked):
        if clicked:
            return None  # пропустить — уже записался
        return (msg.DAY7_FOLLOWUP, kb_cta())

    await send_day("Day2", "day2_sent", 48,  get_day2)
    await send_day("Day4", "day4_sent", 96,  get_day4)
    await send_day("Day6", "day6_sent", 144, get_day6)
    await send_day("Day7", "day7_sent", 168, get_day7)

# ── MAIN ─────────────────────────────────────────────────────────────────────
def main():
    init_db()
    app = Application.builder().token(config.BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_segment, pattern="^seg_"))
    app.add_handler(CallbackQueryHandler(handle_answers, pattern="^(when_|goal_|other_)"))
    app.add_handler(CallbackQueryHandler(handle_cta,     pattern="^cta_"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")

    async def on_startup(application):
        scheduler.add_job(
            lambda: asyncio.ensure_future(send_scheduled(application.bot)),
            "interval", hours=1, id="sender", replace_existing=True
        )
        scheduler.start()
        log.info("✅ Scheduler started — every 1 hour")
        # Прогон сразу при старте — догоняем пропущенные
        await send_scheduled(application.bot)

    app.post_init = on_startup

    log.info("🤖 Bot polling started")
    app.run_polling(allowed_updates=Update.ALL_TYPES, drop_pending_updates=True)

if __name__ == "__main__":
    main()
