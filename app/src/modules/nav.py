# Idea borrowed from https://github.com/fsmosca/sample-streamlit-authenticator

import streamlit as st

#### ------------------------ General ------------------------
def HomeNav():
    st.sidebar.page_link("Home.py", label="Home", icon='🏠')

#### ------------------------ Player --------------------------
def PlayerHomeNav():
    st.sidebar.page_link("pages/00_player_home.py", label="Home", icon='🏠')

def InventoryLoadoutNav():
    st.sidebar.page_link("pages/01_inventory_loadout.py", label="Inventory/Loadout")

def PlayerPerformanceNav():
    st.sidebar.page_link("pages/02_player_performance.py", label="Performance")

#### ------------------------- Developer ----------------------
def DeveloperHomeNav():
    st.sidebar.page_link("pages/10_developer_home.py", label="Home")

def DeveloperPerformanceNav():
    st.sidebar.page_link("pages/11_performance.py", label="Performance Statistics")

def DeveloperLoadoutUseNav():
    st.sidebar.page_link("pages/12_loadout_use.py", label="Loadout Use Statistics")

def DeveloperCommunityNav():
    st.sidebar.page_link("pages/13_developer_community.py", label="Community Management")

# --------------------------------Links Function -----------------------------------------------
def SideBarLinks(show_home=False):
    """
    This function handles adding links to the sidebar of the app based upon the logged-in user's role, which was put in the streamlit session_state object when logging in. 
    """    

    # add a logo to the sidebar always
    st.sidebar.image("assets/logo.png", width = 150)

    # If there is no logged in user, redirect to the Home (Landing) page
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
        st.switch_page('Home.py')
        
    if show_home:
        # Show the Home page link (the landing page)
        HomeNav()

    # Show the other page navigators depending on the users' role.
    if st.session_state["authenticated"]:

        # Show World Bank Link and Map Demo Link if the user is a political strategy advisor role.
        if st.session_state['role'] == 'player':
            PlayerHomeNav()
            InventoryLoadoutNav()
            PlayerPerformanceNav()

        # If the user role is usaid worker, show the Api Testing page
        if st.session_state['role'] == 'developer':
            DeveloperHomeNav()
            DeveloperPerformanceNav()
            DeveloperLoadoutUseNav()
            DeveloperCommunityNav()
        
        # If the user is an administrator, give them access to the administrator pages
        if st.session_state['role'] == 'streamer':
            #AdminPageNav()
            pass

    if st.session_state["authenticated"]:
        # Always show a logout button if there is a logged in user
        if st.sidebar.button("Logout"):
            del st.session_state['role']
            del st.session_state['authenticated']
            st.switch_page('Home.py')

