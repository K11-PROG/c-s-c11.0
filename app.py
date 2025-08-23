import json
import streamlit as st
from pathlib import Path
from datetime import datetime

st.set_page_config(page_title="Saints Calendar 2025", layout="centered")

def load_json(path):
    p = Path(path)
    if p.exists():
        with p.open("r", encoding="utf-8") as f:
            return json.load(f)
    else:
        st.error(f"Missing file: {path}")
        st.stop()

calendar = load_json("data/calendar_2025_en.json")
meditations = load_json("data/meditations_2025_en.json")

st.title("Catholic Saints Calendar 2025 (EN)")

# Default date selection
today = datetime.today().strftime("%Y-%m-%d")
default = today if today in calendar else sorted(calendar.keys())[0]
selected_date = st.selectbox("Select a date", sorted(calendar.keys()), index=sorted(calendar.keys()).index(default))

# Display entry
entry = calendar.get(selected_date, {})
st.subheader(f"{selected_date} — {entry.get('saint', 'Unknown')}")
st.write(f"**Feast Type:** {entry.get('feast_type', '')}")
st.write(f"**Liturgical Color:** {entry.get('liturgical_color', '')}")
st.write(f"**History:** {entry.get('history', '')}")

# Meditation
med = meditations.get(selected_date)
if med:
    st.markdown("### 🕊 Meditation")
    st.write(med)
else:
    st.info("No meditation for this date yet.")
