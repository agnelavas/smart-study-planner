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
    create_user,
    login_user,
    load_profile,
    save_profile,
    save_subject,
    load_subjects,
    delete_subject,
    save_schedule,
    load_schedule,
    delete_schedule,
)

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
# DATABASE
# =========================================================

create_tables()


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="StudySync - Smart Study Planner",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# THEMES
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
# SESSION STATE
# =========================================================

if "logged_in" not in st.session_state:

    st.session_state.logged_in = False


if "user_id" not in st.session_state:

    st.session_state.user_id = None


if "username" not in st.session_state:

    st.session_state.username = ""


if "student_name" not in st.session_state:

    st.session_state.student_name = ""


if "subjects" not in st.session_state:

    st.session_state.subjects = []


if "schedule_df" not in st.session_state:

    st.session_state.schedule_df = pd.DataFrame()


if "edit_profile" not in st.session_state:

    st.session_state.edit_profile = False


# =========================================================
# LOGIN / SIGN UP PAGE
# =========================================================

if not st.session_state.logged_in:

    st.markdown(
        """
        <style>

        .login-title {
            font-size: 48px;
            font-weight: 800;
            text-align: center;
            margin-top: 40px;
        }

        .login-subtitle {
            text-align: center;
            font-size: 18px;
            opacity: 0.75;
            margin-bottom: 30px;
        }

        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="login-title">🌌 StudySync</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="login-subtitle">Your Personalized Smart Study Planner</div>',
        unsafe_allow_html=True
    )

    tab1, tab2 = st.tabs([
        "🔐 Login",
        "📝 Create Account"
    ])


    # =====================================================
    # LOGIN
    # =====================================================

    with tab1:

        st.subheader("Welcome Back 👋")

        login_username = st.text_input(
            "Username",
            key="login_username"
        )

        login_password = st.text_input(
            "Password",
            type="password",
            key="login_password"
        )

        if st.button(
            "🔐 Login",
            type="primary",
            use_container_width=True
        ):

            if not login_username or not login_password:

                st.error(
                    "Please enter username and password."
                )

            else:

                user = login_user(
                    login_username,
                    login_password
                )

                if user:

                    st.session_state.logged_in = True

                    st.session_state.user_id = user[0]

                    st.session_state.username = user[1]

                    st.session_state.student_name = user[2]

                    st.session_state.subjects = load_subjects(
                        user[0]
                    )

                    for subject in st.session_state.subjects:

                        try:

                            subject["exam_date"] = date.fromisoformat(
                                subject["exam_date"]
                            )

                        except Exception:

                            pass


                    st.session_state.schedule_df = load_schedule(
                        user[0]
                    )

                    st.success(
                        "✅ Login successful!"
                    )

                    st.rerun()

                else:

                    st.error(
                        "❌ Invalid username or password."
                    )


    # =====================================================
    # CREATE ACCOUNT
    # =====================================================

    with tab2:

        st.subheader("Create Your StudySync Account 🚀")

        new_name = st.text_input(
            "Full Name",
            key="new_name"
        )

        new_username = st.text_input(
            "Create Username",
            key="new_username"
        )

        new_email = st.text_input(
            "Email",
            key="new_email"
        )

        new_phone = st.text_input(
            "Phone Number",
            key="new_phone"
        )

        new_college = st.text_input(
            "College",
            key="new_college"
        )

        new_semester = st.text_input(
            "Semester",
            placeholder="Example: 3rd Semester",
            key="new_semester"
        )

        new_password = st.text_input(
            "Create Password",
            type="password",
            key="new_password"
        )

        confirm_password = st.text_input(
            "Confirm Password",
            type="password",
            key="confirm_password"
        )


        if st.button(
            "📝 Create Account",
            type="primary",
            use_container_width=True
        ):

            if not new_name.strip():

                st.error("Please enter your name.")

            elif not new_username.strip():

                st.error("Please create a username.")

            elif not new_password:

                st.error("Please create a password.")

            elif len(new_password) < 4:

                st.error(
                    "Password should contain at least 4 characters."
                )

            elif new_password != confirm_password:

                st.error(
                    "Passwords do not match."
                )

            else:

                user_id = create_user(
                    new_username,
                    new_password,
                    new_name,
                    new_email,
                    new_phone,
                    new_college,
                    new_semester
                )

                if user_id:

                    st.success(
                        "🎉 Account created successfully! Please login."
                    )

                else:

                    st.error(
                        "❌ Username already exists. Please choose another username."
                    )


    st.stop()


# =========================================================
# LOGOUT FUNCTION
# =========================================================

def logout():

    st.session_state.logged_in = False

    st.session_state.user_id = None

    st.session_state.username = ""

    st.session_state.student_name = ""

    st.session_state.subjects = []

    st.session_state.schedule_df = pd.DataFrame()

    st.session_state.edit_profile = False


# =========================================================
# CURRENT USER
# =========================================================

user_id = st.session_state.user_id


# =========================================================
# 1. SIDEBAR
# =========================================================

with st.sidebar:

    st.header("🌌 StudySync")

    st.caption(
        "Personalized Smart Study Planner"
    )


    # =====================================================
    # THEME
    # =====================================================

    theme_name = st.selectbox(
        "🎨 Choose Theme",
        list(THEMES.keys())
    )

    theme = THEMES[theme_name]

    st.divider()


    # =====================================================
    # STUDENT PROFILE
    # =====================================================

    st.subheader("👤 Student Profile")

    saved_profile = load_profile(user_id)


    if (
        saved_profile
        and saved_profile[0]
        and not st.session_state.edit_profile
    ):

        st.write(
            f"**Name:** {saved_profile[0]}"
        )

        st.caption(
            f"Username: @{st.session_state.username}"
        )

        if st.button(
            "✏️ Edit Profile",
            use_container_width=True
        ):

            st.session_state.edit_profile = True

            st.rerun()


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
            value=default_name
        )

        email = st.text_input(
            "📧 Email",
            value=default_email
        )

        phone = st.text_input(
            "📱 Phone Number",
            value=default_phone
        )

        college = st.text_input(
            "🏫 College",
            value=default_college
        )

        semester = st.text_input(
            "🎓 Semester",
            value=default_semester
        )


        if st.button(
            "💾 Save Profile",
            use_container_width=True
        ):

            if not student_name.strip():

                st.error(
                    "Please enter your name."
                )

            else:

                save_profile(
                    user_id,
                    student_name,
                    email,
                    phone,
                    college,
                    semester
                )

                st.session_state.student_name = student_name

                st.session_state.edit_profile = False

                st.success(
                    "✅ Profile saved!"
                )

                st.rerun()


    st.divider()


    # =====================================================
    # LOGOUT
    # =====================================================

    if st.button(
        "🚪 Logout",
        use_container_width=True
    ):

        logout()

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
        step=0.5
    )

    start_date = st.date_input(
        "Start Date",
        value=date.today()
    )

    taper_eve = st.checkbox(
        "Exam-Eve Cognitive Taper (50% Load)",
        value=True
    )


    st.divider()


    # =====================================================
    # FOCUS AUDIO
    # =====================================================

    st.subheader("🎵 Focus Audio")

    audio_url = st.text_input(
        "Focus Audio URL",
        placeholder="Paste audio/YouTube URL"
    )

    if audio_url:

        st.markdown(
            f"[🎧 Open Focus Audio]({audio_url})"
        )


# =========================================================
# CUSTOM CSS
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
    unsafe_allow_html=True
)


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="main-title">🌌 StudySync</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Adaptive, Urgency-Weighted Smart Study Planner</div>',
    unsafe_allow_html=True
)


if st.session_state.student_name:

    st.success(
        f"Welcome, {st.session_state.student_name}! 👋"
    )


# =========================================================
# KPI SECTION
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
        subject_count
    )


with k2:

    st.metric(
        "⏱️ Revision Volume",
        f"{total_hours:.1f} hrs"
    )


with k3:

    st.metric(
        "🎯 Nearest Exam",
        exam_days
    )


with k4:

    st.metric(
        "⚡ Daily Capacity",
        f"{daily_hours:.1f} hrs/day"
    )


# =========================================================
# BUILD STUDY PLAN
# =========================================================

st.divider()

st.header(
    "📝 Build Your Personal Study Plan"
)

st.write(
    "Add your subjects and create your personalized timetable."
)


with st.expander(
    "➕ Add a Subject",
    expanded=True
):

    with st.form(
        "add_subject_form",
        clear_on_submit=True
    ):

        col1, col2 = st.columns(2)


        with col1:

            subject_name = st.text_input(
                "Subject Name",
                placeholder="Example: Data Structures"
            )

            chapters = st.number_input(
                "Number of Chapters / Units",
                min_value=1,
                max_value=100,
                value=5,
                step=1
            )


        with col2:

            difficulty = st.slider(
                "Difficulty",
                min_value=1,
                max_value=5,
                value=3
            )

            exam_date = st.date_input(
                "Exam Date",
                value=date.today() + timedelta(days=7),
                min_value=date.today()
            )


        submitted = st.form_submit_button(
            "➕ Add Subject",
            type="primary",
            use_container_width=True
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
                    user_id,
                    subject_name.strip(),
                    int(chapters),
                    int(difficulty),
                    exam_date
                )

                st.session_state.subjects = load_subjects(
                    user_id
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
# SUBJECT ROSTER
# =========================================================

st.subheader(
    "📋 Your Subject Roster"
)


if not st.session_state.subjects:

    st.info(
        "No subjects added yet. Use 'Add a Subject' above."
    )

else:

    for subject in st.session_state.subjects:

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
                key=f"delete_subject_{subject['id']}"
            ):

                delete_subject(
                    user_id,
                    subject["id"]
                )

                st.session_state.subjects = load_subjects(
                    user_id
                )

                st.session_state.schedule_df = pd.DataFrame()

                delete_schedule(
                    user_id
                )

                st.rerun()


# =========================================================
# GENERATE TIMETABLE
# =========================================================

if st.session_state.subjects:

    st.divider()


    if st.button(
        "🚀 Generate My Personalized Study Timetable",
        type="primary",
        use_container_width=True
    ):

        try:

            with st.spinner(
                "Creating your personalized timetable..."
            ):

                schedule = generate_study_plan(
                    st.session_state.subjects,
                    start_date,
                    daily_hours,
                    taper_exam_eve=taper_eve
                )

                st.session_state.schedule_df = schedule

                save_schedule(
                    user_id,
                    schedule
                )


            st.success(
                "🎉 Your personalized timetable has been generated!"
            )

            st.rerun()


        except Exception as e:

            st.error(
                "Could not generate the timetable."
            )

            st.exception(e)


# =========================================================
# CURRENT TIMETABLE
# =========================================================

if not st.session_state.schedule_df.empty:

    st.divider()

    st.header(
        "📅 Your Generated Study Timetable"
    )

    st.dataframe(
        st.session_state.schedule_df,
        use_container_width=True,
        hide_index=True
    )


# =========================================================
# DYNAMIC CATCH-UP
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
            key="slacked_date"
        )


    with col2:

        st.write("")
        st.write("")


        if st.button(
            "⚠️ Slacked Off Today? Rebalance Plan",
            use_container_width=True
        ):

            current_df = (
                st.session_state.schedule_df.copy()
            )

            old_hours = current_df["Hours"].sum()


            new_schedule = panic_rebalance(
                current_df,
                slacked_date.strftime("%Y-%m-%d")
            )


            new_hours = new_schedule["Hours"].sum()


            st.session_state.schedule_df = new_schedule


            save_schedule(
                user_id,
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
# CALENDAR EXPORT
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
            use_container_width=True
        )


    except Exception:

        st.error(
            "Calendar export is currently unavailable."
        )


# =========================================================
# PLOTLY REVISION ROADMAP
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
                "Days Left"
            ]
            if c in df.columns
        ]
    )


    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =========================================================
# INTERACTIVE CHECKLIST
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
            "Days Left"
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
                    "Skipped"
                ],
                required=True
            )
        },
        disabled=disabled_columns,
        hide_index=True,
        use_container_width=True,
        key="revision_checklist"
    )


    st.session_state.schedule_df = edited_df


    save_schedule(
        user_id,
        edited_df
    )


# =========================================================
# COSMIC FOCUS
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
                            use_container_width=True
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
                "NASA picture is temporarily unavailable."
            )


    st.info(
        "💡 Focus tip: Study for 25–50 minutes, then take a short break."
    )


# =========================================================
# EMPTY STATE
# =========================================================

if (
    not st.session_state.subjects
    and st.session_state.schedule_df.empty
):

    st.divider()


    st.markdown(
        """
        ### 🚀 How StudySync Works

        **1️⃣ Create your account / Login**

        **2️⃣ Add your subjects**

        **3️⃣ Enter exam dates**

        **4️⃣ Set difficulty and chapters**

        **5️⃣ Set your daily study hours**

        **6️⃣ Generate your personalized timetable**

        **7️⃣ Track your progress**

        **8️⃣ Export your plan to your calendar**
        """
    )


# =========================================================
# FOOTER
# =========================================================

st.divider()


st.caption(
    "🌌 StudySync | Adaptive Smart Study Planner | Member C UI & Visualization"
)