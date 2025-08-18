import streamlit as st
import json
import os

st.set_page_config(page_title="Catholic Saints Calendar", layout="wide")

# Load data
data_file = "data/calendar_2025_en.json"
if not os.path.exists(data_file):
    st.error(f"Required file not found: {data_file}")
else:
    with open(data_file, "r", encoding="utf-8") as f:
        calendar_data = json.load(f)

# Sidebar
st.sidebar.title("Navigation")
dates = sorted(calendar_data.keys())
selected_date = st.sidebar.selectbox("Select Date", dates)

# Search + Filter
query = st.sidebar.text_input("Search Saint or Feast")
if query:
    filtered_dates = [d for d, v in calendar_data.items() if query.lower() in v["saint"].lower()]
    if filtered_dates:
        selected_date = st.sidebar.selectbox("Results", filtered_dates)

# Main content
if selected_date in calendar_data:
    entry = calendar_data[selected_date]
    st.title(f"{selected_date} — {entry['saint']}")
    st.markdown(f"**Liturgical Color:** {entry['color']}")
    st.subheader("History / Biography")
    st.write(entry["history"])
    st.subheader("Reflection / Meditation")
    st.write(entry["meditation"])
else:
    st.error("Date not found in dataset.")
