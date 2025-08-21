import streamlit as st
import json
import datetime
import os

# Paths to data files
CALENDAR_FILE = "data/calendar_2025_en.json"
MEDITATIONS_FILE = "data/meditations_2025_en.json"

# Load JSON helper
def load_json(path):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

# Load data
calendar_data = load_json(CALENDAR_FILE)
meditations_data = load_json(MEDITATIONS_FILE)

# App title
st.title("Catholic Saints Calendar 2025")

# Default to today's date
today = datetime.date.today()
selected_date = st.date_input("Select a date", today, min_value=datetime.date(2025,1,1), max_value=datetime.date(2025,12,31))
date_str = selected_date.strftime("%Y-%m-%d")

# Display calendar entry
if date_str in calendar_data:
    entry = calendar_data[date_str]
    st.subheader(f"📅 {entry.get('saint', 'Unknown')}")
    st.write(f"**Feast Type:** {entry.get('feast_type', '')}")
    st.write(f"**Liturgical Color:** {entry.get('liturgical_color', '')}")
    st.write(f"**History:** {entry.get('history', '')}")
else:
    st.warning("No entry found for this date.")

# Display meditation
if date_str in meditations_data:
    meditation = meditations_data[date_str].get("meditation", "")
    st.markdown(f"### 🕊️ Meditation\n{meditation}")
else:
    st.info("No meditation available for this date.")
