import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Welcome Player, {st.session_state['first_name']}.")
st.write('')
st.write('')
st.write('### What would you like to do today?')

if st.button('View and manage your inventory and loadout', 
             type='primary',
             use_container_width=True):
    st.switch_page('pages/01_inventory_loadout.py')

if st.button('View player performance', 
             type='primary',
             use_container_width=True):
    st.switch_page('pages/02_player_performance.py')

if st.button('Keep up with posts and developer updates',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/03_player_community.py')