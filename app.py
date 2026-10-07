import streamlit as st

# --------------------------------------------------
# Page settings
# --------------------------------------------------
st.set_page_config(
    page_title="StudySync",
    page_icon="🌌",
    layout="wide"
)

# --------------------------------------------------
# 4 Theme Options
# --------------------------------------------------
THEMES = {
    "🌌 Midnight Cosmos": {
        "background": "#0B0E14",
        "text": "#E2E8F0",
        "accent": "#A855F7"
    },

    "☕ Espresso Library": {
        "background": "#1C1614",
        "text": "#F4EBD9",
        "accent": "#D4AF37"
    },

    "📜 Parchment & Ink": {
        "background": "#FAF8F5",
        "text": "#2A2624",
        "accent": "#4E6E58"
    },

    "❄️ Nordic Aurora": {
        "background": "#F1F5F9",
        "text": "#1E293B",
        "accent": "#6366F1"
    }
}

# --------------------------------------------------
# Theme selector
# --------------------------------------------------
st.sidebar.title("🎨 Visual Atmosphere")

selected_theme = st.sidebar.selectbox(
    "Choose Theme",
    list(THEMES.keys())
)

theme = THEMES[selected_theme]

# --------------------------------------------------
# Apply theme
# --------------------------------------------------
st.markdown(
    f"""
    <style>
    .stApp {{
        background: {theme["background"]};
        color: {theme["text"]};
    }}

    h1, h2, h3, p, label {{
        color: {theme["text"]};
    }}

    .stButton button {{
        border: 1px solid {theme["accent"]};
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# --------------------------------------------------
# Main dashboard
# --------------------------------------------------
st.title("🌌 StudySync")
st.caption("Adaptive Revision Engine & Cosmic Study Lounge")

st.write("Welcome to your Smart Study Planner!")

# Dashboard boxes
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("📚 Subjects", 0)

with col2:
    st.metric("⏳ Study Hours", "0 hrs")

with col3:
    st.metric("🎯 Next Exam", "Not Set")

with col4:
    st.metric("⚡ Daily Hours", "5 hrs")