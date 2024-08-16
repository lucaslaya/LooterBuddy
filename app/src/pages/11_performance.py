import logging
import pandas as pd
import streamlit as st
from streamlit_extras.app_logo import add_logo
import plotly.express as px
from modules.nav import SideBarLinks
import requests

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

logger = logging.getLogger(__name__)

API_URL = "http://api:4000"

# Fetch the list of missions for the dropdown
def get_missions():
    response = requests.get(f"{API_URL}/d/missions")
    if response.status_code == 200:
        missions = response.json()
        return [(mission['missionID'], mission['name']) for mission in missions]
    else:
        st.error("Failed to load missions.")
        return []

# Fetch performance data (all or by mission)
def get_performance_data(mission_id=None):
    if mission_id:
        response = requests.get(f"{API_URL}/d/performance/mission/{mission_id}")
    else:
        response = requests.get(f"{API_URL}/d/performance")
    
    if response.status_code == 200:
        return pd.DataFrame(response.json())
    else:
        st.error("Failed to load performance data.")
        return pd.DataFrame()

# Perform basic analysis on the performance data
def analyze_performance(df):
    analysis = {
        'Average Kills': df['totalKills'].mean(),
        'Average Deaths': df['totalDeaths'].mean(),
        'Average DPS': df['DPS'].mean(),
        'Total Performances': len(df)
    }
    return analysis

# Main Streamlit page setup
st.title("Performance Data Overview")

# Dropdown to select a mission
missions = get_missions()
mission_options = ["All"] + [mission[1] for mission in missions]
selected_mission = st.selectbox("Select a Mission", mission_options)

# Fetch and display performance data based on the selected mission
if selected_mission == "All":
    performance_data = get_performance_data()
else:
    mission_id = next((mission[0] for mission in missions if mission[1] == selected_mission), None)
    performance_data = get_performance_data(mission_id)

# Display the performance data in a table
st.subheader("Performance Data")
st.dataframe(performance_data)

# Perform and display standard analysis
if not performance_data.empty:
    st.subheader("Performance Analysis")
    analysis = analyze_performance(performance_data)
    st.write(analysis)
