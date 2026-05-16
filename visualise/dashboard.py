import sqlite3
import pandas as pd
import streamlit as st
import plotly.express as px
from pathlib import Path

DB_PATH = "garmin_data.db"

st.set_page_config(page_title="Garmin Dashboard", layout="wide", page_icon="🏃")
st.title("🏃 Garmin Connect Dashboard")

if not Path(DB_PATH).exists():
    st.error("No database found. Run `python -m etl.pipeline` first.")
    st.stop()

conn = sqlite3.connect(DB_PATH)

# ── Activities ───────────────────────────────────────────────
st.header("🏋️ Activities")
df_act = pd.read_sql("SELECT * FROM activities", conn, parse_dates=["start_time"])

if not df_act.empty:
    df_act["distance_km"]  = df_act["distance_meters"] / 1000
    df_act["duration_min"] = df_act["duration_secs"] / 60

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Activities", len(df_act))
    col2.metric("Total Distance (km)", f"{df_act['distance_km'].sum():.1f}")
    col3.metric("Avg Heart Rate", f"{df_act['avg_hr'].mean():.0f} bpm")

    fig = px.bar(
        df_act.sort_values("start_time"),
        x="start_time", y="distance_km",
        color="activity_type", title="Distance per Activity"
    )
    st.plotly_chart(fig, use_container_width=True)

    fig2 = px.scatter(
        df_act, x="duration_min", y="avg_hr",
        color="activity_type", size="distance_km",
        title="Duration vs Avg Heart Rate", hover_data=["name"]
    )
    st.plotly_chart(fig2, use_container_width=True)

# ── Steps ────────────────────────────────────────────────────
st.header("👣 Daily Steps")
df_steps = pd.read_sql("SELECT * FROM daily_steps ORDER BY date", conn)

if not df_steps.empty:
    col1, col2 = st.columns(2)
    col1.metric("Avg Daily Steps", f"{df_steps['total_steps'].mean():,.0f}")
    col2.metric("Days Above Goal", int((df_steps["total_steps"] >= df_steps["goal"]).sum()))

    fig3 = px.bar(df_steps, x="date", y="total_steps", title="Daily Step Count")
    fig3.add_hline(y=df_steps["goal"].mean(), line_dash="dash",
                   annotation_text="Goal", line_color="red")
    st.plotly_chart(fig3, use_container_width=True)

# ── Sleep ────────────────────────────────────────────────────
st.header("😴 Sleep")
df_sleep = pd.read_sql("SELECT * FROM sleep ORDER BY date", conn)

if not df_sleep.empty:
    df_sleep["sleep_hours"] = df_sleep["sleep_seconds"] / 3600
    col1, col2 = st.columns(2)
    col1.metric("Avg Sleep (hrs)", f"{df_sleep['sleep_hours'].mean():.1f}")
    col2.metric("Avg Sleep Score", f"{df_sleep['score'].mean():.0f}")

    fig4 = px.area(df_sleep, x="date", y="sleep_hours", title="Nightly Sleep Duration")
    st.plotly_chart(fig4, use_container_width=True)

    df_stages = df_sleep[["date","deep_seconds","light_seconds","rem_seconds","awake_seconds"]].copy()
    for col in ["deep_seconds","light_seconds","rem_seconds","awake_seconds"]:
        df_stages[col] = df_stages[col] / 60
    df_melt = df_stages.melt(id_vars="date", var_name="Stage", value_name="Minutes")
    fig5 = px.bar(df_melt, x="date", y="Minutes", color="Stage",
                  title="Sleep Stages per Night", barmode="stack")
    st.plotly_chart(fig5, use_container_width=True)

conn.close()