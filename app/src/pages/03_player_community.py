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

logger = logging.getLogger(__name__)

API_URL = "http://api:4000"

def get_posts():
    response = requests.get(f"{API_URL}/p/posts")
    return response.json() if response.status_code == 200 else None

def get_followed_streamers(player_id):
    response = requests.get(f"{API_URL}/p/follows/{player_id}")
    return response.json() if response.status_code == 200 else None

def get_likes(post_id):
    response = requests.get(f"{API_URL}/p/likes/{post_id}")
    return response.json() if response.status_code == 200 else None

def get_comments(post_id):
    response = requests.get(f"{API_URL}/p/comments/{post_id}")
    return response.json() if response.status_code == 200 else None

def get_streamers():
    response = requests.get(f"{API_URL}/p/streamers")
    return response.json() if response.status_code == 200 else None

def add_like(player_id, post_id):
    response = requests.post(f"{API_URL}/p/likes/{player_id}/{post_id}")
    return response.status_code == 201

def add_comment(player_id, post_id, content):
    payload = {"content": content}
    response = requests.post(f"{API_URL}/p/comments/{player_id}/{post_id}", json=payload)
    return response.status_code == 201

def add_follow(player_id, streamer_id):
    response = requests.post(f"{API_URL}/p/follows/{player_id}/{streamer_id}")
    return response.status_code == 201

def remove_follow(player_id, streamer_id):
    response = requests.delete(f"{API_URL}/p/follows/{player_id}/{streamer_id}")
    return response.status_code == 200

st.title("Player Posts and Streamer Interaction")

player_id = st.number_input("Enter your Player ID", min_value=1, step=1)

if player_id:
    st.header("Posts")

    posts = get_posts()
    if posts:
        df_posts = pd.DataFrame(posts)

        # Separate posts by updates and followed streamers
        update_posts = df_posts[df_posts['tag'] == 'update']
        streamer_posts = df_posts[df_posts['streamerID'].notnull()]

        st.subheader("Game Updates")
        st.dataframe(update_posts[['title', 'content', 'dateCreated']])

        st.subheader("Posts from Followed Streamers")
        followed_streamers = get_followed_streamers(player_id)
        followed_streamer_ids = [streamer['username'] for streamer in followed_streamers]

        followed_posts = streamer_posts[streamer_posts['streamerID'].isin(followed_streamer_ids)]
        st.dataframe(followed_posts[['title', 'content', 'dateCreated']])

        st.subheader("Interact with Posts")

        if not followed_posts.empty:
            selected_post = st.selectbox("Select a Post to Interact With", options=followed_posts['title'].tolist())

            # Fix: Get the actual postID instead of using the index
            if selected_post in followed_posts['title'].values:
                selected_post_id = followed_posts[followed_posts['title'] == selected_post]['postID'].values[0]

                st.write("### Post Details")
                st.write(f"**Title:** {followed_posts[followed_posts['postID'] == selected_post_id]['title'].values[0]}")
                st.write(f"**Content:** {followed_posts[followed_posts['postID'] == selected_post_id]['content'].values[0]}")
                st.write(f"**Date Created:** {followed_posts[followed_posts['postID'] == selected_post_id]['dateCreated'].values[0]}")

                st.write("### Likes and Comments")
                if st.button("Like Post"):
                    if add_like(player_id, selected_post_id):
                        st.success("You liked the post!")
                    else:
                        st.error("Failed to like the post.")

                comment_content = st.text_area("Add a Comment")
                if st.button("Post Comment"):
                    if add_comment(player_id, selected_post_id, comment_content):
                        st.success("Comment added successfully.")
                    else:
                        st.error("Failed to add comment.")

                st.write("### Existing Likes")
                likes = get_likes(selected_post_id)
                if likes:
                    st.dataframe(pd.DataFrame(likes, columns=["Username"]))
                else:
                    st.write("No likes yet.")

                st.write("### Existing Comments")
                comments = get_comments(selected_post_id)
                if comments:
                    st.dataframe(pd.DataFrame(comments, columns=["Username", "Comment", "Date Created"]))
                else:
                    st.write("No comments yet.")
            else:
                st.error("Selected post not found.")
        else:
            st.warning("No posts available from followed streamers.")

    all_streamers = get_streamers()
    if all_streamers:
        all_streamer_names = [streamer['username'] for streamer in all_streamers]
        st.write("### Follow New Streamers")
        selected_new_streamer = st.selectbox("Select a Streamer to Follow", options=all_streamer_names)
        if st.button("Follow Streamer"):
            new_streamer_id = all_streamers[all_streamer_names.index(selected_new_streamer)]['streamerID']
            if add_follow(player_id, new_streamer_id):
                st.success(f"You followed {selected_new_streamer}.")
            else:
                st.error("Failed to follow streamer.")
else:
    st.error("Please enter a valid Player ID.")