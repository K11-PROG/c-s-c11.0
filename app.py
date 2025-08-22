import streamlit as st
import json
from datetime import date

# --------------------------
# Load data
# --------------------------
with open("data/calendar_2025_en.json", "r", encoding="utf-8") as f:
    calendar_data = json.load(f)

with open("data/meditations_2025_en.json", "r", encoding="utf-8") as f:
    meditations_data = json.load(f)

# --------------------------
# App configuration
# --------------------------
st.set_page_config(
    page_title="Catholic Saints Calendar 2025",
    layout="wide"
)

# --------------------------
# Background image placeholder
# --------------------------
# Put your image in a folder called "static" (e.g. static/background.jpg)
background_image_path = "static/background.jpg"

page_bg = f"""
<style>
[data-testid="stAppViewContainer"] {{
    background: url("{background_image_path}");
    background-size: cover;
    background-attachment: fixed;
    background-position: center;
}}
[data-testid="stSidebar"] {{
    background-color: rgba(255, 255, 255, 0.8);
}}
</style>
"""

st.markdown(page_bg, unsafe_allow_html=True)

# --------------------------
# Main UI
# --------------------------
st.title("📅 Catholic Saints Calendar 2025 (English)")

# Default to today's date if available
today = str(date.today())
selected_date = st.sidebar.date_input("Select a date", value=date.today())
selected_date_str = selected_date.strftime("%Y-%m-%d")

if selected_date_str in calendar_data:
    info = calendar_data[selected_date_str]
    st.subheader(info["saint"])
    st.write(f"**Feast Type:** {info.get('feast_type', 'N/A')}")
    st.write(f"**Liturgical Color:** {info.get('liturgical_color', 'N/A')}")
    st.write(f"**History:** {info.get('history', '')}")

    if selected_date_str in meditations_data:
        st.markdown("### 🕊️ Meditation")
        st.write(meditations_data[selected_date_str])
    else:
        st.info("No meditation available for this day yet.")
else:
    st.warning("No saint or feast found for this date.")
