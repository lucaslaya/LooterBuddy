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

# API URL
API_URL = "http://api:4000"

# Helper function to create a post
def create_post(title, content, streamer_id):
    try:
        payload = {
            "title": title,
            "content": content,
            "tag": "social",
            "streamerID": streamer_id
        }
        response = requests.post(f"{API_URL}/s/posts", json=payload)
        if response.status_code == 201:
            return True, "Post created successfully!"
        else:
            return False, f"Failed to create post. Error: {response.json().get('error', 'Unknown error')}"
    except Exception as e:
        logger.error(f"Error creating post: {e}")
        return False, "An unexpected error occurred."

# Main Streamlit App
st.title("Create a New Post")

# Streamer inputs
streamer_id = st.text_input("Streamer ID")
title = st.text_input("Post Title")
content = st.text_area("Post Content")

# Button to submit the post
if st.button("Create Post"):
    if all([streamer_id, title, content]):
        success, message = create_post(title, content, streamer_id)
        if success:
            st.success(message)
        else:
            st.error(message)
    else:
        st.error("All fields must be filled out to create a post.")
