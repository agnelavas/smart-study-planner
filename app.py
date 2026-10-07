"""
StudySync - Smart Study Planner
Member C: Interface / Output / Visualization Developer
"""

import streamlit as st
import pandas as pd
from datetime import date, timedelta
import plotly.express as px

from database import (
    create_tables,
    create_subject_table,
    create_schedule_table,
    save_profile,
    load_profile,
    save_subject,
    load_subjects,
    delete_subject,
    save_schedule,
    load_schedule,
    delete_schedule,
)

# Create database tables
create_tables()
create_subject_table()
create_schedule_table()

from engine import (
    generate_study_plan,
    panic_rebalance,
    generate_ics_calendar,
)

try:
    from engine import get_nasa_apod
except Exception:
    get_nasa_apod = None


# =========================================================
# 1. PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="StudySync - Smart Study Planner",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# 2. THEMES
# =========================================================

THEMES = {
    "Midnight Cosmos (Dark)": {
        "bg": "linear-gradient(135deg, #0B0E14 0%, #161B26 100%)",
        "card_bg": "rgba(255,255,255,0.05)",
        "border": "rgba(255,255,255,0.12)",
        "text": "#E2E8F0",
        "accent": "#A855F7",
        "plotly": "plotly_dark",
    },

    "Espresso Library (Dark Academia)": {
        "bg": "linear-gradient(135deg, #1C1614 0%, #2A221E 100%)",
        "card_bg": "rgba(212,175,55,0.06)",
        "border": "rgba(212,175,55,0.18)",
        "text": "#F4EBD9",
        "accent": "#D4AF37",
        "plotly": "plotly_dark",
    },

    "Parchment & Ink (Light)": {
        "bg": "linear-gradient(135deg, #F5EBD7 0%, #FFF8EA 100%)",
        "card_bg": "rgba(255,255,255,0.72)",
        "border": "rgba(90,70,40,0.18)",
        "text": "#302A24",
        "accent": "#8B5E34",
        "plotly": "plotly_white",
    },

    "Nordic Aurora (Light)": {
        "bg": "linear-gradient(135deg, #EAF7F4 0%, #F7FBFF 100%)",
        "card_bg": "rgba(255,255,255,0.75)",
        "border": "rgba(40,90,90,0.16)",
        "text": "#183333",
        "accent": "#168A8A",
        "plotly": "plotly_white",
    },
}


# =========================================================
# 3. SESSION STATE
# =========================================================

if "subjects" not in st.session_state:

    saved_subjects = load_subjects()

    for subject in saved_subjects:

        try:
            subject["exam_date"] = date.fromisoformat(
                subject["exam_date"]
            )
        except Exception:
            pass

    st.session_state.subjects = saved_subjects


if "schedule_df" not in st.session_state:

    st.session_state.schedule_df = load_schedule()


if "student_name" not in st.session_state:

    st.session_state.student_name = ""


if "edit_profile" not in st.session_state:

    st.session_state.edit_profile = False


# =========================================================
# 4. SIDEBAR
# =========================================================

with st.sidebar:

    st.header("🌌 StudySync")

    st.caption(
        "Personalized Smart Study Planner"
    )

    # Theme
    theme_name = st.selectbox(
        "🎨 Choose Theme",
        list(THEMES.keys()),
    )

    theme = THEMES[theme_name]

    st.divider()


    # =====================================================
    # STUDENT PROFILE
    # =====================================================

    st.subheader("👤 Student Profile")

    saved_profile = load_profile()

    # NORMAL PROFILE VIEW
    if (
        saved_profile
        and saved_profile[0]
        and not st.session_state.edit_profile
    ):

        # Show ONLY name
        st.write(
            f"**Name:** {saved_profile[0]}"
        )

        # Edit button
        if st.button(
            "✏️ Edit Profile",
            use_container_width=True,
        ):

            st.session_state.edit_profile = True
            st.rerun()

        student_name = saved_profile[0]

        st.session_state.student_name = student_name


    # EDIT / FIRST TIME PROFILE
    else:

        if saved_profile:

            default_name = saved_profile[0] or ""
            default_email = saved_profile[1] or ""
            default_phone = saved_profile[2] or ""
            default_college = saved_profile[3] or ""
            default_semester = saved_profile[4] or ""

        else:

            default_name = ""
            default_email = ""
            default_phone = ""
            default_college = ""
            default_semester = ""


        student_name = st.text_input(
            "Student Name",
            value=default_name,
            placeholder="Enter your name",
        )

        email = st.text_input(
            "📧 Email",
            value=default_email,
            placeholder="example@email.com",
        )

        phone = st.text_input(
            "📱 Phone Number",
            value=default_phone,
            placeholder="Enter phone number",
        )

        college = st.text_input(
            "🏫 College",
            value=default_college,
            placeholder="Enter your college",
        )

        semester = st.text_input(
            "🎓 Semester",
            value=default_semester,
            placeholder="Example: 3rd Semester",
        )


        if st.button(
            "💾 Save Profile",
            use_container_width=True,
        ):

            if not student_name.strip():

                st.error(
                    "Please enter your name."
                )

            else:

                save_profile(
                    student_name,
                    email,
                    phone,
                    college,
                    semester,
                )

                st.session_state.student_name = (
                    student_name
                )

                st.session_state.edit_profile = False

                st.success(
                    "✅ Profile saved successfully!"
                )

                st.rerun()


    st.divider()


    # =====================================================
    # SCHEDULE CONSTRAINTS
    # =====================================================

    st.subheader(
        "📅 Schedule Constraints"
    )

    daily_hours = st.slider(
        "Daily Focus Hours",
        min_value=1.0,
        max_value=12.0,
        value=5.0,
        step=0.5,
    )

    start_date = st.date_input(
        "Start Date",
        value=date.today(),
    )

    taper_eve = st.checkbox(
        "Exam-Eve Cognitive Taper (50% Load)",
        value=True,
    )


    st.divider()


    # =====================================================
    # FOCUS AUDIO
    # =====================================================

    st.subheader("🎵 Focus Audio")

    audio_url = st.text_input(
        "Focus Audio URL",
        placeholder="Paste audio/YouTube URL",
    )

    if audio_url:

        st.markdown(
            f"[🎧 Open Focus Audio]({audio_url})"
        )


