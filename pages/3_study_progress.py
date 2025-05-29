import streamlit as st
import json
import os

# --- File setup ---
DATA_FOLDER = "data"
PROGRESS_FILE = os.path.join(DATA_FOLDER, "progress.json")
os.makedirs(DATA_FOLDER, exist_ok=True)

status_options = ["Not Started", "Started", "In Progress", "Completed"]

# --- Load/Save Functions ---
def load_progress():
    if not os.path.exists(PROGRESS_FILE):
        return {}
    with open(PROGRESS_FILE, "r") as f:
        return json.load(f)

def save_progress(data):
    with open(PROGRESS_FILE, "w") as f:
        json.dump(data, f, indent=2)

def migrate_old_data(data):
    for exam in data:
        for subject in data[exam]:
            for topic in list(data[exam][subject]):
                value = data[exam][subject][topic]
                if isinstance(value, int):  # old percentage format
                    if value == 0:
                        data[exam][subject][topic] = "Not Started"
                    elif value < 40:
                        data[exam][subject][topic] = "Started"
                    elif value < 100:
                        data[exam][subject][topic] = "In Progress"
                    else:
                        data[exam][subject][topic] = "Completed"
    return data

# --- App Config ---
st.set_page_config(page_title="📚 Study Progress Tracker", layout="wide")
st.title("📚 Track Study Progress (Exam → Subject → Topic)")

progress = migrate_old_data(load_progress())
save_progress(progress)

# --- Exam Selection ---
st.subheader("🎓 Select or Add Exam")
exam_list = list(progress.keys())
selected_exam = st.selectbox("Choose Exam", ["New Exam"] + exam_list)

if selected_exam == "New Exam":
    new_exam = st.text_input("Enter New Exam Name")
    if new_exam and new_exam not in progress:
        progress[new_exam] = {}
        save_progress(progress)
        st.success(f"Created exam: **{new_exam}**")
        st.experimental_rerun()
else:
    new_exam = selected_exam

# --- Subject Selection ---
if new_exam:
    st.markdown(f"### 📘 Subjects in: **{new_exam}**")
    subject_list = list(progress[new_exam].keys())
    selected_subject = st.selectbox("Choose Subject", ["New Subject"] + subject_list)

    if selected_subject == "New Subject":
        new_subject = st.text_input("Enter New Subject Name")
        if new_subject and new_subject not in progress[new_exam]:
            progress[new_exam][new_subject] = {}
            save_progress(progress)
            st.success(f"Created subject: **{new_subject}**")
            st.experimental_rerun()
    else:
        new_subject = selected_subject

# --- Topic Status Management ---
if new_exam and new_subject:
    st.markdown(f"### 🧠 Manage Topics for: **{new_subject}** in **{new_exam}**")

    topic_list = list(progress[new_exam][new_subject].keys())
    selected_topic = st.selectbox("Select Topic to View/Edit", ["New Topic"] + topic_list)

    if selected_topic == "New Topic":
        topic_name = st.text_input("Enter New Topic Name")
        status = st.selectbox("Select Status", status_options)
        if st.button("Save New Topic") and topic_name:
            progress[new_exam][new_subject][topic_name] = status
            save_progress(progress)
            st.success(f"Added topic **{topic_name}** with status: {status}")
            st.experimental_rerun()
    else:
        # Edit existing topic
        current_status = progress[new_exam][new_subject].get(selected_topic, "Not Started")
        try:
            current_index = status_options.index(current_status)
        except ValueError:
            current_index = 0

        status = st.selectbox("Update Status", status_options, index=current_index)
        if st.button("Update Topic Status"):
            progress[new_exam][new_subject][selected_topic] = status
            save_progress(progress)
            st.success(f"Updated topic **{selected_topic}** to: {status}")
            st.experimental_rerun()

        # --- Delete Topic ---
        if st.button("❌ Delete This Topic"):
            progress[new_exam][new_subject].pop(selected_topic)
            save_progress(progress)
            st.warning(f"Deleted topic: **{selected_topic}**")
            st.experimental_rerun()

    # --- Display All Topics ---
    if progress[new_exam][new_subject]:
        st.markdown("### 📋 Topic Summary")
        for topic, stat in progress[new_exam][new_subject].items():
            st.markdown(f"- **{topic}** → {stat}")
    else:
        st.info("No topics added yet.")
