import streamlit as st
import json
from datetime import date

# Load data
with open("calendar_2025_en.json", "r", encoding="utf-8") as f:
    calendar_data = json.load(f)

with open("meditations_2025_en.json", "r", encoding="utf-8") as f:
    meditation_data = json.load(f)

today = str(date.today())

# Sidebar - pick a date
selected_date = st.sidebar.date_input("Choose a date", date.today())
selected_date_str = str(selected_date)

data = calendar_data.get(selected_date_str)
meditation = meditation_data.get(selected_date_str, {})

if data:
    st.title(f"{selected_date_str} — {data['saint']}")
    st.subheader(f"{data['feast_type']} • {data['liturgical_color']}")
    st.write(data["history"])

    # Optional: background
    if data.get("background"):
        st.markdown(
            f"""
            <style>
            .stApp {{
                background: url('{data['background']}');
                background-size: cover;
                background-attachment: fixed;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )

    # Optional: saint image
    if data.get("image"):
        st.image(data["image"], caption=data["saint"], use_container_width=True)

    # Optional: saint quote
    if data.get("quote"):
        st.info(f"💬 {data['quote']}")

    # Meditation
    if meditation.get("meditation"):
        st.markdown("### Daily Meditation")
        st.write(meditation["meditation"])

    # Optional meditation image
    if meditation.get("image"):
        st.image(meditation["image"], caption="Meditation", use_container_width=True)

    # Optional meditation background
    if meditation.get("background"):
        st.markdown(
            f"""
            <style>
            .stApp {{
                background: url('{meditation['background']}');
                background-size: cover;
                background-attachment: fixed;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )

    # Optional meditation quote
    if meditation.get("quote"):
        st.success(f"✨ {meditation['quote']}")

else:
    st.warning("No data found for this date.")
