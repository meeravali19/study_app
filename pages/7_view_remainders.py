# pages/2_View_Reminders.py
import streamlit as st
from Utility import load_data, mark_reviewed
from datetime import datetime

st.title("🔔 View Today’s Study Reminders")

data = load_data()
now = datetime.now()

today_str = now.strftime("%Y-%m-%d")  # Get today's date only (YYYY-MM-DD)

all_entries = []
for subject, entries in data.items():
    for entry in entries:
        entry["subject"] = subject
        all_entries.append(entry)

# Filter: only show if not reviewed AND reminder is today
filtered_entries = [
    entry for entry in all_entries
    if not entry.get("reviewed", False)
    and entry["next_review"].startswith(today_str)
]

# Sort by time
sorted_entries = sorted(
    filtered_entries,
    key=lambda x: datetime.strptime(x["next_review"], "%Y-%m-%d %H:%M:%S")
)

if not sorted_entries:
    st.info("🎉 No reminders for today! You're all caught up!")

for entry in sorted_entries:
    reminder_time = datetime.strptime(entry["next_review"], "%Y-%m-%d %H:%M:%S")

    st.markdown(f"### 📘 {entry['subject']} - {entry['topic']}")
    st.write(f"🕒 Last Studied: {entry['session_time']}")
    st.write(f"🔁 Repetition Count: {entry['repetition']}")
    st.write(f"📅 Next Reminder: {entry['next_review']}")
    st.write(f"📝 Notes: {entry['notes']}")
    time_left = reminder_time - now
    st.write(f"⏳ Time Left: {str(time_left).split('.')[0]}")

    if now >= reminder_time:
        st.warning("⚠️ Reminder is due!")

    if st.button("✅ Mark as Reviewed", key=entry["id"]):
        mark_reviewed(entry["id"])
        st.experimental_rerun()
