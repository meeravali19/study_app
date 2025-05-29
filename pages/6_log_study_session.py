# pages/1_Log_Study_Session.py
import streamlit as st
from Utility import log_study

st.title("📝 Log a New Study Session")

subject = st.text_input("Enter Subject")
topic = st.text_input("Enter Topic")
notes = st.text_area("Study Notes")

if st.button("Log Session"):
    if subject and topic:
        log_study(subject, topic, notes)
        st.success("✅ Session logged and reminder scheduled!")
    else:
        st.error("❌ Subject and topic are required.")
