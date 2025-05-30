from datetime import datetime, timedelta
import json
import os

DB_FILE = "study_data.json"

def load_data():
    if not os.path.exists(DB_FILE):
        return {}
    with open(DB_FILE, "r") as file:
        return json.load(file)

def save_data(data):
    with open(DB_FILE, "w") as file:
        json.dump(data, file, indent=4)

def calculate_next_review_date(start_date, repetition):
    if repetition == 1:
        return start_date.replace(hour=21, minute=0, second=0)  # same night at 9 PM
    elif repetition == 2:
        return start_date + timedelta(days=1)
    elif repetition == 3:
        return start_date + timedelta(days=7)
    elif repetition == 4:
        return start_date + timedelta(days=31)
    elif repetition == 5:
        return start_date + timedelta(days=90)
    else:
        return start_date + timedelta(days=90)

def log_study(subject):
    data = load_data()
    now = datetime.now()

    if subject not in data:
        data[subject] = []

    repetition = len(data[subject]) + 1
    next_review = calculate_next_review_date(now, repetition)

    data[subject].append({
        "session_time": now.strftime("%Y-%m-%d %H:%M:%S"),
        "repetition": repetition,
        "next_review": next_review.strftime("%Y-%m-%d %H:%M:%S")
    })

    save_data(data)
    return f"Logged {subject} | Repetition {repetition} | Next review: {next_review.strftime('%Y-%m-%d %H:%M:%S')}"

def mark_reviewed(entry_id):
    data = load_data()
    for entry in data:
        if entry["id"] == entry_id:
            entry["reviewed"] = True
    save_data(data)