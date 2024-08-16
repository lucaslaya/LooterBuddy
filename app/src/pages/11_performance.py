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

def get_all_performance():
    response = requests.get(f"{API_URL}/d/performance")
    return response.json() if response.status_code == 200 else None

def get_performance_by_player(player_id):
    response = requests.get(f"{API_URL}/d/performance/{player_id}")
    return response.json() if response.status_code == 200 else None

def get_missions():
    response = requests.get(f"{API_URL}/d/missions")
    return response.json() if response.status_code == 200 else None

st.title("Player Performance Analysis")

# Option to view all performances or filter by player/mission
view_option = st.radio("Choose an option to view performances:", 
                       ("All Performances", "By Player", "By Mission"))

if view_option == "All Performances":
    performances = get_all_performance()
    if performances:
        df_performance = pd.DataFrame(performances)
        
        # Clean up column names
        df_performance.columns = ['Player ID', 'Performance ID', 'Total Kills', 'Total Deaths', 
                                  'DPS', 'Date Completed', 'Mission Name', 'Mission Description', 
                                  'Weapon 1', 'Weapon 2', 'Armor 1', 'Armor 2', 'Armor 3']
        
        st.subheader("All Player Performances")
        st.dataframe(df_performance)
        
        # Plotting DPS distribution
        st.subheader("DPS Distribution")
        fig = px.histogram(df_performance, x='DPS', nbins=20, title='DPS Distribution')
        st.plotly_chart(fig)
        
        # Summary statistics
        st.subheader("Summary Statistics")
        st.write(df_performance.describe())
        
        # Option to filter by specific mission
        missions = get_missions()
        mission_names = [mission['name'] for mission in missions]
        selected_mission = st.selectbox("Select a mission to filter performances:", mission_names)
        
        if selected_mission:
            filtered_df = df_performance[df_performance['Mission Name'] == selected_mission]
            st.write(f"Showing performance data for mission: {selected_mission}")
            st.dataframe(filtered_df)
            
else:
    player_id = st.number_input("Enter Player ID:", min_value=1, step=1)
    
    if player_id:
        performances = get_performance_by_player(player_id)
        if performances:
            df_performance = pd.DataFrame(performances)
            
            # Clean up column names
            df_performance.columns = ['Player ID', 'Performance ID', 'Total Kills', 'Total Deaths', 
                                      'DPS', 'Date Completed', 'Mission Name', 'Mission Description', 
                                      'Weapon 1', 'Weapon 2', 'Armor 1', 'Armor 2', 'Armor 3']
            
            st.subheader(f"Performance Data for Player {player_id}")
            st.dataframe(df_performance)
            
            # Plotting DPS over time
            st.subheader("DPS Over Time")
            fig = px.line(df_performance, x='Date Completed', y='DPS', title='DPS Over Time')
            st.plotly_chart(fig)
            
            # Summary statistics
            st.subheader("Summary Statistics")
            st.write(df_performance.describe())
            
            # Option to filter by specific mission
            missions = get_missions()
            mission_names = [mission['name'] for mission in missions]
            selected_mission = st.selectbox("Select a mission to filter performances:", mission_names)
            
            if selected_mission:
                filtered_df = df_performance[df_performance['Mission Name'] == selected_mission]
                st.write(f"Showing performance data for mission: {selected_mission}")
                st.dataframe(filtered_df)