# =========================================================
# 5. CUSTOM CSS
# =========================================================

st.markdown(
    f"""
    <style>

    .stApp {{
        background: {theme["bg"]};
        color: {theme["text"]};
    }}

    [data-testid="stSidebar"] {{
        background: rgba(0,0,0,0.12);
    }}

    .main-title {{
        font-size: 42px;
        font-weight: 800;
        margin-bottom: 5px;
    }}

    .subtitle {{
        opacity: 0.75;
        font-size: 18px;
        margin-bottom: 25px;
    }}

    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# 6. HEADER
# =========================================================

st.markdown(
    '<div class="main-title">🌌 StudySync</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="subtitle">Adaptive, Urgency-Weighted Smart Study Planner</div>',
    unsafe_allow_html=True,
)


if student_name:

    st.success(
        f"Welcome, {student_name}! 👋 Enter your subjects below and generate your personalized timetable."
    )

else:

    st.info(
        "👋 Welcome! Enter your name and subjects to create your personalized timetable."
    )


# =========================================================
# 7. KPI SECTION
# =========================================================

subject_count = len(
    st.session_state.subjects
)

total_hours = 0.0

if not st.session_state.schedule_df.empty:

    if "Hours" in st.session_state.schedule_df.columns:

        total_hours = float(
            st.session_state.schedule_df["Hours"].sum()
        )


exam_days = "—"

if st.session_state.subjects:

    future_dates = []

    for subject in st.session_state.subjects:

        exam = subject.get("exam_date")

        if isinstance(exam, str):

            try:
                exam = date.fromisoformat(exam)
            except Exception:
                continue

        if exam:
            future_dates.append(exam)

    if future_dates:

        nearest_exam = min(future_dates)

        days_left = (
            nearest_exam - date.today()
        ).days

        exam_days = (
            f"{max(days_left, 0)} days"
        )


k1, k2, k3, k4 = st.columns(4)

with k1:
    st.metric(
        "📚 Subjects",
        subject_count,
    )

with k2:
    st.metric(
        "⏱️ Revision Volume",
        f"{total_hours:.1f} hrs",
    )

with k3:
    st.metric(
        "🎯 Nearest Exam",
        exam_days,
    )

with k4:
    st.metric(
        "⚡ Daily Capacity",
        f"{daily_hours:.1f} hrs/day",
    )


# =========================================================
# 8. BUILD STUDY PLAN
# =========================================================

st.divider()

st.header(
    "📝 Build Your Personal Study Plan"
)

st.write(
    "Enter your subjects below. Every student can create a different timetable."
)


with st.expander(
    "➕ Add a Subject",
    expanded=True,
):

    with st.form(
        "add_subject_form",
        clear_on_submit=True,
    ):

        col1, col2 = st.columns(2)

        with col1:

            subject_name = st.text_input(
                "Subject Name",
                placeholder="Example: Data Structures",
            )

            chapters = st.number_input(
                "Number of Chapters / Units",
                min_value=1,
                max_value=100,
                value=5,
                step=1,
            )

        with col2:

            difficulty = st.slider(
                "Difficulty",
                min_value=1,
                max_value=5,
                value=3,
                help="1 = Easy, 5 = Very Difficult",
            )

            exam_date = st.date_input(
                "Exam Date",
                value=date.today() + timedelta(days=7),
                min_value=date.today(),
            )

        submitted = st.form_submit_button(
            "➕ Add Subject",
            type="primary",
            use_container_width=True,
        )


        if submitted:

            if not subject_name.strip():

                st.error(
                    "Please enter a subject name."
                )

            elif exam_date < start_date:

                st.error(
                    "Exam date cannot be before the study start date."
                )

            else:

                save_subject(
                    subject_name.strip(),
                    int(chapters),
                    int(difficulty),
                    exam_date,
                )

                st.session_state.subjects = (
                    load_subjects()
                )

                for subject in st.session_state.subjects:

                    try:
                        subject["exam_date"] = date.fromisoformat(
                            subject["exam_date"]
                        )
                    except Exception:
                        pass

                st.success(
                    f"{subject_name} added successfully! ✅"
                )

                st.rerun()


# =========================================================
# 9. SUBJECT ROSTER
# =========================================================

st.subheader(
    "📋 Your Subject Roster"
)


if not st.session_state.subjects:

    st.info(
        "No subjects added yet. Use 'Add a Subject' above."
    )

else:

    for i, subject in enumerate(
        st.session_state.subjects
    ):

        col1, col2, col3, col4, col5 = st.columns(
            [3, 1, 1, 2, 1]
        )

        with col1:
            st.write(
                f"**{subject['name']}**"
            )

        with col2:
            st.write(
                f"📖 {subject['chapters']} Ch"
            )

        with col3:
            st.write(
                f"⭐ {subject['difficulty']}/5"
            )

        with col4:
            st.write(
                f"📅 {subject['exam_date']}"
            )

        with col5:

            if st.button(
                "🗑️",
                key=f"delete_subject_{subject['id']}",
            ):

                delete_subject(
                    subject["id"]
                )

                st.session_state.subjects = (
                    load_subjects()
                )

                for saved_subject in st.session_state.subjects:

                    try:
                        saved_subject["exam_date"] = date.fromisoformat(
                            saved_subject["exam_date"]
                        )
                    except Exception:
                        pass

                st.session_state.schedule_df = (
                    pd.DataFrame()
                )

                delete_schedule()

                st.rerun()


# =========================================================
# 10. GENERATE TIMETABLE
# =========================================================

if st.session_state.subjects:

    st.divider()

    if st.button(
        "🚀 Generate My Personalized Study Timetable",
        type="primary",
        use_container_width=True,
    ):

        try:

            with st.spinner(
                "Creating your personalized timetable..."
            ):

                schedule = generate_study_plan(
                    st.session_state.subjects,
                    start_date,
                    daily_hours,
                    taper_exam_eve=taper_eve,
                )

                st.session_state.schedule_df = schedule

                # Save timetable permanently
                save_schedule(
                    st.session_state.schedule_df
                )

            st.success(
                "🎉 Your personalized study timetable has been generated and saved!"
            )

            st.rerun()

        except Exception as e:

            st.error(
                "Could not generate the timetable."
            )

            st.exception(e)


# =========================================================
# 11. CURRENT TIMETABLE
# =========================================================

if not st.session_state.schedule_df.empty:

    st.divider()

    st.header(
        "📅 Your Generated Study Timetable"
    )

    st.dataframe(
        st.session_state.schedule_df,
        use_container_width=True,
        hide_index=True,
    )


# =========================================================
# 12. DYNAMIC CATCH-UP
# =========================================================

if not st.session_state.schedule_df.empty:

    st.divider()

    st.header(
        "⚡ Dynamic Catch-up Actions"
    )

    st.write(
        "Missed your study target? Rebalance the remaining study hours."
    )

    col1, col2 = st.columns(2)

    with col1:

        slacked_date = st.date_input(
            "Which day did you miss?",
            value=date.today(),
            key="slacked_date",
        )

    with col2:

        st.write("")
        st.write("")

        if st.button(
            "⚠️ Slacked Off Today? Rebalance Plan",
            use_container_width=True,
        ):

            current_df = (
                st.session_state.schedule_df.copy()
            )

            old_hours = current_df["Hours"].sum()

            new_schedule = panic_rebalance(
                current_df,
                slacked_date.strftime(
                    "%Y-%m-%d"
                ),
            )

            new_hours = new_schedule["Hours"].sum()

            st.session_state.schedule_df = (
                new_schedule
            )

            save_schedule(
                new_schedule
            )

            st.success(
                "✅ Schedule recalibrated and saved!"
            )

            st.info(
                "📚 Missed study hours were redistributed across the remaining study sessions."
            )

            st.write(
                f"**Previous total planned hours:** {old_hours:.1f} hrs"
            )

            st.write(
                f"**Updated total planned hours:** {new_hours:.1f} hrs"
            )


# =========================================================
# 13. CALENDAR EXPORT
# =========================================================

if not st.session_state.schedule_df.empty:

    st.divider()

    st.subheader(
        "📅 Calendar Integration"
    )

    try:

        ics_content = generate_ics_calendar(
            st.session_state.schedule_df
        )

        st.download_button(
            label="📅 Export Study Plan to Calendar (.ics)",
            data=ics_content,
            file_name="my_study_plan.ics",
            mime="text/calendar",
            use_container_width=True,
        )

    except Exception:

        st.error(
            "Calendar export is currently unavailable."
        )


# =========================================================
# 14. PLOTLY REVISION ROADMAP
# =========================================================

if not st.session_state.schedule_df.empty:

    st.divider()

    st.header(
        "📊 Dynamic Revision Roadmap"
    )

    df = st.session_state.schedule_df.copy()

    if "Date" in df.columns:

        df["Date"] = pd.to_datetime(
            df["Date"]
        )

    fig = px.bar(
        df,
        x="Date",
        y="Hours",
        color="Subject",
        title="Daily Urgency-Weighted Study Hours",
        template=theme["plotly"],
        barmode="stack",
        hover_data=[
            c
            for c in [
                "Subject",
                "Hours",
                "Exam Date",
                "Days Left",
            ]
            if c in df.columns
        ],
    )

    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
        ),
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )


# =========================================================
# 15. INTERACTIVE CHECKLIST
# =========================================================

if not st.session_state.schedule_df.empty:

    st.divider()

    st.header(
        "✅ Interactive Revision Checklist"
    )

    checklist_df = (
        st.session_state.schedule_df.copy()
    )

    if "Status" not in checklist_df.columns:

        checklist_df["Status"] = "Pending"

    disabled_columns = [
        column
        for column in [
            "Date",
            "Subject",
            "Hours",
            "Exam Date",
            "Days Left",
        ]
        if column in checklist_df.columns
    ]

    edited_df = st.data_editor(
        checklist_df,
        column_config={
            "Status": st.column_config.SelectboxColumn(
                "Status",
                options=[
                    "Pending",
                    "Completed",
                    "Skipped",
                ],
                required=True,
            )
        },
        disabled=disabled_columns,
        hide_index=True,
        use_container_width=True,
        key="revision_checklist",
    )

    st.session_state.schedule_df = edited_df

    # Save checklist changes
    save_schedule(
        st.session_state.schedule_df
    )


# =========================================================
# 16. COSMIC FOCUS
# =========================================================

st.divider()

with st.expander(
    "🌌 Cosmic Focus & Motivation"
):

    st.write(
        "Take a short break, stay focused and keep studying! 🚀"
    )

    if get_nasa_apod is not None:

        try:

            if st.button(
                "🌠 Load NASA Astronomy Picture"
            ):

                apod = get_nasa_apod()

                if apod:

                    if apod.get("url"):

                        st.image(
                            apod["url"],
                            use_container_width=True,
                        )

                    if apod.get("title"):

                        st.subheader(
                            apod["title"]
                        )

                    if apod.get("explanation"):

                        st.write(
                            apod["explanation"]
                        )

        except Exception:

            st.info(
                "NASA picture is temporarily unavailable. The study planner still works normally."
            )

    st.info(
        "💡 Focus tip: Study for 25–50 minutes, then take a short break."
    )


# =========================================================
# 17. EMPTY STATE
# =========================================================

if (
    not st.session_state.subjects
    and st.session_state.schedule_df.empty
):

    st.divider()

    st.markdown(
        """
        ### 🚀 How StudySync Works

        **1️⃣ Enter your subjects**  
        Add every subject you want to study.

        **2️⃣ Enter exam dates**  
        The planner uses exam urgency.

        **3️⃣ Set difficulty and chapters**  
        Difficult subjects receive appropriate priority.

        **4️⃣ Set your daily study hours**  
        The timetable stays within your available time.

        **5️⃣ Generate your timetable**  
        StudySync creates your personalized revision plan.

        **6️⃣ Track your progress**  
        Mark tasks as Completed, Pending or Skipped.

        **7️⃣ Export to your calendar**  
        Download the complete plan as an `.ics` file.
        """
    )


# =========================================================
# 18. FOOTER
# =========================================================

st.divider()

st.caption(
    "🌌 StudySync | Adaptive Smart Study Planner | Member C UI & Visualization"
)