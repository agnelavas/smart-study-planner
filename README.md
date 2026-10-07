# 🌌 StudySync — Adaptive Revision Engine

> An urgency-weighted, fault-tolerant revision scheduling system built for university students facing multi-exam deadlines.

## 📌 Problem Statement

Most traditional revision planners generate static timetables that divide syllabus volume uniformly across days. When a student inevitably misses a study block or falls behind, the schedule collapses, leading to cognitive fatigue and abandoned routines.

## 💡 Solution Overview

StudySync is an adaptive study scheduling dashboard built with Python, Streamlit, and Plotly. It departs from linear time-slicing by implementing an **Urgency-Difficulty Priority Score (UDPS)**.

### Key Features

- **Priority-Weighted Scheduling:** Proximity to exams and subject difficulty dynamically dictate daily hour allocations.
- **Dynamic Panic Rebalancer:** Redistributes missed study weight across remaining days without breaching maximum daily cognitive caps.
- **Cognitive Tapering:** Automatically reduces study workloads by 50% on exam eve.
- **Interoperability:** One-click RFC 5545 `.ics` calendar synchronization.
- **Focus features:** Embedded ambient study audio and real-time NASA Astronomy Picture of the Day (APOD) micro-breaks.

## 🛠️ Tech Stack & Dependencies

- Python 3.10+
- Streamlit
- Plotly Express
- Pandas
- DateTime
- NASA APOD REST API
- RFC 5545 iCalendar standard

## 🚀 Installation & Local Execution

### 1. Clone the repository

```bash
git clone <your-github-repo-link>
cd smart-study-planner
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate it on Windows

```bash
venv\Scripts\activate
```

### 4. Activate it on macOS/Linux

```bash
source venv/bin/activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Launch the dashboard

```bash
streamlit run app.py
```

## 👥 Team Work Distribution

- **Member A — AGNELA PEARL VAS - Core Logic / Backend:** Urgency-Difficulty Priority Score algorithm, exam-eve tapering logic, panic rebalancer, `.ics` calendar generator.
- **Member B — AISHANI SEJAL - Supporting Logic / Integration:** Input validation rules, preset exam schedules, offline fallback vaults, integration tests.
- **Member C — AKSHITHA N - Interface / Visualization:** Streamlit layout, custom four-palette CSS architecture, Plotly stacked timeline, interactive checklist matrix.
- **Member D — AMRITA JYOTI - Documentation / QA / Presentation:** Technical documentation, presentation deck, system stress testing.

## 🧪 Quality Assurance

Member D verifies boundary conditions including:
- 0 study hours
- Large subject counts
- Exam date set to today
- No-subject plan generation
- Preset loading
- Dynamic rebalancing
- Calendar export

Expected behavior is a clean user-facing response rather than a terminal traceback.

## 📊 Main Evaluation Features

The backup demonstration should show:
1. Preset loading
2. Intelligent plan generation
3. Dynamic rebalance after missed study time
4. Calendar export

## 🔭 Future Scope

- OCR-based syllabus scanning from camera images
- AI-driven topic velocity tracking
- Automated Telegram reminder hooks
