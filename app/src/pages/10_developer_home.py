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

if st.button('View mission performances', 
             type='primary',
             use_container_width=True):
    st.switch_page('pages/11_performance.py')

if st.button('View weapon use statistics', 
             type='primary',
             use_container_width=True):
    st.switch_page('pages/12_loadout_use.py')

if st.button('Post and manage community posts',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/13_developer_community.py')