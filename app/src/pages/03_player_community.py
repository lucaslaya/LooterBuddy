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

# API URL
API_URL = "http://api:4000"

# Function to get update articles
def get_update_articles():
    response = requests.get(f"{API_URL}/p/posts/update-articles")
    return response.json()

# Function to get articles from followed streamers
def get_streamer_articles(player_id):
    response = requests.get(f"{API_URL}/p/posts/streamer-articles/{player_id}")
    return response.json()

# Function to get likes and comments for a post
def get_post_details(post_id):
    response = requests.get(f"{API_URL}/p/posts/details/{post_id}")
    return response.json()

# Function to like a post
def like_post(user_id, post_id):
    response = requests.post(f"{API_URL}/p/posts/like", json={"userID": user_id, "postID": post_id})
    
    # Check if the response is successful
    if response.status_code == 200:
        try:
            return response.json()
        except ValueError:
            st.error("Error decoding JSON response")
            return None
    else:
        st.error(f"Error: Received status code {response.status_code}")
        return None

# Function to comment on a post
def comment_on_post(user_id, post_id, content):
    response = requests.post(f"{API_URL}/p/posts/comment", json={"userID": user_id, "postID": post_id, "content": content})
    return response.json()

# Function to get the list of followed streamers
def get_followed_streamers(player_id):
    response = requests.get(f"{API_URL}/p/follows/followed/{player_id}")
    return response.json()

# Function to get all streamers
def get_all_streamers():
    response = requests.get(f"{API_URL}/p/streamers")
    return response.json()

# Function to follow a streamer
def follow_streamer(player_id, streamer_id):
    response = requests.post(f"{API_URL}/p/follows/follow", json={"userID": player_id, "streamerID": streamer_id})
    return response.json()

# Function to unfollow a streamer
def unfollow_streamer(player_id, streamer_id):
    response = requests.post(f"{API_URL}/p/follows/unfollow", json={"userID": player_id, "streamerID": streamer_id})
    return response.json()

# Streamlit page layout
st.title("Player Dashboard")

player_id = 1 

# Display update articles in a table
st.header("Update Articles")
update_articles = get_update_articles()

if update_articles:
    update_df = pd.DataFrame(update_articles)
    st.table(update_df[['title', 'dateCreated']])

# Display articles from followed streamers in a table
st.header("Articles from Followed Streamers")
streamer_articles = get_streamer_articles(player_id)

if streamer_articles:
    streamer_df = pd.DataFrame(streamer_articles)
    st.table(streamer_df[['title', 'dateCreated']])

# Combine article titles for the dropdown selection
all_articles = update_articles + streamer_articles
all_article_titles = [article['title'] for article in all_articles]

# Allow the user to select an article from a dropdown to view details
selected_article_title = st.selectbox("Select an Article to View Details", all_article_titles)

# Find the selected article in the combined list
selected_article = next((article for article in all_articles if article['title'] == selected_article_title), None)

# Display selected article details
if selected_article:
    article_details = get_post_details(selected_article['postID'])
    st.write("Title:", article_details['post']['title'])
    st.write("Content:", article_details['post']['content'])
    st.write("Likes:", article_details['likes'])
    st.write("Comments:")
    for comment in article_details['comments']:
        st.write(f"- {comment['content']} (by {comment['username']})")

    # Like the post
    if st.button("Like this post"):
        like_post(player_id, selected_article['postID'])
        st.success("Post liked!")

    # Comment on the post
    new_comment = st.text_input("Add a comment")
    if st.button("Comment"):
        comment_on_post(player_id, selected_article['postID'], new_comment)
        st.success("Comment added!")

# Follow or unfollow a streamer
st.header("Manage Followed Streamers")
followed_streamers = get_followed_streamers(player_id)
followed_streamer_names = [streamer.get('username', f"Streamer ID {streamer['streamerID']}") for streamer in followed_streamers]

# Select a streamer to unfollow
selected_unfollow_streamer = st.selectbox("Select a Streamer to Unfollow", followed_streamer_names)

if selected_unfollow_streamer and st.button("Unfollow"):
    # Find the streamer ID of the selected streamer
    streamer_id = next(streamer['streamerID'] for streamer in followed_streamers if streamer.get('username') == selected_unfollow_streamer)
    
    # Call the unfollow function with the correct player ID and streamer ID
    unfollow_streamer(player_id, streamer_id)
    st.success(f"Unfollowed {selected_unfollow_streamer}!")

all_streamers = get_all_streamers()
all_streamer_names = [streamer['username'] for streamer in all_streamers if streamer['username'] not in followed_streamer_names]
selected_streamer = st.selectbox("Select a Streamer to Follow", all_streamer_names)

if selected_streamer and st.button("Follow"):
    streamer_id = next(streamer['streamerID'] for streamer in all_streamers if streamer['username'] == selected_streamer)
    follow_streamer(player_id, streamer_id)
    st.success(f"Followed {follow_streamer}!")