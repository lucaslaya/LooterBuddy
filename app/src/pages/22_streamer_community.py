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

# Helper function to get follow count
def get_follow_count(streamer_id):
    try:
        response = requests.get(f"{API_URL}/s/follows/count/{streamer_id}")
        if response.status_code == 200:
            return response.json().get("follow_count", 0)
        else:
            logger.error(f"Failed to fetch follow count: {response.status_code}")
            return 0
    except Exception as e:
        logger.error(f"Error fetching follow count: {e}")
        return 0

# Helper function to get posts by streamer
def get_posts(streamer_id):
    try:
        response = requests.get(f"{API_URL}/s/posts/{streamer_id}")
        if response.status_code == 200:
            return response.json()
        else:
            logger.error(f"Failed to fetch posts: {response.status_code}")
            return []
    except Exception as e:
        logger.error(f"Error fetching posts: {e}")
        return []

# Helper function to get post details
def get_post_details(post_id):
    try:
        response = requests.get(f"{API_URL}/s/posts/details/{post_id}")
        if response.status_code == 200:
            return response.json()
        else:
            logger.error(f"Failed to fetch post details: {response.status_code}")
            return {}
    except Exception as e:
        logger.error(f"Error fetching post details: {e}")
        return {}

# Main Streamlit App
st.title("Streamer Dashboard")

# Streamer input
streamer_id = 1

if streamer_id:
    # Display follow count
    follow_count = get_follow_count(streamer_id)
    st.subheader(f"Total Followers: {follow_count}")

    # Display posts
    posts = get_posts(streamer_id)
    if posts:
        post_titles = {post['title']: post['postID'] for post in posts}
        selected_post = st.selectbox("Select Post", list(post_titles.keys()))

        if selected_post:
            selected_post_id = post_titles[selected_post]

            if st.button("View Post Details"):
                post_details = get_post_details(selected_post_id)
                if post_details:
                    st.write(f"**Title**: {post_details.get('title')}")
                    st.write(f"**Content**: {post_details.get('content')}")
                    st.write(f"**Likes**: {post_details.get('likes', 0)}")
                    st.write("**Comments**:")
                    
                    comments = post_details.get('comments', [])
                    
                    # Display comments
                    if comments:
                        for comment in comments:
                            st.write(f"- {comment['content']} (by {comment['username']})")
                    else:
                        st.write("No comments available.")
                else:
                    st.error("Failed to load post details.")
    else:
        st.write("No posts available.")