"""
Big Cheese Languages — Telegram Bot v3
Новое: двуязычный (RU/EN), выбор языка при /start
"""
import logging, sqlite3, asyncio, os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (Application, CommandHandler, CallbackQueryHandler,
                           MessageHandler, filters, ContextTypes)
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import config, messages as msg

PDF_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "30_phrases.pdf")
DB_PATH  = os.path.join(os.path.dirname(os.path.abspath(__file__)), "users.db")

logging.basicConfig(format="%(asctime)s | %(levelname)s | %(message)s", level=logging.INFO)
log = logging.getLogger(__name__)

# ── БД ────────────────────────────────────────────────────────────
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS users (
        user_id     INTEGER PRIMARY KEY,
        username    TEXT, first_name TEXT,
        lang        TEXT DEFAULT 'ru',
        segment     TEXT DEFAULT NULL,
        subscribed  TEXT DEFAULT CURRENT_TIMESTAMP,
        day2_sent   INTEGER DEFAULT 0,
        day4_sent   INTEGER DEFAULT 0,
        day6_sent   INTEGER DEFAULT 0,
        day7_sent   INTEGER DEFAULT 0,
        clicked_cta INTEGER DEFAULT 0
    )""")
    conn.commit(); conn.close()
    log.info("DB ready: %s", DB_PATH)

def save_user(uid, username, first_name):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO users (user_id,username,first_name) VALUES (?,?,?)",
              (uid, username, first_name))
    conn.commit(); conn.close()

def set_lang(uid, lang):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE users SET lang=? WHERE user_id=?", (lang, uid))
    conn.commit(); conn.close()

def set_segment(uid, segment):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE users SET segment=? WHERE user_id=?", (segment, uid))
    conn.commit(); conn.close()

def mark_cta(uid):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE users SET clicked_cta=1 WHERE user_id=?", (uid,))
    conn.commit(); conn.close()

def get_user(uid):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT lang, segment, subscribed, username, first_name, clicked_cta FROM users WHERE user_id=?", (uid,))
    row = c.fetchone(); conn.close()
    return row  # (lang, segment, subscribed, username, first_name, clicked_cta)

def get_users_for_day(day_col, hours_min):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(f"""SELECT user_id, lang, segment, clicked_cta FROM users
        WHERE {day_col}=0 AND segment IS NOT NULL
        AND datetime(subscribed,'+{hours_min} hours') <= datetime('now')""")
    rows = c.fetchall(); conn.close()
    return rows

def mark_day_sent(uid, day_col):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(f"UPDATE users SET {day_col}=1 WHERE user_id=?", (uid,))
    conn.commit(); conn.close()

def db_stats():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM users")
    total = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM users WHERE segment IS NOT NULL")
    seg = c.fetchone()[0]
    conn.close()
    return total, seg

# ── КЛАВИАТУРЫ ────────────────────────────────────────────────────
def kb_lang():
    return InlineKeyboardMarkup([[
        InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_ru"),
        InlineKeyboardButton("🇬🇧 English", callback_data="lang_en"),
    ]])

def kb_segment(lang):
    btns = msg.BTN_SEGMENT[lang]
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(btns[0], callback_data="seg_relocation")],
        [InlineKeyboardButton(btns[1], callback_data="seg_career")],
        [InlineKeyboardButton(btns[2], callback_data="seg_other")],
    ])

def kb_when(lang):
    btns = msg.BTN_WHEN[lang]
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(btns[0], callback_data="when_soon")],
        [InlineKeyboardButton(btns[1], callback_data="when_half")],
        [InlineKeyboardButton(btns[2], callback_data="when_thinking")],
    ])

def kb_career(lang):
    btns = msg.BTN_CAREER[lang]
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(btns[0], callback_data="goal_speak")],
        [InlineKeyboardButton(btns[1], callback_data="goal_write")],
        [InlineKeyboardButton(btns[2], callback_data="goal_interview")],
    ])

def kb_other(lang):
    btns = msg.BTN_OTHER[lang]
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(btns[0], callback_data="other_yes")],
        [InlineKeyboardButton(btns[1], callback_data="other_no")],
    ])

def kb_cta(lang):
    btns = msg.BTN_CTA[lang]
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(btns[0], callback_data="cta_book")],
        [InlineKeyboardButton(btns[1], callback_data="cta_question")],
    ])

# ── ХЭНДЛЕРЫ ──────────────────────────────────────────────────────
async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    save_user(user.id, user.username, user.first_name)
    log.info("START: %s @%s", user.id, user.username)
    await update.message.reply_text(
        "Выбери язык / Choose language:",
        reply_markup=kb_lang()
    )

async def handle_lang(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    uid = query.from_user.id
    lang = "ru" if query.data == "lang_ru" else "en"
    set_lang(uid, lang)

    name = f" {query.from_user.first_name}" if query.from_user.first_name else ""
    await query.edit_message_text(
        msg.DAY0_WELCOME[lang].format(name=name),
        parse_mode="HTML"
    )
    await asyncio.sleep(1)
    try:
        with open(PDF_PATH,"rb") as f:
            await ctx.bot.send_document(
                chat_id=uid, document=f,
                filename="BigCheese_30_phrases.pdf",
                caption="📄 30 phrases for housing, bank, doctor & neighbours.\n🇪🇸 Spanish · 🇮🇹 Italian · 🇬🇧 English"
            )
    except FileNotFoundError:
        log.warning("PDF not found")
    await asyncio.sleep(1)
    await ctx.bot.send_message(uid, msg.DAY0_SEGMENT[lang],
                               reply_markup=kb_segment(lang), parse_mode="HTML")

async def handle_segment(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    uid = query.from_user.id
    row = get_user(uid)
    lang = row[0] if row else "ru"
    seg_map = {"seg_relocation":"relocation","seg_career":"career","seg_other":"other"}
    seg = seg_map.get(query.data)
    if seg:
        set_segment(uid, seg)
        confirm = msg.SEG_CONFIRM[lang][seg]
        await query.edit_message_text(confirm+"\n\n"+msg.DAY0_CONFIRM[lang], parse_mode="HTML")
        log.info("Segment: %s → %s [%s]", uid, seg, lang)

async def handle_answers(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    uid = query.from_user.id
    row = get_user(uid)
    lang = row[0] if row else "ru"
    ans = msg.ANSWERS[lang].get(query.data)
    if ans:
        await query.edit_message_text(ans)

async def handle_cta(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    uid = query.from_user.id
    row = get_user(uid)
    lang = row[0] if row else "ru"

    if query.data == "cta_book":
        mark_cta(uid)
        await query.edit_message_text(msg.CTA_BOOKED[lang], parse_mode="HTML")
        log.info("CTA booked: %s [%s]", uid, lang)
        # Уведомление Дарье
        try:
            u = query.from_user
            seg = row[1] or "other"
            subscribed = row[2][:10] if row[2] else "—"
            username = row[3] or str(uid)
            flag = "🇷🇺" if lang=="ru" else "🌍"
            seg_label = msg.SEGMENT_LABELS[lang].get(seg, seg)
            mention = f"<a href='tg://user?id={uid}'>{u.first_name or uid}</a>"
            await ctx.bot.send_message(
                config.ADMIN_CHAT_ID,
                msg.ADMIN_NOTIFICATION.format(
                    flag=flag, mention=mention, lang=lang.upper(),
                    segment=seg_label, subscribed=subscribed, username=username
                ), parse_mode="HTML"
            )
        except Exception as e:
            log.warning("Admin notify error: %s", e)

    elif query.data == "cta_question":
        resp = "Напиши свой вопрос — Дарья ответит лично в течение 24 часов 🙂" if lang=="ru" \
               else "Write your question — Darya will reply personally within 24 hours 🙂"
        await query.edit_message_text(resp)

async def handle_text(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = update.message.text
    row = get_user(user.id)
    lang = row[0] if row else "ru"
    try:
        await ctx.bot.send_message(config.ADMIN_CHAT_ID,
            f"💬 @{user.username or user.id} ({user.first_name}) [{lang.upper()}]:\n\n{text}")
    except Exception as e:
        log.warning("Forward error: %s", e)
    await update.message.reply_text(msg.FREE_TEXT_REPLY[lang])

# ── ПЛАНИРОВЩИК ───────────────────────────────────────────────────
async def send_scheduled(bot):
    total, seg = db_stats()
    log.info("⏰ Tick | users:%d seg:%d", total, seg)

    for day_col, hours, get_content in [
        ("day2_sent", 48,  lambda l,s,_: (msg.DAY2[l][s], kb_when(l) if s=="relocation" else kb_career(l) if s=="career" else kb_other(l))),
        ("day4_sent", 96,  lambda l,s,_: (msg.DAY4[l][s], None)),
        ("day6_sent", 144, lambda l,s,_: (msg.DAY6[l],    kb_cta(l))),
        ("day7_sent", 168, lambda l,s,clicked: (None,None) if clicked else (msg.DAY7[l], kb_cta(l))),
    ]:
        users = get_users_for_day(day_col, hours)
        log.info("%s queue: %d", day_col, len(users))
        for uid, lang, segment, clicked in users:
            if not segment: continue
            try:
                text, kb = get_content(lang, segment, clicked)
                if text is None:
                    mark_day_sent(uid, day_col); continue
                await bot.send_message(uid, text, reply_markup=kb, parse_mode="HTML")
                mark_day_sent(uid, day_col)
                log.info("%s → %d [%s/%s]", day_col, uid, lang, segment)
            except Exception as e:
                log.warning("%s error %d: %s", day_col, uid, e)

# ── MAIN ──────────────────────────────────────────────────────────
def main():
    init_db()
    app = Application.builder().token(config.BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_lang,    pattern="^lang_"))
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
        log.info("✅ Scheduler started")
        await send_scheduled(application.bot)

    app.post_init = on_startup
    log.info("🤖 Bot v3 starting (RU/EN)...")
    app.run_polling(allowed_updates=Update.ALL_TYPES, drop_pending_updates=True)

if __name__ == "__main__":
    main()
