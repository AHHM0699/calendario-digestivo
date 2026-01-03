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

# ---------- ESTILOS ----------
st.markdown(
    """
    <style>
    /* Oculta el texto del botón pero mantiene el área clickeable */
    .poop-btn button {
        font-size: 0px;
        height: 110px;
        width: 110px;
        border-radius: 24px;
    }
    .poop-emoji {
        font-size: 90px;
        text-align: center;
        margin-top: -95px;
        pointer-events: none;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------- BOTÓN 💩 VISUAL ----------
c1, c2, c3 = st.columns([1,2,1])
with c2:
    st.markdown('<div class="poop-btn">', unsafe_allow_html=True)
    clicked = st.button("register_poop", key="poop_register")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div class="poop-emoji">💩</div>', unsafe_allow_html=True)

if clicked:
    register_event()

st.divider()

# ---------------- CALENDARIO ----------------
today = date.today()
year, month = today.year, today.month
cal = calendar.monthcalendar(year, month)

st.subheader(f"{calendar.month_name[month]} {year}")

days_header = ["L", "M", "X", "J", "V", "S", "D"]
cols = st.columns(7)
for i, d in enumerate(days_header):
    cols[i].markdown(f"**{d}**")

selected_day = None

for week in cal:
    cols = st.columns(7)
    for i, day in enumerate(week):
        if day == 0:
            cols[i].markdown(" ")
            continue

        d_str = date(year, month, day).isoformat()
        count = len(data.get(d_str, []))
        dots = "💩" * count
        label = f"{day}\n{dots}"

        if cols[i].button(label, key=d_str):
            selected_day = d_str

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
