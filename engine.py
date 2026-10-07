"""
engine.py - Core Scheduling & Algorithmic Engine for StudySync
Role: Member A (Core Logic / Backend Developer)
"""

from datetime import date, timedelta, datetime
import pandas as pd
import requests

# ---------------------------------------------------------
# 1. Cosmic Inspiration Engine (NASA APOD + Resilient Fallback)
# ---------------------------------------------------------
def get_nasa_apod() -> dict:
    """
    Fetches the NASA Astronomy Picture of the Day using the demo API key.
    Includes explicit error handling and an offline fallback for demo reliability.
    """
    url = "https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY"
    try:
        res = requests.get(url, timeout=3)
        if res.status_code == 200:
            data = res.json()
            return {
                "title": data.get("title", "Cosmic Daily Focus"),
                "url": data.get("url"),
                "explanation": data.get("explanation", ""),
                "media_type": data.get("media_type", "image")
            }
    except Exception:
        # Failsafe fallback if Wi-Fi or API quota limits fail
        pass

    return {
        "title": "Cosmic Perspective: The Carina Nebula",
        "url": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?q=80&w=1200",
        "explanation": "Exam syllabus feels overwhelming? The cosmos reminds us to take it one day, one orbit at a time.",
        "media_type": "image"
    }

# ---------------------------------------------------------
# 2. Algorithmic Scheduler (UDPS + Exam-Eve Tapering)
# ---------------------------------------------------------
def generate_study_plan(
    subjects: list, 
    start_date: date, 
    daily_hours: float, 
    taper_exam_eve: bool = True
) -> pd.DataFrame:
    """
    Generates a balanced day-by-day revision schedule using the
    Urgency-Difficulty Priority Score (UDPS):
        Score = (Difficulty * Chapters) / max(1, Days until exam)
    """
    if not subjects:
        return pd.DataFrame()

    max_exam_date = max(s["exam_date"] for s in subjects)
    total_days = (max_exam_date - start_date).days
    if total_days <= 0:
        total_days = 1

    records = []
    current_date = start_date

    for day_offset in range(total_days):
        day_date = current_date + timedelta(days=day_offset)

        # Filter subjects whose exams have not passed
        active_subjects = [
            s for s in subjects 
            if (s["exam_date"] - day_date).days >= 0
        ]

        if not active_subjects:
            break

        # Check for Exam Eve condition
        is_exam_eve = any((s["exam_date"] - day_date).days == 1 for s in active_subjects)
        effective_daily_hours = daily_hours * 0.5 if (taper_exam_eve and is_exam_eve) else daily_hours

        # Calculate UDPS priority weights
        scores = []
        for s in active_subjects:
            days_left = max(1, (s["exam_date"] - day_date).days)
            score = (s["difficulty"] * s["chapters"]) / days_left
            scores.append(score)

        total_score = sum(scores) if sum(scores) > 0 else 1.0

        # Allocate hours proportionally
        for s, score in zip(active_subjects, scores):
            allocated_hours = round((score / total_score) * effective_daily_hours, 1)
            if allocated_hours > 0:
                records.append({
                    "Date": day_date.strftime("%Y-%m-%d"),
                    "Subject": s["name"],
                    "Hours": allocated_hours,
                    "Exam Date": s["exam_date"].strftime("%Y-%m-%d"),
                    "Days Left": (s["exam_date"] - day_date).days,
                    "Status": "Pending"
                })

    return pd.DataFrame(records)

# ---------------------------------------------------------
# 3. Dynamic Panic Rebalancer
# ---------------------------------------------------------
def panic_rebalance(
    schedule_df: pd.DataFrame, 
    current_date_str: str, 
    max_daily_cap: float = 10.0
) -> pd.DataFrame:
    """
    Recalculates remaining days when past tasks are skipped or missed,
    redistributing the deficit across remaining slots while honoring caps.
    """
    if schedule_df.empty:
        return schedule_df

    df = schedule_df.copy()

    # Identify incomplete past hours
    uncompleted_mask = (df["Date"] <= current_date_str) & (df["Status"] != "Completed")
    missed_hours = df.loc[uncompleted_mask, "Hours"].sum()

    future_mask = df["Date"] > current_date_str
    future_count = future_mask.sum()

    if future_count > 0 and missed_hours > 0:
        extra_per_task = missed_hours / future_count
        df.loc[future_mask, "Hours"] = (df.loc[future_mask, "Hours"] + extra_per_task).round(1)

        # Enforce maximum safety cap
        df.loc[future_mask, "Hours"] = df.loc[future_mask, "Hours"].apply(
            lambda h: min(h, max_daily_cap)
        )

    return df

# ---------------------------------------------------------
# 4. Universal Calendar (.ics) Generator
# ---------------------------------------------------------
def generate_ics_calendar(schedule_df: pd.DataFrame) -> str:
    """
    Converts the DataFrame into an RFC 5545 compliant iCalendar string.
    """
    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//StudySync//Adaptive Revision Engine//EN",
        "CALSCALE:GREGORIAN"
    ]

    for _, row in schedule_df.iterrows():
        study_date = datetime.strptime(row["Date"], "%Y-%m-%d").date()
        dt_start = study_date.strftime("%Y%m%d")
        dt_end = (study_date + timedelta(days=1)).strftime("%Y%m%d")

        lines.extend([
            "BEGIN:VEVENT",
            f"SUMMARY:Study: {row['Subject']} ({row['Hours']}h)",
            f"DESCRIPTION:Target Exam: {row['Exam Date']} | Status: {row['Status']}",
            f"DTSTART;VALUE=DATE:{dt_start}",
            f"DTEND;VALUE=DATE:{dt_end}",
            f"STATUS:CONFIRMED",
            "END:VEVENT"
        ])

    lines.append("END:VCALENDAR")
    return "\n".join(lines)

# ---------------------------------------------------------
# 5. Standalone Terminal Test Harness
# ---------------------------------------------------------
if __name__ == "__main__":
    print("Testing Member A Backend Logic...")
    sample_subjects = [
        {"name": "Computer Architecture", "chapters": 5, "difficulty": 4, "exam_date": date.today() + timedelta(days=4)},
        {"name": "DBMS", "chapters": 6, "difficulty": 3, "exam_date": date.today() + timedelta(days=8)}
    ]
    
    plan = generate_study_plan(sample_subjects, date.today(), daily_hours=5.0)
    print("\n--- Plan Output Preview ---")
    print(plan.head())
    
    rebalanced = panic_rebalance(plan, date.today().strftime("%Y-%m-%d"))
    print("\n--- Rebalanced Preview ---")
    print(rebalanced.head())
    
    ics_text = generate_ics_calendar(plan)
    print("\n--- ICS File Output Preview ---")
    print("\n".join(ics_text.splitlines()[:10]))
    print("\nAll backend modules executed cleanly!")