import sqlite3
import os
import json
import pandas as pd


# =========================================================
# DATABASE LOCATION
# =========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_NAME = os.path.join(BASE_DIR, "studysync.db")


def get_connection():
    return sqlite3.connect(DATABASE_NAME)


# =========================================================
# STUDENT PROFILE
# =========================================================

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS student_profile (
            id INTEGER PRIMARY KEY,
            name TEXT,
            email TEXT,
            phone TEXT,
            college TEXT,
            semester TEXT
        )
    """)

    conn.commit()
    conn.close()


def save_profile(name, email, phone, college, semester):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR REPLACE INTO student_profile
        (id, name, email, phone, college, semester)
        VALUES (1, ?, ?, ?, ?, ?)
    """, (
        name,
        email,
        phone,
        college,
        semester
    ))

    conn.commit()
    conn.close()


def load_profile():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT name, email, phone, college, semester
        FROM student_profile
        WHERE id = 1
    """)

    profile = cursor.fetchone()

    conn.close()

    return profile


# =========================================================
# SUBJECTS
# =========================================================

def create_subject_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS subjects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            chapters INTEGER,
            difficulty INTEGER,
            exam_date TEXT
        )
    """)

    conn.commit()
    conn.close()


def save_subject(name, chapters, difficulty, exam_date):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO subjects
        (name, chapters, difficulty, exam_date)
        VALUES (?, ?, ?, ?)
    """, (
        name,
        chapters,
        difficulty,
        str(exam_date)
    ))

    conn.commit()
    conn.close()


def load_subjects():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name, chapters, difficulty, exam_date
        FROM subjects
        ORDER BY id
    """)

    rows = cursor.fetchall()

    conn.close()

    subjects = []

    for row in rows:
        subjects.append({
            "id": row[0],
            "name": row[1],
            "chapters": row[2],
            "difficulty": row[3],
            "exam_date": row[4]
        })

    return subjects


def delete_subject(subject_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM subjects
        WHERE id = ?
    """, (subject_id,))

    conn.commit()
    conn.close()


# =========================================================
# SAVED TIMETABLE
# =========================================================

def create_schedule_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS saved_schedule (
            id INTEGER PRIMARY KEY,
            schedule_data TEXT
        )
    """)

    conn.commit()
    conn.close()


def save_schedule(schedule_df):
    conn = get_connection()
    cursor = conn.cursor()

    create_schedule_table()

    data = schedule_df.to_json(
        orient="records",
        date_format="iso"
    )

    cursor.execute("""
        INSERT OR REPLACE INTO saved_schedule
        (id, schedule_data)
        VALUES (1, ?)
    """, (data,))

    conn.commit()
    conn.close()


def load_schedule():
    conn = get_connection()
    cursor = conn.cursor()

    create_schedule_table()

    cursor.execute("""
        SELECT schedule_data
        FROM saved_schedule
        WHERE id = 1
    """)

    result = cursor.fetchone()

    conn.close()

    if not result:
        return pd.DataFrame()

    try:
        data = json.loads(result[0])

        return pd.DataFrame(data)

    except Exception:
        return pd.DataFrame()


def delete_schedule():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM saved_schedule
        WHERE id = 1
    """)

    conn.commit()
    conn.close()