// ═══════════════════════════════════════════════════════════════════
// Big Cheese Languages — Apps Script
// Что делает:
// 1. При отправке формы → переносит заявку в RU/EN Leads
// 2. → отправляет email на два адреса
// 3. → отправляет уведомление в Telegram Дарье
// ═══════════════════════════════════════════════════════════════════

const MANAGER_EMAILS = ["i@rusovich-top.ru", "granatmediar@gmail.com"];

// ⚠️ ЗАМЕНИТЬ на реальные значения:
const TELEGRAM_BOT_TOKEN = "8610604385:AAEBMxXk6Kv0-57_jM5XYW9s_r98J7Rgk5o";
const TELEGRAM_CHAT_ID   = "ВСТАВИТЬ_ID_ДАРЬИ"; // @userinfobot → число

const CONFIG = {
  "RU Form Responses": {
    targetSheet: "RU Leads",
    flow: "RU",
    status: "Новая заявка",
    emoji: "🇷🇺"
  },
  "EN Form Responses": {
    targetSheet: "EN Leads",
    flow: "EN",
    status: "New lead",
    emoji: "🌍"
  }
};

// ─── ГЛАВНАЯ ФУНКЦИЯ ──────────────────────────────────────────────
function onFormSubmit(e) {
  const sourceSheet     = e.range.getSheet();
  const sourceSheetName = sourceSheet.getName();
  const config          = CONFIG[sourceSheetName];

  if (!config) return; // не наша вкладка — выходим

  const row        = e.range.getRow();
  const lastColumn = sourceSheet.getLastColumn();
  const values     = sourceSheet.getRange(row, 1, 1, lastColumn).getValues()[0];

  // Разбираем поля формы (порядок: Timestamp, Имя, Контакт, Email, Цель, Язык)
  const timestamp = values[0] || new Date();
  const name      = values[1] || "";
  const contact   = values[2] || "";
  const email     = values[3] || "";
  const goal      = values[4] || "";
  const languages = values[5] || "";

  // Форматируем дату
  const dateStr = Utilities.formatDate(
    new Date(timestamp),
    Session.getScriptTimeZone(),
    "dd.MM.yyyy HH:mm"
  );

  const ss          = SpreadsheetApp.getActiveSpreadsheet();
  const targetSheet = ss.getSheetByName(config.targetSheet);

  if (!targetSheet) {
    throw new Error("Target sheet not found: " + config.targetSheet);
  }

  // ── 1. Записываем в CRM ──────────────────────────────────────────
  const newRow = [
    dateStr,
    name,
    contact,
    email,
    goal,
    languages,
    config.status,
    "Google Form",  // источник
    ""              // примечания
  ];
  targetSheet.appendRow(newRow);

  // ── 2. Email-уведомление ─────────────────────────────────────────
  sendLeadEmailNotification(config, dateStr, name, contact, email, goal, languages);

  // ── 3. Telegram-уведомление ──────────────────────────────────────
  sendTelegramNotification(config, dateStr, name, contact, email, goal, languages);
}

// ─── EMAIL ────────────────────────────────────────────────────────
function sendLeadEmailNotification(config, dateStr, name, contact, email, goal, languages) {
  const isRU = config.flow === "RU";

  const subject = isRU
    ? `🎯 Новая заявка с сайта — ${name}`
    : `🎯 New lead from website — ${name}`;

  const body = isRU
    ? `Новая заявка на бесплатный урок!

Имя:       ${name}
Контакт:   ${contact}
Email:     ${email}
Язык:      ${languages}
Цель:      ${goal}
Дата:      ${dateStr}
Источник:  Google Form (RU)

Открыть CRM:
https://docs.google.com/spreadsheets/d/1yWz9mP6nylfVJrs6VmyiasBQGEVKiQLE6MKu1E3eO8M/edit`
    : `New free lesson request!

Name:      ${name}
Contact:   ${contact}
Email:     ${email}
Language:  ${languages}
Goal:      ${goal}
Date:      ${dateStr}
Source:    Google Form (EN)

Open CRM:
https://docs.google.com/spreadsheets/d/1yWz9mP6nylfVJrs6VmyiasBQGEVKiQLE6MKu1E3eO8M/edit`;

  MANAGER_EMAILS.forEach(emailAddr => {
    try {
      MailApp.sendEmail(emailAddr, subject, body);
    } catch(err) {
      Logger.log("Email error to " + emailAddr + ": " + err);
    }
  });
}

// ─── TELEGRAM ─────────────────────────────────────────────────────
function sendTelegramNotification(config, dateStr, name, contact, email, goal, languages) {
  if (TELEGRAM_CHAT_ID === "ВСТАВИТЬ_ID_ДАРЬИ") {
    Logger.log("Telegram CHAT_ID not set — skipping");
    return;
  }

  const isRU = config.flow === "RU";

  const text = isRU
    ? `${config.emoji} <b>Новая заявка с сайта!</b>\n\n` +
      `👤 <b>Имя:</b> ${name}\n` +
      `📱 <b>Контакт:</b> ${contact}\n` +
      `📧 <b>Email:</b> ${email || "—"}\n` +
      `🎯 <b>Язык:</b> ${languages}\n` +
      `💬 <b>Цель:</b> ${goal || "—"}\n` +
      `📅 <b>Дата:</b> ${dateStr}\n\n` +
      `<i>Напиши ему первой — он ждёт 🙂</i>`
    : `${config.emoji} <b>New lead from website!</b>\n\n` +
      `👤 <b>Name:</b> ${name}\n` +
      `📱 <b>Contact:</b> ${contact}\n` +
      `📧 <b>Email:</b> ${email || "—"}\n` +
      `🎯 <b>Language:</b> ${languages}\n` +
      `💬 <b>Goal:</b> ${goal || "—"}\n` +
      `📅 <b>Date:</b> ${dateStr}\n\n` +
      `<i>Reach out first — they're waiting 🙂</i>`;

  const url     = `https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage`;
  const payload = {
    chat_id:    TELEGRAM_CHAT_ID,
    text:       text,
    parse_mode: "HTML"
  };

  try {
    const response = UrlFetchApp.fetch(url, {
      method:      "post",
      contentType: "application/json",
      payload:     JSON.stringify(payload),
      muteHttpExceptions: true
    });
    Logger.log("Telegram response: " + response.getContentText());
  } catch(err) {
    Logger.log("Telegram error: " + err);
  }
}

// ─── ТЕСТ (запускать вручную из редактора) ────────────────────────
function testTelegramNotification() {
  const testConfig = { flow: "RU", emoji: "🧪" };
  sendTelegramNotification(
    testConfig,
    "05.05.2026 12:00",
    "Тест Тестов",
    "@test_user",
    "test@email.com",
    "Испанский",
    "Переезд"
  );
}
