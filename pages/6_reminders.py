import streamlit as st
import json
from datetime import datetime, timedelta
import os

# Local storage file
DATA_FOLDER = "data"
REMINDERS_FILE = "reminders.json"

# Load reminders from file
def load_reminders():
    if os.path.exists(REMINDERS_FILE):
        with open(REMINDERS_FILE, "r") as f:
            return json.load(f)
    return []

# Save reminders to file
def save_reminders(reminders):
    with open(REMINDERS_FILE, "w") as f:
        json.dump(reminders, f, indent=4)

# Add new reminder
def add_reminder(title, description, date, time, repeat):
    reminders = load_reminders()
    reminders.append({
        "title": title,
        "description": description,
        "datetime": f"{date} {time}",
        "repeat": repeat,
        "done": False
    })
    save_reminders(reminders)

# Filter reminders by date
def filter_reminders(reminders, filter_option):
    now = datetime.now()
    if filter_option == "Today":
        return [r for r in reminders if r['done'] is False and datetime.strptime(r['datetime'], "%Y-%m-%d %H:%M:%S").date() == now.date()]
    elif filter_option == "This Week":
        week_end = now + timedelta(days=7)
        return [r for r in reminders if r['done'] is False and now.date() <= datetime.strptime(r['datetime'], "%Y-%m-%d %H:%M:%S").date() <= week_end.date()]
    else:
        return [r for r in reminders if r['done'] is False]

# UI starts here
st.title("🛎️ Reminders")

st.subheader("➕ Add New Reminder")
with st.form("add_reminder_form"):
    title = st.text_input("Title")
    description = st.text_area("Description")
    date = st.date_input("Date")
    time = st.time_input("Time")
    repeat = st.radio("Repeat", ["None", "Daily", "Weekly"])
    submitted = st.form_submit_button("Add Reminder")
    if submitted:
        add_reminder(title, description, date, time, repeat)
        st.success("Reminder added!")

st.subheader("📋 Upcoming Reminders")
filter_option = st.selectbox("Filter", ["All", "Today", "This Week"])
reminders = load_reminders()
filtered_reminders = filter_reminders(reminders, filter_option)

if not filtered_reminders:
    st.info("No reminders found.")
else:
    for i, reminder in enumerate(filtered_reminders):
        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(f"**{reminder['title']}**")
            st.caption(f"{reminder['description']}")
            st.caption(f"🕒 {reminder['datetime']} | 🔁 {reminder['repeat']}")
        with col2:
            if st.button("✅ Done", key=f"done_{i}"):
                reminder['done'] = True
                save_reminders(reminders)
                st.rerun()

st.markdown("---")
st.caption("Reminders are stored locally in reminders.json")
