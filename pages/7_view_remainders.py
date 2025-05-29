# pages/2_View_Reminders.py
import streamlit as st
from Utility import load_data, mark_reviewed
from datetime import datetime, timedelta

st.title("🔔 View Upcoming Study Reminders")

data = load_data()
now = datetime.now()
sorted_data = sorted(data, key=lambda x: x["next_reminder"])

for entry in sorted_data:
    reminder_time = datetime.strptime(entry["next_reminder"], "%Y-%m-%d %H:%M:%S")

    if not entry["reviewed"]:
        st.markdown(f"### 📘 {entry['subject']} - {entry['topic']}")
        st.write(f"🕒 Last Studied: {entry['last_studied']}")
        st.write(f"🔁 Repetition Count: {entry['repetition_count']}")
        st.write(f"📅 Next Reminder: {entry['next_reminder']}")
        st.write(f"📝 Notes: {entry['notes']}")
        time_left = reminder_time - now
        st.write(f"⏳ Time Left: {str(time_left).split('.')[0]}")

        if now >= reminder_time:
            st.warning("⚠️ Reminder is due!")

        if st.button("✅ Mark as Reviewed", key=entry["id"]):
            mark_reviewed(entry["id"])
            st.experimental_rerun()
