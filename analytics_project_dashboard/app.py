import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import plotly.express as px

st.set_page_config(
    page_title="Analytics Project Monitoring System",
    page_icon="📊",
    layout="wide"
)

st.markdown("""
# 📊 Analytics Project Lifecycle Monitoring System
### Real-Time Project Tracking | Risk Monitoring | Status Reporting
---
""")

data = pd.read_csv("project_data.csv")

data["Start_Date"] = pd.to_datetime(data["Start_Date"])
data["End_Date"] = pd.to_datetime(data["End_Date"])

today = pd.to_datetime(datetime.today().date())

st.sidebar.header("🔍 Filter Projects")

team_filter = st.sidebar.selectbox(
    "Select Team",
    ["All"] + list(data["Team"].unique())
)

status_filter = st.sidebar.selectbox(
    "Select Status",
    ["All"] + list(data["Status"].unique())
)

filtered_data = data.copy()

if team_filter != "All":
    filtered_data = filtered_data[filtered_data["Team"] == team_filter]

if status_filter != "All":
    filtered_data = filtered_data[filtered_data["Status"] == status_filter]


filtered_data["Overdue"] = filtered_data["End_Date"] < today

def calculate_health(row):
    if row["Completion_Percentage"] == 100:
        return "🟢 Healthy"
    elif row["Overdue"] == True or row["Risk_Level"] == "High":
        return "🔴 Critical"
    elif row["Completion_Percentage"] < 50 and row["Risk_Level"] == "Medium":
        return "🟡 Warning"
    else:
        return "🟢 Stable"

filtered_data["Health_Status"] = filtered_data.apply(calculate_health, axis=1)

st.markdown("## 📋 Project Overview")
st.dataframe(filtered_data, use_container_width=True)
st.markdown("---")

total_projects = len(filtered_data)
completed_projects = len(filtered_data[filtered_data["Status"] == "Completed"])
delayed_projects = len(filtered_data[filtered_data["Status"] == "Delayed"])
high_risk_projects = len(filtered_data[filtered_data["Risk_Level"] == "High"])

st.markdown("## 📌 Project Performance Metrics")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Projects", total_projects)
col2.metric("Completed", completed_projects)
col3.metric("Delayed", delayed_projects)
col4.metric("High Risk", high_risk_projects)

st.markdown("---")


st.markdown("## ⚠ Overdue Projects")

overdue_projects = filtered_data[filtered_data["Overdue"] == True]

if len(overdue_projects) > 0:
    st.dataframe(overdue_projects, use_container_width=True)
else:
    st.success("No overdue projects 🎉")

st.markdown("---")

st.markdown("## 📈 Completion Progress Overview")

fig, ax = plt.subplots(figsize=(10, 4))
ax.bar(filtered_data["Project_Name"],
       filtered_data["Completion_Percentage"])

ax.set_ylabel("Completion %")
ax.set_ylim(0, 100)
plt.xticks(rotation=45)

st.pyplot(fig)

st.markdown("---")

st.markdown("## 🗓 Project Timeline (Gantt View)")

gantt_chart = px.timeline(
    filtered_data,
    x_start="Start_Date",
    x_end="End_Date",
    y="Project_Name",
    color="Health_Status",
)

gantt_chart.update_yaxes(autorange="reversed")

st.plotly_chart(gantt_chart, use_container_width=True)

st.markdown("---")

st.markdown("## 📝 Weekly Management Summary")

on_track = len(filtered_data[filtered_data["Status"] == "On Track"])
at_risk = len(filtered_data[filtered_data["Status"] == "At Risk"])

summary = f"""
Total Active Projects: {total_projects}

Projects On Track: {on_track}
Projects Completed: {completed_projects}
Projects Delayed: {delayed_projects}
Projects At Risk: {at_risk}

High Risk Projects: {high_risk_projects}
Overdue Projects: {len(overdue_projects)}
"""

st.info(summary)

st.markdown("---")

st.markdown("## 🏥 Project Health Overview")

st.dataframe(
    filtered_data[[
        "Project_Name",
        "Completion_Percentage",
        "Risk_Level",
        "Overdue",
        "Health_Status"
    ]],
    use_container_width=True

)
