import streamlit as st
import json
from datetime import datetime, date
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

# 💩 BOTÓN GRANDE REAL
st.markdown(
    """
    <style>
    .stButton > button {
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

if st.button("💩"):
    register_event()

st.divider()

# ---------------- CALENDARIO MENSUAL NATIVO ----------------
st.subheader("📅 Calendario")

selected_date = st.date_input(
    "Selecciona un día",
    value=date.today()
)

selected_day = selected_date.isoformat()
selected_year = selected_date.year
selected_month = selected_date.month

# ---------------- RESUMEN VISUAL DEL MES ----------------
st.subheader("🟤 Resumen del mes")

month_days = {
    d: len(events)
    for d, events in data.items()
    if date.fromisoformat(d).year == selected_year
    and date.fromisoformat(d).month == selected_month
}

if not month_days:
    st.info("No hay registros este mes.")
else:
    for d in sorted(month_days):
        day_num = int(d.split("-")[2])
        count = month_days[d]
        dots = "💩" * min(count, 5)
        st.markdown(f"**Día {day_num}** {dots}")

st.divider()

# ---------------- DETALLE DEL DÍA ----------------
st.subheader(f"Registros del {selected_date.strftime('%d/%m/%Y')}")

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
