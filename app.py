import streamlit as st
import json, os, calendar
from datetime import datetime, date, timedelta

st.set_page_config(page_title="Catholic Saints Calendar", layout="wide")

@st.cache_data
def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

DATA_CAL = "data/calendar_2025_en.json"
DATA_MED = "data/meditations_2025_en.json"

missing = [p for p in (DATA_CAL, DATA_MED) if not os.path.exists(p)]
if missing:
    st.error("Required file(s) missing:\n" + "\n".join(missing))
    st.stop()

calendar_data = load_json(DATA_CAL)     # { "YYYY-MM-DD": {...} }
meditations_data = load_json(DATA_MED)  # { "YYYY-MM-DD": "..." or {...} }

# ---------- helpers ----------
def to_date(s): return datetime.strptime(s, "%Y-%m-%d").date()
def month_key(d: date): return f"{d.year:04d}-{d.month:02d}"
def month_label(y, m): return date(y, m, 1).strftime("%B %Y")
def normalize_entry(day_str):
    """Accept either 'color' or 'liturgical_color', and optional feast_type/history."""
    e = calendar_data.get(day_str, {}) or {}
    saint = e.get("saint") or e.get("title") or "(Unknown)"
    color = e.get("liturgical_color") or e.get("color") or "Green"
    ftype = e.get("feast_type") or e.get("type") or None
    history = e.get("history")
    # meditation may live in meditations file as str or object
    med_entry = meditations_data.get(day_str)
    if isinstance(med_entry, dict):
        meditation = med_entry.get("meditation") or med_entry.get("reflection") or ""
        # prefer richer history if meditation file carries it
        history = med_entry.get("history") or history
    else:
        meditation = med_entry or ""
    return saint, color, ftype, history, meditation

def month_days(y, m):
    """All dates in the month as date objects."""
    last = calendar.monthrange(y, m)[1]
    return [date(y, m, d) for d in range(1, last + 1)]

# ---------- months available ----------
all_dates = sorted({to_date(k) for k in set(calendar_data.keys()) | set(meditations_data.keys())})
if not all_dates:
    st.error("No dates found in the dataset.")
    st.stop()

# Build a distinct, ordered list of months based on min..max in data
first_d, last_d = min(all_dates), max(all_dates)
months = []
y, m = first_d.year, first_d.month
while (y < last_d.year) or (y == last_d.year and m <= last_d.month):
    months.append((y, m))
    if m == 12: y, m = y + 1, 1
    else: m += 1

labels = [month_label(y, m) for (y, m) in months]
label_to_ym = dict(zip(labels, months))

st.title("Catholic Saints Calendar (robust month view)")
st.caption("Shows every day of the selected month. Missing days are clearly flagged so you can complete the data.")

# ---------- sidebar ----------
st.sidebar.header("Navigate")
sel_label = st.sidebar.selectbox("Month", labels)
sel_year, sel_month = label_to_ym[sel_label]

# Compile full month day list and mark coverage
days = month_days(sel_year, sel_month)
ds_strings = [d.strftime("%Y-%m-%d") for d in days]

present = {d for d in ds_strings if (d in calendar_data) or (d in meditations_data)}
missing_days = [d for d in ds_strings if d not in present]
coverage = int(round(100 * (len(present) / len(ds_strings)))) if ds_strings else 0

st.metric("Month coverage", f"{coverage}%")
if missing_days:
    with st.expander(f"Show missing days ({len(missing_days)})"):
        st.write(", ".join(missing_days))

# Optional search inside selected month
query = st.sidebar.text_input("Search (saint / color / text)", placeholder="e.g., Augustine, Rosary, martyr")
def matches(day_str):
    saint, color, ftype, history, meditation = normalize_entry(day_str)
    hay = " ".join([saint or "", color or "", ftype or "", history or "", meditation or ""]).lower()
    return (query or "").lower() in hay

# ---------- date picker (always lists all month days) ----------
def fmt_day(d: date): return d.strftime("%a %d %b %Y")
day_choice = st.sidebar.selectbox("Date", days, format_func=fmt_day,
                                  index=days.index(date.today()) if date(sel_year, sel_month, 1) <= date.today() <= date(sel_year, sel_month, calendar.monthrange(sel_year, sel_month)[1]) else 0)

day_str = day_choice.strftime("%Y-%m-%d")
saint, color, ftype, history, meditation = normalize_entry(day_str)

# Provide graceful defaults for missing entries
if day_str in missing_days:
    # Sunday detection for better default type/color
    dow = day_choice.weekday()  # 0=Mon..6=Sun
    default_type = "Sunday" if dow == 6 else "Weekday"
    default_color = "Green" if default_type in ("Weekday", "Sunday") else "Green"
    saint = saint if saint != "(Unknown)" else (default_type + " in Ordinary Time")
    color = color or default_color
    ftype = ftype or default_type
    history = history or "No entry yet. Add to data/calendar_2025_en.json."
    meditation = meditation or "No meditation yet. Add to data/meditations_2025_en.json."

st.subheader(f"{fmt_day(day_choice)} — {saint}")
meta = []
if ftype: meta.append(f"**Feast type:** {ftype}")
if color: meta.append(f"**Liturgical color:** {color}")
if meta: st.markdown(" · ".join(meta))

c1, c2 = st.columns(2)
with c1:
    st.markdown("### History / Biography")
    st.write(history or "—")
with c2:
    st.markdown("### Reflection / Meditation")
    st.write(meditation or "—")

st.divider()
st.caption("Tip: If some days look missing, use the expander above and paste the needed entries into your JSON files. This view always shows the full real calendar month.")
