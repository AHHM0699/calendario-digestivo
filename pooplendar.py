import streamlit as st
import json
from datetime import datetime, date
import calendar
from pathlib import Path

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="Pooplendar",
    page_icon="💩",
    layout="centered"
)

DATA_FILE = Path("data.json")

# ---------------- DATA ----------------
def load_data():
    if DATA_FILE.exists():
        return json.loads(DATA_FILE.read_text(encoding="utf-8"))
    return {}

def save_data(data):
    DATA_FILE.write_text(
        json.dumps(data, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

data = load_data()

# ---------------- LOGIC ----------------
def register_event():
    today = date.today().isoformat()
    now = datetime.now().strftime("%H:%M")
    data.setdefault(today, []).append({
        "time": now,
        "notes": ""
    })
    save_data(data)
    st.success(f"Registro guardado – {now}")

# ---------------- UI ----------------
st.title("Pooplendar")
st.caption("Registro simple y rápido")

# ---------------- 💩 BOTÓN REAL ----------------
st.markdown(
    """
    <style>
    .poop-btn button {
        font-size: 64px;
        height: 110px;
        width: 110px;
        border-radius: 24px;
        margin: auto;
        display: block;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="poop-btn">', unsafe_allow_html=True)
if st.button("💩"):
    register_event()
st.markdown('</div>', unsafe_allow_html=True)

st.divider()

# ---------------- CALENDARIO MOBILE-FIRST ----------------
today = date.today()
year, month = today.year, today.month
month_calendar = calendar.monthcalendar(year, month)

st.subheader(f"{calendar.month_name[month]} {year}")

# Días de la semana
st.markdown(
    """
    <div style="display:grid; grid-template-columns: repeat(7, 1fr); text-align:center; font-weight:bold;">
        <div>L</div><div>M</div><div>X</div><div>J</div><div>V</div><div>S</div><div>D</div>
    </div>
    """,
    unsafe_allow_html=True
)

# CSS de la grilla
st.markdown(
    """
    <style>
    .calendar-grid {
        display: grid;
        grid-template-columns: repeat(7, 1fr);
        gap: 6px;
        margin-top: 6px;
    }
    .calendar-grid button {
        height: 52px;
        border-radius: 12px;
        padding: 0;
    }
    </style>
    """,
    unsafe_allow_html=True
)

selected_day = None

st.markdown('<div class="calendar-grid">', unsafe_allow_html=True)

for week in month_calendar:
    for day in week:
        if day == 0:
            st.markdown("<div></div>", unsafe_allow_html=True)
        else:
            d_str = date(year, month, day).isoformat()
            count = len(data.get(d_str, []))
            label = f"{day}"
            if count > 0:
                label += "💩" * min(count, 3)

            if st.button(label, key=d_str):
                selected_day = d_str

st.markdown('</div>', unsafe_allow_html=True)

# ---------------- DETALLE DEL DÍA ----------------
if selected_day:
    st.divider()
    st.subheader(f"📅 {selected_day}")

    events = data.get(selected_day, [])

    if not events:
        st.info("No hay registros este día.")
    else:
        for i, ev in enumerate(events):
            with st.expander(f"🕒 {ev['time']}"):
                ev["notes"] = st.text_area(
                    "Notas (opcional)",
                    ev["notes"],
                    key=f"{selected_day}_{i}_notes"
                )

                if st.button(
                    "🗑️ Eliminar registro",
                    key=f"del_{selected_day}_{i}"
                ):
                    events.pop(i)
                    save_data(data)
                    st.experimental_rerun()
