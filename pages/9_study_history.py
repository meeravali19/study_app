# pages/3_Study_History.py
import streamlit as st
from Utility import load_data
from datetime import datetime
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import calplot

st.title("📚 Study History Timeline + Calendar")

data = load_data()

history_entries = []

# Flatten reviewed entries into a list
for subject, entries in data.items():
    for entry in entries:
        if entry.get("repetition", 0) > 1:
            history_entries.append({
                "Subject": subject,
                "Topic": entry["topic"],
                "Repetition": entry["repetition"],
                "Last Studied": entry["session_time"],
                "Next Review": entry["next_review"],
                "Notes": entry["notes"]
            })

if not history_entries:
    st.info("No reviewed history yet. Start studying and marking topics as reviewed!")
else:
    # Convert to DataFrame
    df = pd.DataFrame(history_entries)
    df["Last Studied"] = pd.to_datetime(df["Last Studied"])
    df["Next Review"] = pd.to_datetime(df["Next Review"])
    df.sort_values("Last Studied", ascending=False, inplace=True)

    st.subheader("📋 Study History Table")
    st.dataframe(df, use_container_width=True)

    st.subheader("📈 Study Timeline Chart")
    chart = px.scatter(
        df,
        x="Last Studied",
        y="Subject",
        color="Repetition",
        hover_data=["Topic", "Notes"],
        title="Study Activity Over Time",
        height=500
    )
    st.plotly_chart(chart, use_container_width=True)

   # 📅 Calendar Heatmap
st.subheader("📅 Calendar Heatmap (GitHub-style)")
df['date_only'] = pd.to_datetime(df['Last Studied'].dt.date)  # convert date_only to datetime

heatmap_data = df.groupby('date_only').size()
heatmap_data.index = pd.to_datetime(heatmap_data.index)  # convert index to DatetimeIndex

fig, ax = calplot.calplot(
    heatmap_data,
    cmap='YlGn',
    colorbar=True,
    suptitle='Your Study Streak 📅',
    edgecolor='white',
    linewidth=1,
    figsize=(10, 3)
)
st.pyplot(fig)
