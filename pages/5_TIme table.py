import streamlit as st
import pandas as pd
import os
import json
from datetime import datetime

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

# Generate 12-hour format time slots
def generate_12_hour_slots():
    slots = []
    for hour in range(6, 22):  # 6 AM to 9 PM
        t = datetime.strptime(f"{hour}:00", "%H:%M")
        slots.append(t.strftime("%I:%M %p"))
    return slots

TIME_SLOTS = generate_12_hour_slots()
TIMETABLE_FILE = "data/timetable.json"
os.makedirs("data", exist_ok=True)

def load_timetable():
    if os.path.exists(TIMETABLE_FILE):
        with open(TIMETABLE_FILE, "r") as f:
            data = json.load(f)
            df = pd.DataFrame(data)
            df.index = TIME_SLOTS  # Restore index properly
            return df
    else:
        return pd.DataFrame({day: ["" for _ in TIME_SLOTS] for day in DAYS}, index=TIME_SLOTS)

def save_timetable(df):
    df_to_save = df.to_dict()
    with open(TIMETABLE_FILE, "w") as f:
        json.dump(df_to_save, f, indent=2)

def render_timetable():
    st.title("📅 Weekly Timetable Planner (12-Hour Format)")
    st.markdown("Plan your daily subjects here. Data will auto-save.")

    df = load_timetable()

    edited_df = st.data_editor(df, use_container_width=True, num_rows="dynamic", key="editor",column_config={day: {"width": "200px"} for day in df.columns})

    if st.button("💾 Save Timetable"):
        save_timetable(edited_df)
        st.success("✅ Timetable saved successfully!")

    if st.button("📥 Reload Timetable"):
        st.experimental_rerun()
render_timetable()