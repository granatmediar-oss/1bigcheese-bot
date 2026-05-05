def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS users (
        user_id     INTEGER PRIMARY KEY,
        username    TEXT,
        first_name  TEXT,
        lang        TEXT DEFAULT 'ru',
        segment     TEXT DEFAULT NULL,
        subscribed  TEXT DEFAULT CURRENT_TIMESTAMP,
        day2_sent   INTEGER DEFAULT 0,
        day4_sent   INTEGER DEFAULT 0,
        day6_sent   INTEGER DEFAULT 0,
        day7_sent   INTEGER DEFAULT 0,
        clicked_cta INTEGER DEFAULT 0
    )""")

    # Safe migrations for older users.db versions
    c.execute("PRAGMA table_info(users)")
    existing_columns = [row[1] for row in c.fetchall()]

    migrations = {
        "username": "ALTER TABLE users ADD COLUMN username TEXT",
        "first_name": "ALTER TABLE users ADD COLUMN first_name TEXT",
        "lang": "ALTER TABLE users ADD COLUMN lang TEXT DEFAULT 'ru'",
        "segment": "ALTER TABLE users ADD COLUMN segment TEXT DEFAULT NULL",
        "subscribed": "ALTER TABLE users ADD COLUMN subscribed TEXT DEFAULT CURRENT_TIMESTAMP",
        "day2_sent": "ALTER TABLE users ADD COLUMN day2_sent INTEGER DEFAULT 0",
        "day4_sent": "ALTER TABLE users ADD COLUMN day4_sent INTEGER DEFAULT 0",
        "day6_sent": "ALTER TABLE users ADD COLUMN day6_sent INTEGER DEFAULT 0",
        "day7_sent": "ALTER TABLE users ADD COLUMN day7_sent INTEGER DEFAULT 0",
        "clicked_cta": "ALTER TABLE users ADD COLUMN clicked_cta INTEGER DEFAULT 0",
    }

    for column, sql in migrations.items():
        if column not in existing_columns:
            c.execute(sql)

    conn.commit()
    conn.close()
    log.info("DB ready: %s", DB_PATH)
