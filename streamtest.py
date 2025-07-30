import streamlit as st
import time
import pandas as pd
import matplotlib.pyplot as plt
import random
import threading
import GPUtil

# Streamlit page configuration
st.set_page_config(page_title="IoT Dashboard", layout="wide")
st.title("🌡️ IoT Environment Monitoring Dashboard (Simulated)")

# Initialize session state variables
if 'recording' not in st.session_state:
    st.session_state.recording = False
if 'data' not in st.session_state:
    st.session_state.data = []

# Simulated sensor reading function (uses GPU temp or fallback)
def read_env_sensor():
    gpus = GPUtil.getGPUs()
    temp = gpus[0].temperature if gpus else random.uniform(40, 60)
    humidity = temp + 20  # Simulate humidity based on temp
    return temp, humidity

# Background recording function (runs in a thread)
def record_data():
    while st.session_state.recording:
        temp, humidity = read_env_sensor()
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        st.session_state.data.append({
            'Timestamp': timestamp,
            'Temperature (°C)': temp,
            'Humidity (%)': humidity
        })
        time.sleep(10)  # 10-second interval

# Start / Stop recording controls
col1, col2 = st.columns(2)
with col1:
    if st.button("▶️ Start Recording", use_container_width=True):
        if not st.session_state.recording:
            st.session_state.recording = True
            threading.Thread(target=record_data, daemon=True).start()

with col2:
    if st.button("⏹️ Stop Recording", use_container_width=True):
        st.session_state.recording = False

# Display recorded data and plot
if st.session_state.data:
    df = pd.DataFrame(st.session_state.data)

    st.subheader("📋 Last 10 Records")
    st.dataframe(df.tail(10), use_container_width=True)

    st.subheader("📈 Real-Time Temperature & Humidity Graph")
    fig, ax = plt.subplots()
    ax.plot(df['Timestamp'], df['Temperature (°C)'], label="Temperature (°C)", marker='o')
    ax.plot(df['Timestamp'], df['Humidity (%)'], label="Humidity (%)", marker='x')
    ax.set_xlabel("Time")
    ax.set_ylabel("Values")
    ax.tick_params(axis='x', labelrotation=45)
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)
