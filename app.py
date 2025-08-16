import json, os
import streamlit as st

st.set_page_config(page_title="Catholic Saints Calendar — Minimal", layout="centered")
st.title("Catholic Saints Calendar — August 2025 (English) — Minimal with Liturgical Colors")

CAL_FILE = "data/calendar_2025_en.json"
MED_FILE = "data/meditations_2025_en.json"
NOTES_DIR = "notes"

LITURGICAL_COLOR_LABELS = {
    "green": "Green — Ordinary Time",
    "white": "White — Feasts of the Lord/Mary/Non-martyrs",
    "red": "Red — Martyrs/Apostles/Holy Spirit",
    "violet": "Violet — Advent/Lent/Penance",
    "rose": "Rose — Gaudete/Laetare",
    "black": "Black — All Souls (optional)"
}

COLOR_SWATCH = {
    "green": "#2e7d32",
    "white": "#e0e0e0",
    "red": "#c62828",
    "violet": "#6a1b9a",
    "rose": "#c2185b",
    "black": "#212121"
}

def load_json(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        st.error(f"Required file not found: {path}")
        st.stop()
    except json.JSONDecodeError as e:
        st.error(f"JSON parse error in {path}: {e}")
        st.stop()

calendar = load_json(CAL_FILE)
meditations = load_json(MED_FILE)

dates = sorted(calendar.keys())
if not dates:
    st.error("Calendar is empty."); st.stop()

default_date = "2025-08-01" if "2025-08-01" in dates else dates[0]
chosen = st.selectbox("Select a date", dates, index=dates.index(default_date))

entry = calendar.get(chosen, {})
title = entry.get("title", "—")
color = entry.get("color", "green")
color_name = LITURGICAL_COLOR_LABELS.get(color, color.capitalize())

st.subheader(chosen)
st.write(f"**Saint/Feast:** {title}")

swatch = COLOR_SWATCH.get(color, "#9e9e9e")
st.markdown(
    f'''
    <div style="display:inline-flex;align-items:center;gap:.5rem;
                padding:.35rem .6rem;border-radius:999px;
                background:rgba(0,0,0,.03);border:1px solid rgba(0,0,0,.08)">
        <span style="display:inline-block;width:14px;height:14px;border-radius:50%;
                     background:{swatch};border:1px solid rgba(0,0,0,.25)"></span>
        <span style="font-size:0.9rem">{color_name}</span>
    </div>
    ''',
    unsafe_allow_html=True
)

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
