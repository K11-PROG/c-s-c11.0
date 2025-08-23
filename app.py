import json
import streamlit as st
from pathlib import Path
from datetime import datetime

st.set_page_config(page_title="Catholic Saints Calendar 2025", layout="centered")

# --- Load JSON helper ---
def load_json(file_path):
    path = Path(file_path)
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        st.error(f"❌ Required file not found: {file_path}")
        st.stop()

# --- Load Data ---
calendar_data = load_json("data/calendar_2025_en.json")
meditations_data = load_json("data/meditations_2025_en.json")

# --- App UI ---
st.title("📅 Catholic Saints Calendar 2025")

# Default to today’s date if available
today = datetime.today().strftime("%Y-%m-%d")
if today in calendar_data:
    default_date = today
else:
    default_date = sorted(calendar_data.keys())[0]

selected_date = st.selectbox(
    "Select a date:",
    options=sorted(calendar_data.keys()),
    index=sorted(calendar_data.keys()).index(default_date),
)

# Display calendar entry
day_info = calendar_data[selected_date]

st.subheader(f"{selected_date} — {day_info.get('saint', 'Unknown')}")
st.markdown(f"**Feast Type:** {day_info.get('feast_type', 'N/A')}")
st.markdown(f"**Liturgical Color:** {day_info.get('liturgical_color', 'N/A')}")
st.markdown(f"**History:** {day_info.get('history', 'No details available.')}")

# Display meditation if exists
if selected_date in meditations_data:
    st.markdown("### 🕊️ Meditation")
    st.write(meditations_data[selected_date])
else:
    st.info("No meditation available for this date yet.")
