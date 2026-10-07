import sqlite3
import os
import json
import hashlib
import pandas as pd


# =========================================================
# DATABASE LOCATION
# =========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_NAME = os.path.join(BASE_DIR, "studysync.db")


def get_connection():
    return sqlite3.connect(DATABASE_NAME)


# =========================================================
# PASSWORD SECURITY
# =========================================================

def hash_password(password):
    return hashlib.sha256(
        password.encode("utf-8")
    ).hexdigest()


# =========================================================
# CREATE TABLES
# =========================================================

def create_tables():

    conn = get_connection()
    cursor = conn.cursor()

    # USERS
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            name TEXT,
            email TEXT,
            phone TEXT,
            college TEXT,
            semester TEXT
        )
    """)

    # SUBJECTS
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_subjects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            name TEXT,
            chapters INTEGER,
            difficulty INTEGER,
            exam_date TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    # SAVED TIMETABLE
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_schedules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE NOT NULL,
            schedule_data TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    conn.commit()
    conn.close()


# =========================================================
# USER ACCOUNT
# =========================================================

def create_user(username, password, name, email, phone, college, semester):

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute("""
            INSERT INTO users
            (username, password, name, email, phone, college, semester)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            username.strip().lower(),
            hash_password(password),
            name.strip(),
            email.strip(),
            phone.strip(),
            college.strip(),
            semester.strip()
        ))

        conn.commit()

        user_id = cursor.lastrowid

        conn.close()

        return user_id

    except sqlite3.IntegrityError:

        conn.close()

        return None


def login_user(username, password):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            username,
            name,
            email,
            phone,
            college,
            semester
        FROM users
        WHERE username = ?
        AND password = ?
    """, (
        username.strip().lower(),
        hash_password(password)
    ))

    user = cursor.fetchone()

    conn.close()

    return user


# =========================================================
# PROFILE
# =========================================================

def load_profile(user_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            name,
            email,
            phone,
            college,
            semester
        FROM users
        WHERE id = ?
    """, (user_id,))

    profile = cursor.fetchone()

    conn.close()

    return profile


def save_profile(
    user_id,
    name,
    email,
    phone,
    college,
    semester
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE users
        SET
            name = ?,
            email = ?,
            phone = ?,
            college = ?,
            semester = ?
        WHERE id = ?
    """, (
        name,
        email,
        phone,
        college,
        semester,
        user_id
    ))

    conn.commit()
    conn.close()


# =========================================================
# SUBJECTS
# =========================================================

def save_subject(
    user_id,
    name,
    chapters,
    difficulty,
    exam_date
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO user_subjects
        (user_id, name, chapters, difficulty, exam_date)
        VALUES (?, ?, ?, ?, ?)
    """, (
        user_id,
        name,
        chapters,
        difficulty,
        str(exam_date)
    ))

    conn.commit()
    conn.close()


def load_subjects(user_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            name,
            chapters,
            difficulty,
            exam_date
        FROM user_subjects
        WHERE user_id = ?
        ORDER BY id
    """, (user_id,))

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


def delete_subject(user_id, subject_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM user_subjects
        WHERE id = ?
        AND user_id = ?
    """, (
        subject_id,
        user_id
    ))

    conn.commit()
    conn.close()


# =========================================================
# SAVED TIMETABLE
# =========================================================

def save_schedule(user_id, schedule_df):

    conn = get_connection()
    cursor = conn.cursor()

    data = schedule_df.to_json(
        orient="records",
        date_format="iso"
    )

    cursor.execute("""
        INSERT INTO user_schedules
        (user_id, schedule_data)
        VALUES (?, ?)
        ON CONFLICT(user_id)
        DO UPDATE SET schedule_data = excluded.schedule_data
    """, (
        user_id,
        data
    ))

    conn.commit()
    conn.close()


def load_schedule(user_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT schedule_data
        FROM user_schedules
        WHERE user_id = ?
    """, (user_id,))

    result = cursor.fetchone()

    conn.close()

    if not result:
        return pd.DataFrame()

    try:

        data = json.loads(result[0])

        return pd.DataFrame(data)

    except Exception:

        return pd.DataFrame()


def delete_schedule(user_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM user_schedules
        WHERE user_id = ?
    """, (user_id,))

    conn.commit()
    conn.close()


# =========================================================
# INITIALIZE DATABASE
# =========================================================

create_tables()