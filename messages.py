"""
Big Cheese Languages — тексты бота
RU и EN версии в одном файле
"""

# ══ ДЕНЬ 0 ══════════════════════════════════════════════════════════

# Первый вопрос — выбор языка интерфейса
LANG_SELECT = {
    "ru": "Выбери язык / Choose language:",
    "en": "Выбери язык / Choose language:"
}

DAY0_WELCOME = {
    "ru": """Привет{name}! 👋

Я Дарья, основатель <b>Big Cheese Languages</b>.

Здесь учим языки для реальной жизни — переезд, карьера, адаптация. С живыми носителями языка. Без учебниковой скуки.

Держи подарок сразу 🎁 — прикрепила PDF ниже.

Там фразы для аренды, банка, врача и соседей. Испанский, итальянский, английский.""",

    "en": """Hi{name}! 👋

I'm Darya, founder of <b>Big Cheese Languages</b>.

We teach languages for real life — relocation, career, everyday communication. With native speakers. No textbook boredom.

Here's a gift right away 🎁 — PDF attached below.

30 phrases for housing, bank, doctor and neighbours. Spanish, Italian, English."""
}

DAY0_SEGMENT = {
    "ru": "Чтобы я присылала именно то, что нужно тебе — скажи, для чего учишь язык?",
    "en": "To send you the most relevant content — tell me, why are you learning a language?"
}

DAY0_CONFIRM = {
    "ru": "Буду присылать полезное раз в пару дней. Без спама 🙂\n\nЕсли хочешь поговорить прямо сейчас — просто напиши. Отвечу лично.",
    "en": "I'll send useful content every couple of days. No spam 🙂\n\nIf you'd like to talk now — just write. I'll reply personally."
}

SEG_CONFIRM = {
    "ru": {
        "relocation": "🏠 Отлично! Буду присылать самое важное для переезда.",
        "career":     "💼 Понял! Сфокусируемся на языке для карьеры.",
        "other":      "🌍 Хорошо! Пришлю полезный контент.",
    },
    "en": {
        "relocation": "🏠 Great! I'll send the most important content for relocation.",
        "career":     "💼 Got it! We'll focus on language for your career.",
        "other":      "🌍 Perfect! I'll send useful content for you.",
    }
}

# ══ ДЕНЬ 2 ══════════════════════════════════════════════════════════

DAY2 = {
    "ru": {
        "relocation": """Вчера прислала тебе 30 фраз. Сегодня — чуть глубже 🙂

<b>3 ситуации, которые реально удивляют переехавших в первый месяц:</b>

1. Арендодатель говорит быстро и нет времени переспросить
2. В банке не понимают твой акцент — и ты не понимаешь их объяснения
3. Врач задаёт вопросы, которых не было в учебнике

Именно такие ситуации мы разбираем на уроках. Не «глагол ser и estar», а «как объяснить врачу что болит».

<b>Когда планируешь переезд?</b> 👇""",

        "career": """Вчера прислала тебе 30 фраз. Сегодня — конкретнее 🙂

<b>3 ситуации, где язык реально влияет на зарплату:</b>

1. Умеешь писать письма — но не можешь говорить на созвоне
2. Понимаешь задание — но боишься переспросить при коллегах
3. Собеседование прошло бы лучше, если бы не языковой барьер

Это не проблема уровня. Это проблема формата обучения.

<b>Что тебе нужно в первую очередь?</b> 👇""",

        "other": """Вчера прислала тебе 30 фраз. Сегодня хочу спросить кое-что 🙂

Многие приходят с одной историей:
<i>«Учил язык годами. Знаю слова. Открываю рот — тишина.»</i>

Это не плохая память. Это проблема формата.

<b>Узнаёшь себя?</b> 👇"""
    },
    "en": {
        "relocation": """Yesterday I sent you 30 phrases. Today — a bit deeper 🙂

<b>3 situations that genuinely surprise people in the first month abroad:</b>

1. The landlord speaks fast and there's no time to ask them to repeat
2. The bank doesn't understand your accent — and you don't understand their explanation
3. The doctor asks questions that weren't in any textbook

These are exactly the situations we work on. Not "verb conjugation theory" — but "how to explain what hurts".

<b>When are you planning to move?</b> 👇""",

        "career": """Yesterday I sent you 30 phrases. Today — more specific 🙂

<b>3 situations where language actually affects your salary:</b>

1. You can write emails — but freeze on a video call
2. You understand the task — but fear asking for clarification in front of colleagues
3. The interview would have gone better without the language barrier

This isn't about your level. It's about the wrong learning format.

<b>What do you need most right now?</b> 👇""",

        "other": """Yesterday I sent you 30 phrases. Today I want to ask something 🙂

Many people come to us with one story:
<i>"I've studied for years. I know the words. I open my mouth — silence."</i>

That's not bad memory. That's the wrong learning format.

<b>Does that sound familiar?</b> 👇"""
    }
}

