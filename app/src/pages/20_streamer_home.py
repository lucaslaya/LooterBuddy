import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Welcome Streamer, {st.session_state['first_name']}.")
st.write('')
st.write('')
st.write('### What would you like to do today?')

if st.button('View loadout use statistics', 
             type='primary',
             use_container_width=True):
    st.switch_page('pages/21_loadout_use.py')

if st.button('View community reactions', 
             type='primary',
             use_container_width=True):
    st.switch_page('pages/22_streamer_community.py')

if st.button('Post a new article/notice',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/23_streamer_post.py')