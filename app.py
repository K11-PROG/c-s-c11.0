import streamlit as st
import json
from datetime import date

st.set_page_config(page_title="Catholic Saints Calendar", layout="centered")

# Load data
with open("data/calendar_2025_en.json", "r", encoding="utf-8") as f:
    calendar_data = json.load(f)
with open("data/meditations_2025_en.json", "r", encoding="utf-8") as f:
    meditations_data = json.load(f)

# Today's date
today_str = date.today().strftime("%Y-%m-%d")
if today_str not in calendar_data:
    today_str = list(calendar_data.keys())[0]

day_info = calendar_data[today_str]
meditation_info = meditations_data.get(today_str, {"history": "No history available.", "reflection": "No reflection available."})

# UI
st.title("📅 Catholic Saints Calendar 2025")

st.subheader(f"{today_str} — {day_info['feast']}")
st.write(f"**Saint(s):** {', '.join(day_info['saints'])}")
st.write(f"**Liturgical Color:** 🟢 {day_info['color']}")

st.markdown("---")
st.header("📖 History / Biography")
st.write(meditation_info["history"])

st.header("🙏 Reflection / Meditation")
st.write(meditation_info["reflection"])

# Notes
st.markdown("---")
st.subheader("📝 Personal Notes")
note_file = f"notes/{today_str}.txt"
note = ""
try:
    with open(note_file, "r", encoding="utf-8") as f:
        note = f.read()
except FileNotFoundError:
    pass

user_note = st.text_area("Write your note:", value=note, height=150)
if st.button("Save Note"):
    with open(note_file, "w", encoding="utf-8") as f:
        f.write(user_note)
    st.success("Note saved!")