import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import time
from datetime import datetime, timedelta

st.set_page_config(layout="wide", page_title="Sensor Dashboard")

st.title("📊 Sensor Data Dashboard")

# Initialize session state
if "data" not in st.session_state:
    st.session_state.data = []
    st.session_state.running = True
    st.session_state.start_time = datetime.now()

# Start/Stop buttons
col1, col2 = st.columns(2)
with col1:
    if st.button("🟢 Start"):
        st.session_state.running = True
with col2:
    if st.button("🔴 Stop"):
        st.session_state.running = False

# Generate fake data
def simulate_data():
    now = datetime.now()
    elapsed = (now - st.session_state.start_time).total_seconds()
    temp = np.random.randint(30, 60)
    humid = temp - 20
    return {
        "timestamp": now.strftime("%H:%M:%S"),
        "elapsed": elapsed,
        "temperature": temp,
        "humidity": humid
    }

# Update data every second
if st.session_state.running:
    new_data = simulate_data()
    st.session_state.data.append(new_data)
    time.sleep(1)  # Only delays rendering, not recommended for long-term but okay for demo

# Convert to DataFrame
df = pd.DataFrame(st.session_state.data)

# Draw plots
col1, col2 = st.columns(2)

if not df.empty:
    for col, metric, color in [(col1, "temperature", "red"), (col2, "humidity", "blue")]:
        fig, ax = plt.subplots(figsize=(6, 3))
        ax.plot(df["elapsed"], df[metric], color=color, linewidth=2)
        ax.fill_between(df["elapsed"], df[metric], alpha=0.3, color=color)
        ax.set_ylim(0, 100)
        ax.set_xlim(0, 3600)

        # X-ticks every 10 mins (600s)
        ticks = np.arange(0, 3601, 600)
        labels = [(st.session_state.start_time + timedelta(seconds=int(t))).strftime("%H:%M") for t in ticks]
        ax.set_xticks(ticks)
        ax.set_xticklabels(labels, rotation=45)
        ax.set_title(f"{metric.capitalize()} Chart")
        ax.set_ylabel(f"{'°C' if metric == 'temperature' else '%'}")
        col.pyplot(fig)

# Show Data Table
st.subheader("📋 Recorded Sensor Data")
st.dataframe(df[["timestamp", "temperature", "humidity"]].iloc[::-1], use_container_width=True)
