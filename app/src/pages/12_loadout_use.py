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

@st.cache_data
def get_item_names():
    response = requests.post(f"{API_URL}/d/items/names")
    if response.status_code == 200:
        item_dict = {item['itemID']: item['name'] for item in response.json()}
        return item_dict
    else:
        st.error("Failed to load item names.")
        return {}

# Helper function to load data
def load_loadout_use_data(mission_id):
    response = requests.get(f"{API_URL}/d/loadoutuse/{mission_id}")
    
    if response.status_code == 200:
        return pd.DataFrame(response.json())
    return pd.DataFrame()

def load_mission_data():
    response = requests.get(f"{API_URL}/d/missions")
    if response.status_code == 200:
        return response.json()
    return []

# Main Streamlit App
st.title("Loadout Use Analysis")

# Load data
item_names = get_item_names()
if not isinstance(item_names, dict) or not item_names:
    st.error("Item names could not be loaded properly. Please check the API or data.")
else:
    # Load mission data
    missions = load_mission_data()

    # Mission Selector
    mission_options = [mission['name'] for mission in missions]
    mission_choice = st.selectbox("Select Mission", mission_options)

    selected_mission_id = next(mission['missionID'] for mission in missions if mission['name'] == mission_choice)

    # Load loadout use data
    loadout_data = load_loadout_use_data(selected_mission_id)

    # Replace itemIDs with names in loadout use data
    if not loadout_data.empty:
        for col in ['weapon1', 'weapon2', 'armor1', 'armor2', 'armor3']:
            loadout_data[col] = loadout_data[col].map(item_names)

    # Display loadout use data
    st.subheader("Loadout Use Data")
    if not loadout_data.empty:
        st.dataframe(loadout_data)
    else:
        st.write("No loadout use data available.")

    # Analyze item use popularity
    st.subheader("Item Use Popularity Analysis")
    if not loadout_data.empty:
        item_use_counts = loadout_data[['weapon1', 'weapon2', 'armor1', 'armor2', 'armor3']].apply(pd.Series.value_counts).fillna(0)
        st.bar_chart(item_use_counts.sum(axis=1).sort_values(ascending=False))
    else:
        st.write("No data available for item use analysis.")
