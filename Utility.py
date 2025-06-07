# Utility.py
from datetime import datetime, timedelta
import json
import os
import uuid

DB_FILE = "study_db.json"

def load_data():
    if not os.path.exists(DB_FILE):
        return {}
    with open(DB_FILE, "r") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return {}

def save_data(data):
    with open(DB_FILE, "w") as file:
        json.dump(data, file, indent=4)

def calculate_next_review_date(start_date, repetition):
    if repetition == 1:
        return start_date.replace(hour=21, minute=0, second=0, microsecond=0)
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

def get_repetition_for_topic(data, subject, topic):
    if subject not in data:
        return 1
    return sum(1 for entry in data[subject] if entry["topic"] == topic) + 1

def log_study(subject, topic, notes):
    data = load_data()
    now = datetime.now()

    if subject not in data:
        data[subject] = []

    repetition = get_repetition_for_topic(data, subject, topic)
    next_review = calculate_next_review_date(now, repetition)

    entry = {
        "id": str(uuid.uuid4()),
        "topic": topic,
        "notes": notes,
        "session_time": now.strftime("%Y-%m-%d %H:%M:%S"),
        "repetition": repetition,
        "next_review": next_review.strftime("%Y-%m-%d %H:%M:%S"),
        "reviewed": False
    }

    data[subject].append(entry)
    save_data(data)
    return f"Logged {subject} - {topic} | Repetition {repetition} | Next review: {entry['next_review']}"

def mark_reviewed(entry_id):
    data = load_data()
    updated = False
    now = datetime.now()

    for subject in data:
        for entry in data[subject]:
            if entry.get("id") == entry_id and not entry.get("reviewed", False):
                # 1. Mark as reviewed temporarily (optional since we'll re-use the same entry)
                entry["reviewed"] = False  # Reset reviewed to False for next cycle

                # 2. Increment repetition count
                current_repetition = entry.get("repetition", 1)
                new_repetition = current_repetition + 1
                entry["repetition"] = new_repetition

                # 3. Update session time
                entry["session_time"] = now.strftime("%Y-%m-%d %H:%M:%S")

                # 4. Recalculate next review date
                new_next_review = calculate_next_review_date(now, new_repetition)
                entry["next_review"] = new_next_review.strftime("%Y-%m-%d %H:%M:%S")

                # 5. Mark it still as not reviewed (because this is the new repetition entry)
                entry["reviewed"] = False

                updated = True
                break

    if updated:
        save_data(data)
        return True
    return False
