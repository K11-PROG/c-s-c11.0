import streamlit as st
import json
from datetime import datetime

# ---- Load JSON safely ----
def load_json(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        st.error(f"File not found: {path}")
        return {}
    except json.JSONDecodeError:
        st.error(f"Error decoding JSON in: {path}")
        return {}

# ---- Load calendar and meditations ----
calendar = load_json("data/calendar_2025_en.json")
meditations = load_json("data/meditations_2025_en.json")

st.title("📅 Catholic Saints Calendar (2025)")
st.write("Daily saints, feast types, liturgical colors, history, and meditations.")

# ---- Date selector (show ALL dates from JSON) ----
all_dates = sorted(calendar.keys())  # ✅ gets every date available
if not all_dates:
    st.error("No dates found in calendar JSON.")
else:
    today = datetime.today().strftime("%Y-%m-%d")
    default_date = today if today in all_dates else all_dates[0]

    selected_date = st.selectbox(
        "Select a date:",
        all_dates,
        index=all_dates.index(default_date)
    )

    # ---- Display calendar info ----
    if selected_date in calendar:
        day_info = calendar[selected_date]
        st.subheader(f"{selected_date} – {day_info.get('saint','Unknown')}")
        st.markdown(f"**Feast Type:** {day_info.get('feast_type','N/A')}")
        st.markdown(f"**Liturgical Color:** {day_info.get('liturgical_color','N/A')}")
        st.markdown(f"**History:** {day_info.get('history','')}")

        # ---- Meditation ----
        meditation = meditations.get(selected_date, "No meditation available.")
        st.markdown("### 🕊 Meditation")
        st.write(meditation)
    else:
        st.warning(f"No entry found for {selected_date}")
