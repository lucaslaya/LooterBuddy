import logging
import pandas as pd
import streamlit as st
from streamlit_extras.app_logo import add_logo
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
from modules.nav import SideBarLinks
import requests

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

logger = logging.getLogger(__name__)

API_URL = "http://api:4000"

def get_performance(player_id, mission_id=None):
    if mission_id:
        response = requests.get(f"{API_URL}/p/performance/{player_id}?mission_id={mission_id}")
    else:
        response = requests.get(f"{API_URL}/p/performance/{player_id}")
    return response.json() if response.status_code == 200 else None

st.title("Player Performance")

player_id = st.number_input("Enter your Player ID", min_value=1, step=1)

if player_id:
    st.header("Performance")

    # Fetch all performance data
    all_performance = get_performance(player_id)

    if all_performance:
        # Convert the response to a DataFrame
        df_performance = pd.DataFrame(all_performance)

        # Ensure the data is aligned with the correct columns by explicitly defining the columns in the correct order
        df_performance = df_performance[['totalKills', 'totalDeaths', 'DPS', 'dateCompleted', 'missionName', 'missionDescription']]

        # Rename columns for better readability
        df_performance.columns = ['Total Kills', 'Total Deaths', 'DPS', 'Date Completed', 'Mission Name', 'Mission Description']

        # Reorder columns to make the table more intuitive
        df_performance = df_performance[['Mission Name', 'Mission Description', 'Date Completed', 'Total Kills', 'Total Deaths', 'DPS']]

        # Display a dropdown to filter by mission
        missions = df_performance['Mission Name'].unique().tolist()
        missions.insert(0, "All Missions")  # Add an option to view all missions

        selected_mission = st.selectbox("Select a Mission", options=missions)

        if selected_mission != "All Missions":
            filtered_performance = df_performance[df_performance['Mission Name'] == selected_mission]
        else:
            filtered_performance = df_performance

        st.dataframe(filtered_performance)

        # Basic data analysis
        st.header("Performance Analysis")

        total_kills = filtered_performance['Total Kills'].sum()
        total_deaths = filtered_performance['Total Deaths'].sum()
        avg_dps = filtered_performance['DPS'].mean()

        st.markdown(f"""
        - **Total Kills:** {total_kills}
        - **Total Deaths:** {total_deaths}
        - **Average DPS:** {avg_dps:.2f}
        """)

        # Plotting performance over time
        st.subheader("Performance Over Time")
        fig = px.line(filtered_performance, x='Date Completed', y='DPS', title='DPS Over Time')
        st.plotly_chart(fig)

    else:
        st.error("Failed to retrieve performance data")