# ══ ДЕНЬ 4 ══════════════════════════════════════════════════════════

DAY4 = {
    "ru": {
        "relocation": """Хочу рассказать про одну нашу ученицу.

Она планировала переезд в Барселону. Начала заниматься испанским за 3 месяца до отъезда. С нуля.

<b>Через 8 недель она:</b>
— сама договорилась об аренде квартиры
— открыла счёт в банке без переводчика
— записалась к врачу и объяснила симптомы

<i>«Без этого курса я бы потратила намного больше на посредников» — написала она после переезда.</i>

Хочешь разобраться со своей ситуацией? Первый урок бесплатно — ссылка завтра.""",

        "career": """Расскажу про одного нашего ученика.

IT-специалист. Английский — средний. Говорить — боялся. На созвонах молчал.

3 месяца занятий с носителем: деловой английский, созвоны, презентации.

<b>Результат:</b> прошёл собеседование в международную компанию. Зарплата выросла на 40%.

<i>«Дело не в уровне. Я никогда не тренировал говорить под давлением.»</i>

Первый урок бесплатно — ссылка завтра.""",

        "other": """Ещё одна история.

Ученица учила итальянский 2 года. По приложениям. Потом поехала в Рим — не смогла объясниться.

Пришла к нам. Через 6 недель с носителем — свободно разговаривала с местными.

<i>«Я перестала думать о грамматике и просто начала говорить.»</i>

Первый урок бесплатно — ссылка завтра 🙂"""
    },
    "en": {
        "relocation": """Let me tell you about one of our students.

She was planning to move to Barcelona. Started learning Spanish 3 months before. From scratch.

<b>After 8 weeks she:</b>
— negotiated her apartment rental herself
— opened a bank account without a translator
— booked a doctor and explained her symptoms

<i>"Without this course I would have spent so much more on intermediaries" — she wrote after moving.</i>

Want to sort out your situation? Free first lesson — link tomorrow.""",

        "career": """Let me tell you about one of our students.

IT specialist. Intermediate English. Could write — but froze on calls. Silent in meetings.

3 months with a native speaker: business English, calls, presentations.

<b>Result:</b> passed an interview at an international company. Salary went up 40%.

<i>"It wasn't about my level. I had never practised speaking under pressure."</i>

Free first lesson — link tomorrow.""",

        "other": """Another story.

A student had been learning Italian for 2 years. Through apps. Then went to Rome — couldn't communicate.

Came to us. After 6 weeks with a native speaker from Italy — she was chatting freely with locals.

<i>"I stopped thinking about grammar and just started speaking."</i>

Free first lesson — link tomorrow 🙂"""
    }
}

# ══ ДЕНЬ 6 — ОФФЕР ══════════════════════════════════════════════════

DAY6 = {
    "ru": """Хочу быть честной.

Мы не подходим всем. И мы не берём людей, если понимаем что им нужно другое.

Но если ты хочешь <b>говорить</b> — а не просто «знать язык» — мы умеем именно это.

<b>Первый урок — бесплатно. 45 минут:</b>
— Определяем твой уровень
— Разбираем твою цель (переезд / работа / другое)
— Подбираем преподавателя-носителя
— Составляем план именно под тебя

Без обязательств. Если не подойдём — так и скажем.

👇 Записаться:""",

    "en": """I want to be honest.

We don't work for everyone. And we won't take you on if we think you need something different.

But if you want to <b>actually speak</b> — not just "know the language" — that's exactly what we do.

<b>First lesson — free. 45 minutes:</b>
— We assess your level
— We discuss your goal (relocation / career / other)
— We match you with a native-speaker teacher
— We build a plan specifically for you

No commitment. If we're not the right fit — we'll tell you honestly.

👇 Book your spot:"""
}

# ══ ДЕНЬ 7 — ДОЖИМ ══════════════════════════════════════════════════

DAY7 = {
    "ru": """Последнее сообщение — обещаю не надоедать 😊

Если ты ещё думаешь — это нормально. Хочу убрать одно возражение:

<i>«Пойду когда буду готов»</i> — но готовность не приходит сама. Приходит только когда начинаешь.

Первый урок бесплатный именно поэтому — без риска попробовать.

<b>Место на этой неделе ещё есть.</b> 👇""",

    "en": """Last message — I promise not to bother you after this 😊

If you're still thinking — that's completely normal. I just want to remove one objection:

<i>"I'll go when I'm ready"</i> — but readiness doesn't come on its own. It comes when you start.

The first lesson is free for exactly that reason — try it without any risk.

<b>There's still a spot this week.</b> 👇"""
}

