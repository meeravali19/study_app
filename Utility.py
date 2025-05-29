from datetime import datetime, timedelta
import uuid
import json
import os

DB_FILE = "study_db.json"

def load_data():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as file:
            return json.load(file)
    return []

def save_data(data):
    with open(DB_FILE, "w") as file:
        json.dump(data, file, indent=4)

def get_next_interval(repetition_count):
    return timedelta(days=7 * repetition_count)

def log_study(subject, topic, notes):
    data = load_data()
    now = datetime.now()

    for entry in data:
        if entry["subject"].lower() == subject.lower() and entry["topic"].lower() == topic.lower():
            entry["repetition_count"] += 1
            entry["last_studied"] = now.strftime("%Y-%m-%d %H:%M:%S")
            interval = get_next_interval(entry["repetition_count"])
            entry["next_reminder"] = (now + interval).strftime("%Y-%m-%d %H:%M:%S")
            entry["notes"] = notes
            entry["reviewed"] = False
            break
    else:
        repetition_count = 1
        next_time = now + get_next_interval(repetition_count)
        data.append({
            "id": str(uuid.uuid4()),
            "subject": subject,
            "topic": topic,
            "notes": notes,
            "last_studied": now.strftime("%Y-%m-%d %H:%M:%S"),
            "repetition_count": repetition_count,
            "next_reminder": next_time.strftime("%Y-%m-%d %H:%M:%S"),
            "reviewed": False
        })

    save_data(data)

def mark_reviewed(entry_id):
    data = load_data()
    for entry in data:
        if entry["id"] == entry_id:
            entry["reviewed"] = True
    save_data(data)
