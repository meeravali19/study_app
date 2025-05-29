import streamlit as st
import json
import os
import datetime
import random
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


# --- File paths ---
DATA_FOLDER = "data"
TODAY = datetime.date.today().isoformat()

# Create folder if not exists
os.makedirs(DATA_FOLDER, exist_ok=True)

# --- Utility functions ---
def load_json(filename, default_data):
    path = os.path.join(DATA_FOLDER, filename)
    if not os.path.exists(path):
        with open(path, "w") as f:
            json.dump(default_data, f)
    with open(path, "r") as f:
        return json.load(f)

def save_json(filename, data):
    path = os.path.join(DATA_FOLDER, filename)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

# --- Load data ---
tasks = load_json("tasks.json", {})         # Format: {"2025-04-22": [{"task": "Read ML", "completed": True}]}
progress = load_json("progress.json", {})   # Format: {"Math": 60, "DSA": 40}
reminders = load_json("reminders.json", []) # Format: [{"text": "Revise OOP", "time": "18:00"}]

# --- Layout ---
st.set_page_config(page_title="📊 My Dashboard", layout="wide")
st.title("📚 Personal Preparation Dashboard")

# --- Column Layout ---
col1, col2 = st.columns(2)

# 📅 Today's Summary
with col1:
    st.subheader("✅ Today's Summary")
    today_tasks = tasks.get(TODAY, [])
    completed = sum(1 for t in today_tasks if t["completed"])
    total = len(today_tasks)
    st.metric("Tasks Completed", f"{completed}/{total}")

# 📌 Subject Progress
#
# 📊 Task Completion Graph (Last 5 Days)
def display_task_graph():
    last_5_days = [(datetime.date.today() - datetime.timedelta(days=i)).isoformat() for i in reversed(range(5))]

    dates = []
    total_tasks = []
    completed_tasks = []

    for day in last_5_days:
        task_data = tasks.get(day, [])
        dates.append(day)
        total_tasks.append(len(task_data))
        completed_tasks.append(sum(1 for t in task_data if t["completed"]))

    # Bar chart with grouped bars
    fig = go.Figure(data=[
        go.Bar(name='Total Tasks', x=dates, y=total_tasks, marker_color='lightblue'),
        go.Bar(name='Completed Tasks', x=dates, y=completed_tasks, marker_color='green')
    ])

    fig.update_layout(
        barmode='group',
        title='📊 Task Completion Overview (Last 5 Days)',
        xaxis_title='Date',
        yaxis_title='Number of Tasks',
        bargap=0.25,
        xaxis_tickformat='%Y-%m-%d',
        width=900,
        height=400
    )

    st.subheader("📊 Task Completion Overview (Last 5 Days)")
    st.plotly_chart(fig)

display_task_graph()

# 🔔 Reminders
st.subheader("⏰ Today's Reminders")
today_reminders = [r for r in reminders if r["time"]]
if today_reminders:
    for r in today_reminders:
        st.markdown(f"- 🕒 **{r['time']}**: {r['text']}")
else:
    st.info("No reminders for today.")

# 💡 Motivation
st.subheader("💬 Quote of the Day")
quotes = [
    "Push yourself, because no one else is going to do it for you.",
    "Success doesn’t just find you. You have to go out and get it.",
    "It always seems impossible until it’s done.",
    "Great things never come from comfort zones."
]
st.success(random.choice(quotes))
