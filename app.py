import streamlit as st
import json
import os
from datetime import datetime, date

st.set_page_config(page_title="Catholic Saints Calendar", layout="wide")

@st.cache_data
def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

# --- Load data (calendar: saint+color; meditations: history+meditation) ---
CAL_PATH = "data/calendar_2025_en.json"
MED_PATH = "data/meditations_2025_en.json"

missing = []
if not os.path.exists(CAL_PATH): missing.append(CAL_PATH)
if not os.path.exists(MED_PATH): missing.append(MED_PATH)
if missing:
    st.error("Required file(s) missing:\n" + "\n".join(missing))
    st.stop()

calendar_data = load_json(CAL_PATH)           # { "YYYY-MM-DD": {"saint":..., "color":...}, ... }
meditations_data = load_json(MED_PATH)        # { "YYYY-MM-DD": {"history":..., "meditation":...}, ... }

# --- Helpers ---
def ymd(dstr):  # "YYYY-MM-DD" -> date
    return datetime.strptime(dstr, "%Y-%m-%d").date()

def month_key(dstr):  # "YYYY-MM"
    return dstr[:7]

def month_label(ym):  # "YYYY-MM" -> "Month YYYY"
    y, m = ym.split("-")
    return datetime(int(y), int(m), 1).strftime("%B %Y")

# Dates present (union of both files, sorted)
all_dates = sorted(set(calendar_data.keys()) | set(meditations_data.keys()))
if not all_dates:
    st.error("No dates found in dataset.")
    st.stop()

# Build months present (ordered by date)
months_ordered = []
seen = set()
for d in all_dates:
    mk = month_key(d)
    if mk not in seen:
        seen.add(mk)
        months_ordered.append(mk)

month_labels = [month_label(mk) for mk in months_ordered]
label_to_mk = dict(zip(month_labels, months_ordered))

st.title("Catholic Saints Calendar (Minimal — Aug–Nov 2025)")
st.caption("English only for now · Includes liturgical colors · History & Reflection separated")

# --- Sidebar controls ---
st.sidebar.header("Navigate")
selected_month_label = st.sidebar.selectbox("Month", month_labels)
selected_mk = label_to_mk[selected_month_label]

# Dates in selected month
month_dates = [d for d in all_dates if month_key(d) == selected_mk]
month_dates_sorted = sorted(month_dates, key=ymd)

# Search (filters days in this month)
query = st.sidebar.text_input("Search saint/feast or text", placeholder="e.g., Augustine, Mary, cross...")
if query:
    q = query.lower()
    def matches(d):
        cal = calendar_data.get(d, {})
        med = meditations_data.get(d, {})
        haystacks = [
            cal.get("saint", ""),
            cal.get("color", ""),
            med.get("history", ""),
            med.get("meditation", "")
        ]
        return any(q in h.lower() for h in haystacks if h)
    filtered = [d for d in month_dates_sorted if matches(d)]
    dates_for_dd = filtered if filtered else month_dates_sorted
    if not filtered:
        st.sidebar.warning("No results in this month; showing all days.")
else:
    dates_for_dd = month_dates_sorted

def fmt_date(d):
    return ymd(d).strftime("%a %d %b %Y")  # e.g., Mon 01 Aug 2025

selected_day = st.sidebar.selectbox("Date", dates_for_dd, format_func=fmt_date)

# --- Show entry ---
cal = calendar_data.get(selected_day, {})
med = meditations_data.get(selected_day, {})
saint = cal.get("saint", "(Unknown)")
color = cal.get("color", "(n/a)")
history = med.get("history", "—")
reflection = med.get("meditation", "—")

st.subheader(f"{fmt_date(selected_day)} — {saint}")
st.markdown(f"**Liturgical Color:** {color}")

col1, col2 = st.columns(2)
with col1:
    st.markdown("### History / Biography")
    st.write(history)
with col2:
    st.markdown("### Reflection / Meditation")
    st.write(reflection)

st.divider()
st.caption("Minimal dataset for reliability. We’ll expand month-by-month.")
