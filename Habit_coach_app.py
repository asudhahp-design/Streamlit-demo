import streamlit as st
import datetime
import pandas as pd
import random

st.set_page_config(page_title="AI Habit Coach", layout="centered")

st.title("🌟 AI-Powered Habit Coach With Weekly/Monthly Analytics")

# ---- Session State ----
if "logs" not in st.session_state:
    st.session_state.logs = []

# ---- Habit Input ----
habit = st.selectbox(
    "Choose a habit to track:",
    ["Sleep (hours)", "Exercise (minutes)", "Study (hours)", "Water Intake (liters)"]
)

value = st.number_input("Enter today's value:", min_value=0.0)
date = st.date_input("Date:", datetime.date.today())

# ---- Add Entry ----
if st.button("Add Entry"):
    st.session_state.logs.append({"habit": habit, "value": value, "date": date})
    st.success("✅ Entry added successfully!")

# ---- Show Logs ----
st.subheader("📅 Your Habit Logs")

if st.session_state.logs:
    df = pd.DataFrame(st.session_state.logs)
    df = df.sort_values("date")

    st.dataframe(df)

    # ✅ THIN ADD-ON: Trend Chart
    st.subheader("📈 Habit Progress Trend")
    chart_data = df.groupby("date")["value"].sum()
    st.line_chart(chart_data)

    # ---------------------------------------------------------
    # ✅ WEEKLY & MONTHLY ANALYTICS (NEW ADD-ON)
    # ---------------------------------------------------------
    st.subheader("📊 Analytics Summary")

    # Convert date column to datetime
    df["date"] = pd.to_datetime(df["date"])

    # Add week number & month name
    df["week"] = df["date"].dt.isocalendar().week
    df["month"] = df["date"].dt.strftime("%B")

    # ✅ Weekly Analytics
    st.write("### 📆 Weekly Summary")
    weekly_summary = df.groupby("week")["value"].sum().reset_index()
    st.bar_chart(weekly_summary.set_index("week"))

    # ✅ Monthly Analytics
    st.write("### 🗓 Monthly Summary")
    monthly_summary = df.groupby("month")["value"].sum().reset_index()
    st.bar_chart(monthly_summary.set_index("month"))

    # Show tables
    with st.expander("View Weekly Data Table"):
        st.dataframe(weekly_summary)

    with st.expander("View Monthly Data Table"):
        st.dataframe(monthly_summary)

else:
    st.info("No logs yet. Add your first entry above!")

# ---- Simple AI-Like Advice ----
if st.button("Get AI Advice"):
    advice_list = [
        "Try setting small, daily goals. Consistency beats intensity.",
        "You're doing great! Keep showing up daily.",
        "Visualize your goal and track progress regularly.",
        "Reward yourself for completing habit streaks!",
        "Stay hydrated, well-rested, and maintain balance."
    ]
    st.subheader("💡 Coach Advice")
    st.write(random.choice(advice_list))