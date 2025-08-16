import streamlit as st
import json
from datetime import date as dt

st.set_page_config(page_title="Catholic Saints Calendar", layout="centered")

@st.cache_data
def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

calendar_data = load_json("data/calendar_2025_en.json")
meditations_data = load_json("data/meditations_2025_en.json")

def ymd_to_month_label(ymd: str) -> str:
    y, m, _ = ymd.split("-")
    import calendar as cal
    return f"{cal.month_name[int(m)]} {y}"

def sorted_dates(dates):
    return sorted(dates)

all_types = sorted({v.get("type","") for v in calendar_data.values() if v.get("type")})
all_colors = sorted({v.get("color","") for v in calendar_data.values() if v.get("color")})
months_present = sorted({ymd_to_month_label(k) for k in calendar_data.keys()},
                        key=lambda s: (int(s.split()[-1]), __import__("calendar").month_name.index(s.split()[0])))

st.sidebar.header("Filters")
month_label = st.sidebar.selectbox("Month", options=months_present)
q = st.sidebar.text_input("Search (saint, feast, text)")
type_filter = st.sidebar.multiselect("Feast Type", options=all_types)
color_filter = st.sidebar.multiselect("Liturgical Color", options=all_colors)

dates_in_month = [d for d in calendar_data.keys() if ymd_to_month_label(d) == month_label]

def match_filters(ymd):
    item = calendar_data[ymd]
    if type_filter and item.get("type") not in type_filter:
        return False
    if color_filter and item.get("color") not in color_filter:
        return False
    if q:
        ql = q.lower()
        hay = " ".join([
            item.get("feast",""),
            " ".join(item.get("saints",[])),
            meditations_data.get(ymd,{}).get("history",""),
            meditations_data.get(ymd,{}).get("reflection",""),
        ]).lower()
        if ql not in hay:
            return False
    return True

filtered_dates = [d for d in dates_in_month if match_filters(d)]
if not filtered_dates:
    filtered_dates = sorted_dates(dates_in_month)

date_choice = st.sidebar.selectbox("Date", options=sorted_dates(filtered_dates))

item = calendar_data[date_choice]
med = meditations_data.get(date_choice, {"history":"No history available.","reflection":"No reflection available."})

st.title("📅 Catholic Saints Calendar 2025 (Phase 2.3)")
st.caption("Search + filters + month switcher + fixed date dropdown")

st.subheader(f"{date_choice} — {item['feast']}")
if item.get("saints"):
    st.write(f"**Saint(s):** {', '.join(item['saints'])}")
st.write(f"**Feast Type:** {item.get('type','—')}")
st.write(f"**Liturgical Color:** {item.get('color','—')}")

st.markdown('---')
st.header('📖 History / Biography')
st.write(med.get('history','No history available.'))

st.header('🙏 Reflection / Meditation')
st.write(med.get('reflection','No reflection available.'))

st.markdown('---')
st.subheader('📝 Personal Notes')
note_file = f"notes/{date_choice}.txt"
existing = ''
try:
    with open(note_file, 'r', encoding='utf-8') as f:
        existing = f.read()
except FileNotFoundError:
    pass

note_text = st.text_area('Write your note for this day:', value=existing, height=150)
if st.button('Save Note'):
    with open(note_file, 'w', encoding='utf-8') as f:
        f.write(note_text)
    st.success('Note saved!')
