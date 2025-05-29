import streamlit as st
import json
import os
import datetime
from datetime import datetime as dt

# --- File setup ---
DATA_FOLDER = "data"
TODAY = datetime.date.today().isoformat()
DAY_NAME = dt.now().strftime("%A")  # e.g., 'Monday'
TASK_FILE = os.path.join(DATA_FOLDER, "tasks.json")
TIMETABLE_FILE = os.path.join(DATA_FOLDER, "timetable.json")
os.makedirs(DATA_FOLDER, exist_ok=True)

# --- Load or Initialize Tasks ---
def load_tasks():
    if not os.path.exists(TASK_FILE):
        return {}
    with open(TASK_FILE, "r") as f:
        return json.load(f)

def save_tasks(tasks):
    with open(TASK_FILE, "w") as f:
        json.dump(tasks, f, indent=2)

# --- Sync timetable to today ---
def sync_from_timetable(today_tasks):
    if not os.path.exists(TIMETABLE_FILE):
        return today_tasks

    with open(TIMETABLE_FILE, "r") as f:
        timetable = json.load(f)

    if DAY_NAME not in timetable:
        return today_tasks

    entries = timetable[DAY_NAME]
    timetable_tasks = [task.strip() for task in entries.values() if task.strip()]

    # Avoid duplicates
    existing_tasks = {task["task"] for task in today_tasks}
    for task in timetable_tasks:
        if task not in existing_tasks:
            today_tasks.append({"task": task, "completed": False})

    return today_tasks

# --- App Layout ---
st.set_page_config(page_title="📝 Daily Tracker", layout="centered")
st.title("📝 Daily Learning Tracker")

tasks = load_tasks()
today_tasks = tasks.get(TODAY, [])

# 🔄 Sync from timetable (non-destructive)
today_tasks = sync_from_timetable(today_tasks)
tasks[TODAY] = today_tasks
save_tasks(tasks)

# --- Add New Task ---
st.subheader("➕ Add New Task")
new_task = st.text_input("What do you want to work on today?")
if st.button("Add Task") and new_task:
    today_tasks.append({"task": new_task, "completed": False})
    tasks[TODAY] = today_tasks
    save_tasks(tasks)
    st.experimental_rerun()

# --- Show Today's Tasks ---
st.subheader("📋 Today's Task List")
if today_tasks:
    for i, task in enumerate(today_tasks):
        col1, col2 = st.columns([0.8, 0.2])
        with col1:
            if task["completed"]:
                st.markdown(f"✅ ~~{task['task']}~~")
            else:
                st.markdown(f"🔲 {task['task']}")
        with col2:
            toggle = st.checkbox("Done", value=task["completed"], key=f"task_{i}")
            if toggle != task["completed"]:
                today_tasks[i]["completed"] = toggle
                tasks[TODAY] = today_tasks
                save_tasks(tasks)
                st.experimental_rerun()
else:
    st.info("No tasks added yet for today.")
