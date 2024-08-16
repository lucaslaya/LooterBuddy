import streamlit as st
import requests

# Set base URL for the API
base_url = "http://api:4000/p"  # Replace with your actual backend URL

# Function to get update posts from developers
def get_developer_posts():
    response = requests.get(f"{base_url}/posts")
    if response.status_code == 200:
        posts = response.json()
        return [post for post in posts if post['tag'] == 'update']
    return []

# Function to get posts from content creators the player follows
def get_followed_content_creator_posts(player_id):
    response = requests.get(f"{base_url}/follows/{player_id}")
    followed_creators = response.json() if response.status_code == 200 else []
    followed_usernames = [creator['username'] for creator in followed_creators]

    response = requests.get(f"{base_url}/posts")
    if response.status_code == 200:
        posts = response.json()
        return [post for post in posts if post['username'] in followed_usernames]
    return []

# Function to get detailed post information, including likes and comments
def get_post_details(post_id):
    response = requests.get(f"{base_url}/posts/{post_id}")
    if response.status_code == 200:
        return response.json()
    return {}

# Function to like a post
def like_post(player_id, post_id):
    response = requests.post(f"{base_url}/likes/{player_id}/{post_id}")
    return response.status_code == 201

# Function to add a comment to a post
def add_comment(player_id, post_id, comment_content):
    response = requests.post(f"{base_url}/comments/{player_id}/{post_id}", json={"content": comment_content})
    return response.status_code == 201

# Function to get the list of content creators
def get_content_creators():
    response = requests.get(f"{base_url}/streamers")
    if response.status_code == 200:
        return response.json()
    return []

# Function to follow or unfollow a content creator
def update_follow_status(player_id, streamer_id, follow=True):
    if follow:
        response = requests.post(f"{base_url}/follows/{player_id}/{streamer_id}")
    else:
        response = requests.delete(f"{base_url}/follows/{player_id}/{streamer_id}")
    return response.status_code == 201 if follow else response.status_code == 200

# Streamlit App Layout
st.title("Looter Buddy: Player Dashboard")

# Get the current player ID
player_id = st.number_input("Enter your Player ID", min_value=1, step=1)

# Display developer posts
st.header("Developer Updates")
developer_posts = get_developer_posts()
for post in developer_posts:
    st.subheader(post['title'])
    st.write(post['content'])
    st.write(f"Posted on: {post['dateCreated']}")

# Display content creator posts
st.header("Posts from Content Creators You Follow")
creator_posts = get_followed_content_creator_posts(player_id)
for post in creator_posts:
    st.subheader(post['title'])
    st.write(post['content'])
    st.write(f"Posted by: {post['username']} on {post['dateCreated']}")

# Post details section
st.header("Investigate a Post")
all_posts = developer_posts + creator_posts
selected_post_title = st.selectbox("Select a post to view details", [post['title'] for post in all_posts])
selected_post = next((post for post in all_posts if post['title'] == selected_post_title), None)

if selected_post:
    post_details = get_post_details(selected_post['postID'])
    st.subheader(post_details['title'])
    st.write(post_details['content'])
    st.write(f"Total Likes: {post_details['likes']}")
    st.write("Comments:")
    for comment in post_details['comments']:
        st.write(f"{comment['username']}: {comment['content']} (Posted on: {comment['dateCreated']})")

    # Like the post
    if st.button("Like this post"):
        if like_post(player_id, selected_post['postID']):
            st.success("You liked this post!")

    # Add a comment
    comment_content = st.text_input("Add a comment")
    if st.button("Post Comment"):
        if add_comment(player_id, selected_post['postID'], comment_content):
            st.success("Your comment was posted!")

# Follow/Unfollow content creators
st.header("Manage Content Creator Follows")
creators = get_content_creators()
creator_names = [creator['username'] for creator in creators]
followed_creators = [post['username'] for post in creator_posts]

selected_creator_name = st.selectbox("Select a content creator", creator_names)
selected_creator = next((creator for creator in creators if creator['username'] == selected_creator_name), None)

if selected_creator:
    streamer_id = selected_creator['streamerID']
    if selected_creator_name in followed_creators:
        if st.button(f"Unfollow {selected_creator_name}"):
            if update_follow_status(player_id, streamer_id, follow=False):
                st.success(f"You unfollowed {selected_creator_name}")
    else:
        if st.button(f"Follow {selected_creator_name}"):
            if update_follow_status(player_id, streamer_id, follow=True):
                st.success(f"You followed {selected_creator_name}")