# ══ CTA ПОДТВЕРЖДЕНИЕ ═══════════════════════════════════════════════

CTA_BOOKED = {
    "ru": """Отлично! 🎉

Дарья напишет тебе в течение 15 минут — договоритесь об удобном времени.

Если хочешь написать прямо сейчас — просто ответь сюда 🙂""",

    "en": """Awesome! 🎉

Darya will message you within 15 minutes to schedule a convenient time.

If you'd like to reach out right now — just reply here 🙂"""
}

# ══ УВЕДОМЛЕНИЕ ДАРЬЕ ═══════════════════════════════════════════════

ADMIN_NOTIFICATION = """{flag} <b>Новая заявка из бота!</b>

👤 Пользователь: {mention}
🌐 Язык интерфейса: {lang}
🎯 Сегмент: {segment}
📅 Подписался: {subscribed}
💬 Username: @{username}

<i>Напиши ему первой — он ждёт 🙂</i>"""

SEGMENT_LABELS = {
    "ru": {
        "relocation": "🏠 Переезд за рубеж",
        "career":     "💼 Карьера и работа",
        "other":      "🌍 Другое",
    },
    "en": {
        "relocation": "🏠 Relocation abroad",
        "career":     "💼 Career & work",
        "other":      "🌍 Other",
    }
}

# ══ КНОПКИ (тексты) ═════════════════════════════════════════════════

BTN_SEGMENT = {
    "ru": ["🏠 Переезд за рубеж", "💼 Карьера и работа", "🌍 Другое"],
    "en": ["🏠 Relocation abroad", "💼 Career & work", "🌍 Other"]
}

BTN_WHEN = {
    "ru": ["📅 До 3 месяцев", "📅 Через полгода", "🤔 Пока думаю"],
    "en": ["📅 Within 3 months", "📅 In about 6 months", "🤔 Still thinking"]
}

BTN_CAREER = {
    "ru": ["🎤 Говорить свободно", "📝 Писать письма", "💼 Пройти собеседование"],
    "en": ["🎤 Speak fluently", "📝 Write emails", "💼 Pass an interview"]
}

BTN_OTHER = {
    "ru": ["✅ Да, это про меня", "❌ Нет, другая ситуация"],
    "en": ["✅ Yes, that's me", "❌ No, different situation"]
}

BTN_CTA = {
    "ru": ["✅ Записаться на урок", "❓ Есть вопрос"],
    "en": ["✅ Book a lesson", "❓ I have a question"]
}

ANSWERS = {
    "ru": {
        "when_soon":      "Значит, времени немного. Правильно что начинаешь сейчас ✅",
        "when_half":      "Полгода — хорошо. Успеем подготовиться основательно ✅",
        "when_thinking":  "Думать — нормально. Но чем раньше начнёшь — тем спокойнее переезд ✅",
        "goal_speak":     "Говорить свободно — именно это тренируем с первого урока ✅",
        "goal_write":     "Деловая переписка — конкретный навык. Отработаем ✅",
        "goal_interview": "Собеседование — чёткая цель. Готовим именно к этому ✅",
        "other_yes":      "Слышим тебя. Именно с этим работаем 🙂",
        "other_no":       "Расскажи свою ситуацию — Дарья ответит лично. Напиши текстом 👇",
    },
    "en": {
        "when_soon":      "So not much time. Good that you're starting now ✅",
        "when_half":      "Six months — great. Plenty of time to prepare properly ✅",
        "when_thinking":  "That's fine. But the sooner you start, the calmer the move ✅",
        "goal_speak":     "Speaking fluently — that's exactly what we train from lesson one ✅",
        "goal_write":     "Business writing — a specific skill. We'll work on templates ✅",
        "goal_interview": "Interview prep — a clear goal. We'll train specifically for that ✅",
        "other_yes":      "Heard you. That's exactly what we work on 🙂",
        "other_no":       "Tell me your situation — Darya will reply personally. Just write 👇",
    }
}

FREE_TEXT_REPLY = {
    "ru": "Получила! Дарья ответит в течение 24 часов 🙂\n\nПока ждёшь — посмотри наш канал 👉 https://t.me/BigCheeseLanguages",
    "en": "Got it! Darya will reply within 24 hours 🙂\n\nWhile you wait — check our channel 👉 https://t.me/BigCheeseLanguages"
}
