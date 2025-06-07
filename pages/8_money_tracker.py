import streamlit as st
import json
import os
from datetime import datetime
import pandas as pd
import plotly.express as px

DATA_FILE = "data/data.json"

# Load or create data
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def add_expense(data, date, category, amount, note):
    month = date[:7]  # YYYY-MM
    if month not in data:
        data[month] = []
    data[month].append({
        "date": date,
        "category": category,
        "amount": amount,
        "note": note
    })
    return data

# UI starts
st.title("📊 Monthly Expenditure Tracker")

data = load_data()
today = datetime.today().strftime('%Y-%m-%d')
current_month = today[:7]

st.header("➕ Add Expense")
with st.form("expense_form"):
    date = st.date_input("Date", datetime.today()).strftime('%Y-%m-%d')
    category = st.selectbox("Category", ["Food", "Transport", "Rent", "Utilities", "Entertainment", "Study" ,"Exam fees","Other"])
    amount = st.number_input("Amount", min_value=0.0, format="%.2f")
    note = st.text_input("Note (optional)")
    submitted = st.form_submit_button("Add")

if submitted:
    data = add_expense(data, date, category, amount, note)
    save_data(data)
    st.success("Expense added!")

# Show Summary
if current_month in data:
    df = pd.DataFrame(data[current_month])
    df['amount'] = df['amount'].astype(float)
    st.header(f"📅 Summary for {current_month}")
    st.dataframe(df)

    total = df['amount'].sum()
    st.metric("Total Spent", f"₹{total:.2f}")

    category_summary = df.groupby("category")["amount"].sum().reset_index()
    fig = px.pie(category_summary, names='category', values='amount', title='Category-wise Spending')
    st.plotly_chart(fig)

# Reset button
# --- Yearly Summary ---
st.header("📆 Yearly Summary")

years_available = sorted(set(k[:4] for k in data.keys()))
selected_year = st.selectbox("Select Year", years_available)

# Filter data for selected year
yearly_records = []
for month, records in data.items():
    if month.startswith(selected_year):
        yearly_records.extend(records)

if yearly_records:
    df_year = pd.DataFrame(yearly_records)
    df_year['amount'] = df_year['amount'].astype(float)

    st.subheader(f"💰 Total Expenditure in {selected_year}")
    total_year = df_year['amount'].sum()
    st.metric("Total Spent", f"₹{total_year:.2f}")

    # Category-wise summaries
    category_summary_year = df_year.groupby("category")["amount"].sum().reset_index()

    bar_chart = px.bar(category_summary_year, x='category', y='amount',
                       title='Category-wise Spending (Bar)', color='category')
    st.plotly_chart(bar_chart)

    pie_chart = px.pie(category_summary_year, names='category', values='amount',
                       title='Category-wise Spending (Pie)')
    st.plotly_chart(pie_chart)

    # ✅ Monthly Expense Pie Chart for the Year
    st.subheader(f"🧾 Spending Distribution by Month in {selected_year}")
    df_year['month'] = pd.to_datetime(df_year['date']).dt.strftime('%B')

    month_summary = df_year.groupby("month")["amount"].sum().reset_index()
    # Ensure months are in calendar order
    month_order = ['January', 'February', 'March', 'April', 'May', 'June',
                   'July', 'August', 'September', 'October', 'November', 'December']
    month_summary['month'] = pd.Categorical(month_summary['month'], categories=month_order, ordered=True)
    month_summary = month_summary.sort_values("month")

    pie_month_chart = px.pie(month_summary, names='month', values='amount',
                             title=f"📆 Month-wise Spending in {selected_year}")
    st.plotly_chart(pie_month_chart)

    # Detailed data view
    with st.expander("🔍 Show Detailed Data"):
        st.dataframe(df_year)
else:
    st.warning(f"No data found for year {selected_year}")
