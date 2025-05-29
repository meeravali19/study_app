import streamlit as st
import json
import os

# --- File setup ---
DATA_FOLDER = "data"
MOCKTESTS_FILE = os.path.join(DATA_FOLDER, "mocktests.json")
PROGRESS_FILE = os.path.join(DATA_FOLDER, "progress.json")
os.makedirs(DATA_FOLDER, exist_ok=True)

# --- Load/Save Functions ---
def load_mocktests():
    if not os.path.exists(MOCKTESTS_FILE):
        return {}
    with open(MOCKTESTS_FILE, "r") as f:
        return json.load(f)

def load_progress():
    if not os.path.exists(PROGRESS_FILE):
        return {}
    with open(PROGRESS_FILE, "r") as f:
        return json.load(f)

def save_mocktests(data):
    with open(MOCKTESTS_FILE, "w") as f:
        json.dump(data, f, indent=2)

def save_progress(data):
    with open(PROGRESS_FILE, "w") as f:
        json.dump(data, f, indent=2)

# Load the current progress
progress = load_progress()
mocktests = load_mocktests()

# --- Page Config ---
st.set_page_config(page_title="📚 Mock Test Tracker", layout="wide")
st.title("📚 Track Mock Tests by Exam")

# --- Dropdown for Selecting an Exam ---
exam_list = list(progress.keys())
selected_exam = st.selectbox("Choose an Exam", ["Select exam"] + exam_list)

new_exam = selected_exam

# --- Left/Right Layout (Upcoming/Completed) ---
col1, col2 = st.columns(2)

# --- Left Box: Upcoming Mock Tests ---
with col1:
    st.markdown("### ⏳ **Upcoming Mock Tests**")
    
    if new_exam != "Select exam":
        upcoming_exams = mocktests.get(new_exam, {}).get("Upcoming", [])
        for mock_test in upcoming_exams:
            st.write(f"Test Name: **{mock_test['name']}** - Status: {mock_test['status']}")

        with st.form("add_upcoming_test", clear_on_submit=True):
            test_name = st.text_input("Test Name")
            status = st.selectbox("Status", ["Not Started", "Started", "In Progress", "Completed"])
            submit_upcoming = st.form_submit_button("Add Upcoming Test")

            if submit_upcoming and test_name:
                mock_test = {"name": test_name, "status": status}
                if new_exam not in mocktests:
                    mocktests[new_exam] = {"Upcoming": [], "Attempted": []}
                mocktests[new_exam]["Upcoming"].append(mock_test)
                save_mocktests(mocktests)
                st.success(f"Added new upcoming test: **{test_name}**")
                st.experimental_rerun()

        if upcoming_exams:
            with st.form("update_status_form", clear_on_submit=True):
                selected_test_name = st.selectbox("Select Test to Update Status", [test['name'] for test in upcoming_exams])
                new_status = st.selectbox("Update Status", ["Not Attempted", "Attempted"])
                submit_button = st.form_submit_button("Update Status")
                
                if submit_button and selected_test_name:
                    for test in upcoming_exams:
                        if test["name"] == selected_test_name:
                            test["status"] = new_status
                            if new_status == "Attempted":
                                if "Attempted" not in mocktests[new_exam]:
                                    mocktests[new_exam]["Attempted"] = []
                                mocktests[new_exam]["Attempted"].append(test)
                                mocktests[new_exam]["Upcoming"].remove(test)
                            save_mocktests(mocktests)
                            st.success(f"Test status for **{selected_test_name}** updated to {new_status}.")
                            st.experimental_rerun()

# --- Right Box: Completed Mock Tests ---
with col2:
    st.markdown("### ✅ **Completed Mock Tests**")
    
    if new_exam != "Select exam":
        completed_exams = mocktests.get(new_exam, {}).get("Attempted", [])
        if completed_exams:
            for mock_test in completed_exams:
                st.write(f"Test Name: **{mock_test['name']}** - Score: {mock_test.get('score', 'N/A')} - Status: {mock_test['status']}")

            for mock_test in completed_exams:
                if mock_test.get("score", 0) == 0:
                    st.markdown(f"#### Enter Details for **{mock_test['name']}**")

                    # Step 1: Get number of sections outside the form
                    section_key = f"num_sections_{mock_test['name']}"
                    num_sections = st.number_input("Number of Sections", min_value=1, max_value=10, value=1, step=1, key=section_key)

                    # Step 2: Score input form
                    with st.form(f"update_score_form_{mock_test['name']}", clear_on_submit=True):
                        score = st.number_input("Enter Total Score", min_value=0, max_value=100, value=0, step=1, key=f"score_input_{mock_test['name']}")

                        sections = {}
                        for i in range(1, num_sections + 1):
                            section_name = st.text_input(f"Section {i} Name", key=f"section_name_{mock_test['name']}_{i}")
                            section_score = st.number_input(f"Marks for {section_name}", min_value=0, max_value=100, value=0, step=1, key=f"section_score_{mock_test['name']}_{i}")
                            sections[section_name] = section_score

                        submit_score = st.form_submit_button("Save Details")
                        if submit_score:
                            mock_test["score"] = score
                            mock_test["sections"] = sections
                            save_mocktests(mocktests)
                            st.success(f"Details for **{mock_test['name']}** saved successfully!")
                            st.experimental_rerun()
        else:
            st.write("No completed tests yet.")
