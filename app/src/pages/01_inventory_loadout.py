import logging
logger = logging.getLogger(__name__)
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

API_URL = "http://api:4000"

def get_inventory(player_id):
    response = requests.get(f"{API_URL}/p/inventory/{player_id}")
    return response.json() if response.status_code == 200 else None

def get_loadout(player_id):
    response = requests.get(f"{API_URL}/p/loadout/{player_id}")
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to retrieve loadout data. Please check if the player ID is correct or if the player has a loadout.")
        return None

def update_loadout(player_id, weapon1, weapon2, armor1, armor2, armor3):
    payload = {
        'weapon1': weapon1,
        'weapon2': weapon2,
        'armor1': armor1,
        'armor2': armor2,
        'armor3': armor3
    }
    response = requests.put(f"{API_URL}/p/loadout/{player_id}", json=payload)
    return response.status_code == 200

st.title("Player Inventory and Loadout")

player_id = 23

if player_id:
    st.header("Inventory")
    inventory = get_inventory(player_id)
    if inventory:
        df_inventory = pd.DataFrame(inventory)

        # Filter inventory to separate weapons and armor
        df_weapons = df_inventory[df_inventory['itemType'] == 'weapon'][['itemID', 'itemName', 'itemRarity', 'itemDamage', 'itemMagSize', 'itemFireRate']]
        df_armor = df_inventory[df_inventory['itemType'] == 'armor'][['itemID', 'itemName', 'itemRarity', 'itemDefense']]

        # Rename columns to be more user-friendly
        df_weapons.columns = ['Item ID', 'Item Name', 'Rarity', 'Damage', 'Magazine Size', 'Fire Rate']
        df_armor.columns = ['Item ID', 'Item Name', 'Rarity', 'Defense']

        st.subheader("Weapons")
        st.dataframe(df_weapons[['Item Name', 'Rarity', 'Damage', 'Magazine Size', 'Fire Rate']])

        st.subheader("Armor")
        st.dataframe(df_armor[['Item Name', 'Rarity', 'Defense']])

        # Weapon and armor options for loadout change form
        weapon_options = {"Keep current": None}
        weapon_options.update({row['Item Name']: row['Item ID'] for _, row in df_weapons.iterrows()})

        armor_options = {"Keep current": None}
        armor_options.update({row['Item Name']: row['Item ID'] for _, row in df_armor.iterrows()})
    else:
        st.error("Failed to retrieve inventory")

    st.header("Loadout")
    loadout = get_loadout(player_id)
    if loadout:
        # Extract current loadout items
        current_weapon1_id = loadout[0]['weapon1_id']
        current_weapon1_name = loadout[0]['weapon1']
        current_weapon2_id = loadout[0]['weapon2_id']
        current_weapon2_name = loadout[0]['weapon2']
        current_armor1_id = loadout[0]['armor1_id']
        current_armor1_name = loadout[0]['armor1']
        current_armor2_id = loadout[0]['armor2_id']
        current_armor2_name = loadout[0]['armor2']
        current_armor3_id = loadout[0]['armor3_id']
        current_armor3_name = loadout[0]['armor3']

        # Display the current loadout
        st.subheader("Current Loadout")
        st.markdown(f"""
        - **Weapon 1:** {current_weapon1_name}
        - **Weapon 2:** {current_weapon2_name}
        - **Armor 1:** {current_armor1_name}
        - **Armor 2:** {current_armor2_name}
        - **Armor 3:** {current_armor3_name}
        """)

        # Form to change loadout
        st.subheader("Change Loadout")
        with st.form("change_loadout"):
            weapon1_name = st.selectbox("Weapon 1", options=list(weapon_options.keys()), index=list(weapon_options.keys()).index(current_weapon1_name) if current_weapon1_name in weapon_options else 0)
            weapon2_name = st.selectbox("Weapon 2", options=list(weapon_options.keys()), index=list(weapon_options.keys()).index(current_weapon2_name) if current_weapon2_name in weapon_options else 0)
            armor1_name = st.selectbox("Armor 1", options=list(armor_options.keys()), index=list(armor_options.keys()).index(current_armor1_name) if current_armor1_name in armor_options else 0)
            armor2_name = st.selectbox("Armor 2", options=list(armor_options.keys()), index=list(armor_options.keys()).index(current_armor2_name) if current_armor2_name in armor_options else 0)
            armor3_name = st.selectbox("Armor 3", options=list(armor_options.keys()), index=list(armor_options.keys()).index(current_armor3_name) if current_armor3_name in armor_options else 0)

            # Map item names to itemIDs for API request
            weapon1_id = current_weapon1_id if weapon1_name == "Keep current" else weapon_options[weapon1_name]
            weapon2_id = current_weapon2_id if weapon2_name == "Keep current" else weapon_options[weapon2_name]
            armor1_id = current_armor1_id if armor1_name == "Keep current" else armor_options[armor1_name]
            armor2_id = current_armor2_id if armor2_name == "Keep current" else armor_options[armor2_name]
            armor3_id = current_armor3_id if armor3_name == "Keep current" else armor_options[armor3_name]


            submitted = st.form_submit_button("Update Loadout")
            if submitted:
                success = update_loadout(player_id, weapon1_id, weapon2_id, armor1_id, armor2_id, armor3_id)
                if success:
                    st.success("Loadout updated successfully")
                    #st.experimental_rerun()
                else:
                    st.error("Failed to update loadout")
    else:
        st.error("Failed to retrieve loadout")