
import json, os
import streamlit as st

st.set_page_config(page_title="Catholic Saints Calendar — Minimal", layout="centered")
st.title("Catholic Saints Calendar — Minimal (August 2025, EN)")

CAL_FILE = "data/calendar_2025_en.json"
MED_FILE = "data/meditations_2025_en.json"
NOTES_DIR = "notes"

def load_json(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        st.error(f"Required file not found: {path}")
        st.stop()

calendar = load_json(CAL_FILE)
meditations = load_json(MED_FILE)

dates = sorted(calendar.keys())
idx_default = dates.index("2025-08-01") if "2025-08-01" in dates else 0
chosen = st.selectbox("Select a date", dates, index=idx_default)

st.subheader(chosen)
st.write(f"**Saint/Feast:** {calendar.get(chosen, '—')}")

st.markdown("### Meditation")
st.info(meditations.get(chosen, "No meditation available."))

os.makedirs(NOTES_DIR, exist_ok=True)
note_path = os.path.join(NOTES_DIR, f"{chosen}.txt")
existing = ""
if os.path.exists(note_path):
    try:
        with open(note_path, "r", encoding="utf-8") as f:
            existing = f.read()
    except Exception:
        existing = ""

text = st.text_area("Your notes for this date:", value=existing, height=150)
if st.button("Save note"):
    try:
        with open(note_path, "w", encoding="utf-8") as f:
            f.write(text)
        st.success("Note saved.")
    except Exception as e:
        st.error(f"Could not save note: {e}")
