import json
from datetime import date, datetime
from pathlib import Path
import streamlit as st

DATA_DIR = Path("data")
CAL_PATH = DATA_DIR / "calendar_2025_en.json"
MED_PATH = DATA_DIR / "meditations_2025_en.json"

@st.cache_data
def load_json(p: Path):
    with p.open("r", encoding="utf-8") as f:
        return json.load(f)

def ymd_to_label(ymd: str) -> str:
    dt = datetime.strptime(ymd, "%Y-%m-%d").date()
    return dt.strftime("%B %d, %Y")

def liturgical_badge(color: str) -> str:
    # Simple colored pill; tweak colors here.
    color_map = {
        "White": "#f5f5f5",
        "Red": "#ffdddd",
        "Green": "#ddffdd",
        "Violet": "#eadcff",
        "Rose": "#ffe6f2",
        "Black": "#eeeeee",
        "Gold": "#fff6cc",
    }
    fg_map = {
        "White": "#333",
        "Red": "#900",
        "Green": "#064",
        "Violet": "#5a2d82",
        "Rose": "#a11d5f",
        "Black": "#222",
        "Gold": "#7a6000",
    }
    bg = color_map.get(color, "#eeeeee")
    fg = fg_map.get(color, "#333")
    return f"""
    <span style="
      display:inline-block;padding:.20rem .55rem;border-radius:999px;
      background:{bg};color:{fg};font-size:.85rem;border:1px solid rgba(0,0,0,.06)
    ">{color}</span>
    """

def apply_background(url: str):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url('{url}');
            background-size: cover;
            background-attachment: fixed;
            background-repeat: no-repeat;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

def main():
    st.set_page_config(page_title="Catholic Saints Calendar 2025", layout="wide")

    if not CAL_PATH.exists() or not MED_PATH.exists():
        st.error("Required data files not found. Ensure data/calendar_2025_en.json and data/meditations_2025_en.json exist.")
        st.stop()

    calendar = load_json(CAL_PATH)
    meditations = load_json(MED_PATH)

    # Sidebar: date + search + filters
    st.sidebar.header("Browse")
    today = date.today()
    chosen = st.sidebar.date_input("Choose date", today)
    chosen_key = chosen.strftime("%Y-%m-%d")

    # Text search over saint name
    q = st.sidebar.text_input("Search saint/feast (live)", "")
    feast_types = sorted({v.get("feast_type", "Weekday") for v in calendar.values()})
    selected_types = st.sidebar.multiselect("Filter by feast type", feast_types, default=feast_types)
    colors = sorted({v.get("liturgical_color", "Green") for v in calendar.values()})
    selected_colors = st.sidebar.multiselect("Filter by color", colors, default=colors)

    # Build an index for the sidebar month/day list
    all_keys = sorted(calendar.keys())
    month_filter = st.sidebar.selectbox(
        "Jump to month",
        options=sorted({k[:7] for k in all_keys}),  # YYYY-MM
        index=sorted({k[:7] for k in all_keys}).index(chosen_key[:7]) if chosen_key[:7] in {k[:7] for k in all_keys} else 0
    )
    month_days = [k for k in all_keys if k.startswith(month_filter)]
    pick_day = st.sidebar.selectbox(
        "Day in month",
        options=month_days,
        index=month_days.index(chosen_key) if chosen_key in month_days else 0,
        format_func=ymd_to_label
    )

    # If search or filters applied, adjust the chosen day if needed
    def matches_filters(k: str, v: dict) -> bool:
        if q and q.lower() not in v.get("saint", "").lower():
            return False
        if v.get("feast_type", "Weekday") not in selected_types:
            return False
        if v.get("liturgical_color", "Green") not in selected_colors:
            return False
        return True

    filtered_keys = [k for k in all_keys if matches_filters(k, calendar[k])]
    if filtered_keys:
        if chosen_key not in filtered_keys:
            chosen_key = filtered_keys[0]
    else:
        st.sidebar.info("No results match your filters/search.")
        chosen_key = pick_day

    # Display chosen date
    record = calendar.get(chosen_key)
    med = meditations.get(chosen_key, {})

    if not record:
        st.warning("Date not found in dataset. Showing first available date.")
        chosen_key = all_keys[0]
        record = calendar[chosen_key]
        med = meditations.get(chosen_key, {})

    # Optional background: prefer meditation bg, else calendar bg
    bg = med.get("background") or record.get("background")
    if bg:
        apply_background(bg)

    # Header
    left, right = st.columns([3,1])
    with left:
        st.title(f"{ymd_to_label(chosen_key)} — {record.get('saint','')}")
        sub = f"{record.get('feast_type','')} • {record.get('liturgical_color','')}"
        st.markdown(sub)

    with right:
        st.markdown(liturgical_badge(record.get("liturgical_color","")), unsafe_allow_html=True)

    # Saint image (optional)
    if record.get("image"):
        st.image(record["image"], caption=record.get("saint",""), use_container_width=True)

    # Quote (optional)
    if record.get("quote"):
        st.info(f"💬 {record['quote']}")

    # History / bio (optional)
    if record.get("history"):
        st.markdown("#### About / History")
        st.write(record["history"])

    # Meditation
    if med.get("meditation"):
        st.markdown("### Daily Meditation")
        st.write(med["meditation"])

    # Optional extras for meditation
    if med.get("image"):
        st.image(med["image"], caption="Meditation", use_container_width=True)
    if med.get("quote"):
        st.success(f"✨ {med['quote']}")
    if med.get("prayer"):
        st.markdown("#### Closing Prayer")
        st.write(med["prayer"])

    st.divider()
    st.caption("Tip: put images in /images and backgrounds in /backgrounds. Paths in JSON should be relative (e.g., 'images/jerome.jpg').")

if __name__ == "__main__":
    main()
