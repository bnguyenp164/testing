import streamlit as st
import pandas as pd
import time
from datetime import datetime
import random

# Simulated in-memory data
data = []

st.title("🌡️ IoT Dashboard - Temp & Humidity")

# Line chart placeholder
chart = st.line_chart()

# Every second, update data
for _ in range(3600):  # 1 hour loop
    now = datetime.now().strftime("%H:%M:%S")
    temp = random.uniform(30, 70)     # Simulated GPU temp - 20
    humid = random.uniform(40, 80)    # Simulated GPU temp

    data.append({"time": now, "temperature": temp, "humidity": humid})

    # Limit to 1 hour (3600 seconds)
    if len(data) > 3600:
        data = data[-3600:]

    df = pd.DataFrame(data)
    df.set_index("time", inplace=True)

    chart.line_chart(df)

    time.sleep(1)
