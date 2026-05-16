import sqlite3
from pathlib import Path

DB_PATH = Path("garmin_data.db")

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS activities (
            activity_id     TEXT PRIMARY KEY,
            name            TEXT,
            activity_type   TEXT,
            start_time      TEXT,
            duration_secs   REAL,
            distance_meters REAL,
            avg_hr          REAL,
            max_hr          REAL,
            calories        REAL,
            avg_speed       REAL,
            elevation_gain  REAL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS daily_steps (
            date        TEXT PRIMARY KEY,
            total_steps INTEGER,
            goal        INTEGER
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sleep (
            date            TEXT PRIMARY KEY,
            sleep_seconds   REAL,
            deep_seconds    REAL,
            light_seconds   REAL,
            rem_seconds     REAL,
            awake_seconds   REAL,
            score           REAL
        )
    """)

    conn.commit()
    conn.close()
    print("✅ Database initialised.")