import streamlit as st
import pandas as pd
import numpy as np
import time
import plotly.express as px
import plotly.graph_objects as pgo
from datetime import datetime
import connection as con  # Kepware OPC UA connection

# Set Streamlit page
st.set_page_config(page_title="Live Data Streaming from Kepware OPC UA", layout="wide")

# Set Title
st.title("Live Data Streaming from Kepware OPC UA")

# Sidebar Settings
st.sidebar.header("Settings")
record_limit = st.sidebar.slider("Number of Records to Display", 10, 100, 50)

# Initialized session state for storing data
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=["Timestamp", "Sensor1", "Sensor2", "Sensor3", "Sensor4"])

# Fetched live data
sensor1 = con.node1.get_value()  # Get latest Kepware OPC UA value
sensor2 = con.node2.get_value()
sensor3 = con.node3.get_value()
sensor4 = con.node4.get_value()

timestamp = datetime.now()

# Appended new data while keeping only the last record_limit values
new_data = pd.DataFrame([[timestamp, sensor1, sensor2, sensor3, sensor4]], columns=["Timestamp", "Sensor1", "Sensor2", "Sensor3", "Sensor4"])
st.session_state.data = pd.concat([st.session_state.data, new_data]).tail(record_limit)

# Checked if data is empty
if st.session_state.data.empty:
    st.warning("No data found, Please check your sensor connection.")
else:
# Converted Timestamp column to datetime format
    st.session_state.data["Timestamp"] = pd.to_datetime(st.session_state.data["Timestamp"])

# Plotly Line Chart
    fig1 = px.line(st.session_state.data, x="Timestamp", y="Sensor1",title="Live Sensor1 Readings", markers=True, template="plotly_dark")
    fig1.update_traces(mode="lines+markers", hoverinfo="x+y")

    fig2 = px.line(st.session_state.data, x="Timestamp", y="Sensor2", title="Live Sensor2 Readings", markers=True, template="plotly_dark")
    fig2.update_traces(mode="lines+markers", hoverinfo="x+y")

    fig3 = px.line(st.session_state.data, x="Timestamp", y="Sensor3", title="Live Sensor3 Readings", markers=True, template="plotly_dark")
    fig3.update_traces(mode="lines+markers", hoverinfo="x+y")

    fig4 = pgo.Figure()
    fig4.add_trace(pgo.Scatter(x=st.session_state.data["Timestamp"], y=st.session_state.data["Sensor4"], mode="lines+markers", name="Sensor4", line=dict(shape="spline", smoothing=1.3)))
    fig4.update_layout(title="Live Sensor4 Readings", xaxis_title="Timestamp", yaxis_title="Sensor4", template="plotly_dark")


# Displayed Plotly Chart
    # Displayed Plots in Two Rows
    col1, col2 = st.columns(2)  # Created two columns for the first row
    with col1:
        st.plotly_chart(fig1, use_container_width=True)  
    with col2:
        st.plotly_chart(fig2, use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        st.plotly_chart(fig3, use_container_width=True)
    with col4:
        st.plotly_chart(fig4, use_container_width=True) 

# Live Data Table
    st.dataframe(st.session_state.data.iloc[::-1], use_container_width=True)

# Refresh the Page
time.sleep(1)
st.rerun()
