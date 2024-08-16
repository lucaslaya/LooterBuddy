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

# Helper function to post an update article
def post_update_article(title, content, developer_id):
    payload = {
        "title": title,
        "content": content,
        "tag": "update",
        "developerID": developer_id
    }
    response = requests.post(f"{API_URL}/d/posts", json=payload)
    return response

# Helper function to delete a post
def delete_post(post_id):
    response = requests.delete(f"{API_URL}/d/posts/{post_id}")
    return response

# Helper function to get post likes and comments
def get_post_likes_comments(post_id):
    response = requests.get(f"{API_URL}/d/posts/{post_id}")
    if response.status_code == 200:
        return response.json()
    return {}

# Helper function to get all posts
@st.cache_data
def get_all_posts():
    response = requests.get(f"{API_URL}/d/posts")
    if response.status_code == 200:
        return response.json()
    return []

# Main Streamlit App
st.title("Admin Dashboard")

# Section for posting an update article
st.subheader("Post an Update Article")
with st.form("post_update"):
    title = st.text_input("Title")
    content = st.text_area("Content")
    developer_id = st.text_input("Developer ID")  # Assuming developer ID is known
    submit_button = st.form_submit_button(label="Post Update")

    if submit_button:
        if title and content and developer_id:
            response = post_update_article(title, content, developer_id)
            if response.status_code == 201:
                st.success("Update article posted successfully!")
            else:
                st.error("Failed to post update article.")
        else:
            st.error("All fields must be filled out.")

# Section for deleting a post
st.subheader("Delete a Post")

# Load all posts
all_posts = get_all_posts()

if all_posts:
    post_titles = {post['title']: post['postID'] for post in all_posts}
    post_choice_delete = st.selectbox("Select Post to Delete", list(post_titles.keys()))

    selected_post_id_delete = post_titles[post_choice_delete]

    if st.button("Delete Post"):
        response = delete_post(selected_post_id_delete)
        if response.status_code == 200:
            st.success(f"Post '{post_choice_delete}' deleted successfully.")
        else:
            st.error(f"Failed to delete post '{post_choice_delete}'.")
else:
    st.write("No posts available.")

# Section for viewing likes and comments on update posts
st.subheader("View Likes and Comments on Update Posts")

if all_posts:
    update_post_titles = {post['title']: post['postID'] for post in all_posts if post['tag'] == 'update'}
    post_choice_view = st.selectbox("Select Post to View", list(update_post_titles.keys()))

    selected_post_id_view = update_post_titles[post_choice_view]

    if st.button("View Likes and Comments"):
        post_data = get_post_likes_comments(selected_post_id_view)
        if post_data:
            st.write(f"**Title**: {post_data.get('title')}")
            st.write(f"**Likes**: {post_data.get('likes', 0)}")
            st.write(f"**Comments**:")
            comments = post_data.get('comments', [])
            if comments:
                for comment in comments:
                    st.write(f"- {comment['content']} (by {comment['username']})")
            else:
                st.write("No comments available.")
        else:
            st.error(f"No data found for post ID {selected_post_id_view}.")
else:
    st.write("No update posts available.")
