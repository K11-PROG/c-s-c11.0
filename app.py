import streamlit as st
import json
from datetime import datetime

# Load calendar data
with open("data/calendar_2025_en.json") as f:
    calendar = json.load(f)

with open("data/meditations_2025_en.json") as f:
    meditations = json.load(f)

st.title("Catholic Saints Calendar (2025)")

today = datetime.today().strftime("%Y-%m-%d")
if today in calendar:
    feast = calendar[today]
    meditation = meditations.get(today, "No meditation available.")
    st.subheader(f"{today} – {feast['name']}")
    st.markdown(f"**Feast Type:** {feast['type']}")
    st.markdown(f"**Liturgical Color:** {feast['color']}")
    st.write(meditation)
else:
    st.write("Date not found in dataset. Showing first available date:")
    first_date = list(calendar.keys())[0]
    feast = calendar[first_date]
    meditation = meditations.get(first_date, "No meditation available.")
    st.subheader(f"{first_date} – {feast['name']}")
    st.markdown(f"**Feast Type:** {feast['type']}")
    st.markdown(f"**Liturgical Color:** {feast['color']}")
    st.write(meditation)
