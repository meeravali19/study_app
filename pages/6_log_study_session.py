# pages/1_Log_Study_Session.py
import streamlit as st
from Utility import log_study

st.title("📝 Log a New Study Session")

subject = st.text_input("Enter Subject").strip().title()
topic = st.text_input("Enter Topic").strip().title()
notes = st.text_area("Study Notes")

if st.button("Log Session"):
    if subject and topic:
        result = log_study(subject, topic, notes)
        st.success(f"✅ {result}")
    else:
        st.error("❌ Subject and topic are required.")