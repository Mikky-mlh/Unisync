# File: 2_Find_Peers.py
# Purpose: Tinder-style peer matching system with skill exchange
# Assigned to: Yuvraj & Aaradhya
# Deadline: Jan 9, 2024

# Key Features:
# - Swipe through user profiles to connect
# - Track matches and viewed users
# - Display skill exchange marketplace

import streamlit as st
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.data_manager import load_users
from src.utils import calculate_compatibility
import pandas as pd

# Setup page configuration
st.set_page_config(page_title="Find Peers", page_icon="👥", layout="wide")

# Load CSS for styling
try:
    with open("assets/style-peer.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except:
    pass  # CSS file optional

# Initialize session state variables
if 'viewed_users' not in st.session_state:
    st.session_state.viewed_users = []  # Track users we've seen
if 'matches' not in st.session_state:
    st.session_state.matches = []  # Track users we connected with
if 'current_user_index' not in st.session_state:
    st.session_state.current_user_index = 0  # Track which user to show

# Load all users from CSV
users = load_users()

# Tinder-style swipe UI
st.title("👥 Campus Tribe - Find Your People")
st.markdown("### Swipe to connect with fellow students")

# Filter: Remove current user (assume user ID 1 is logged in)
current_user_id = 1
available_users = [u for u in users if u.get('id') != current_user_id and u.get('id') not in st.session_state.viewed_users]

if not available_users:
    st.info("🎉 You've seen all available users! Check your matches below.")
else:
    # Get current user to display
    if st.session_state.current_user_index >= len(available_users):
        st.session_state.current_user_index = 0

    user = available_users[st.session_state.current_user_index]

    # Center the user card
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # Display user profile
        st.markdown(f"### {user.get('name', 'Unknown')}")
        st.write(f"**Major:** {user.get('major', 'N/A')}")
        st.write(f"**Year:** {user.get('year', 'N/A')}")
        st.write(f"**Skills:** {user.get('skills', 'N/A')}")
        st.write(f"**Interests:** {user.get('interests', 'N/A')}")
        st.info(f"✨ {user.get('x_factor', 'No special skill listed')}")

        st.markdown("---")

        # Swipe buttons
        col_left, col_right = st.columns(2)
        with col_left:
            if st.button("👎 Pass", use_container_width=True, key=f"pass_{user.get('id')}"):
                # Add user ID to viewed_users
                st.session_state.viewed_users.append(user.get('id'))
                st.session_state.current_user_index += 1
                st.rerun()

        with col_right:
            if st.button("👍 Connect", use_container_width=True, key=f"connect_{user.get('id')}"):
                # Add user to matches and viewed_users
                st.session_state.matches.append(user)
                st.session_state.viewed_users.append(user.get('id'))
                st.session_state.current_user_index += 1
                st.success(f"✅ Connected with {user.get('name')}!")
                st.rerun()

# Display study buddy matches
st.markdown("---")
st.subheader("🎓 Your Study Buddy Matches")

if st.session_state.matches:
    st.success(f"You have {len(st.session_state.matches)} matches!")

    # Display matches
    for match in st.session_state.matches:
        with st.expander(f"👤 {match.get('name', 'Unknown')}"):
            st.write(f"**Email:** {match.get('email', 'N/A')}")
            st.write(f"**Major:** {match.get('major', 'N/A')}")
            st.write(f"**Can teach:** {match.get('can_teach', 'N/A')}")
            st.write(f"**Wants to learn:** {match.get('wants_to_learn', 'N/A')}")

            # Calculate and display compatibility score
            # Use calculate_compatibility() from src/utils.py
            # Display as percentage with progress bar
else:
    st.info("No matches yet. Start swiping to find your study buddies!")

# Skill exchange marketplace
st.markdown("---")
st.subheader("🔄 Skill Exchange Marketplace")
st.caption("Connect with students to learn new skills or teach what you know")

# Create two columns for skills
col_teach, col_learn = st.columns(2)

with col_teach:
    st.markdown("### 📚 Skills Available to Learn")
    # Loop through all users
    # Extract and display skills from 'can_teach' field
    # Format: "Python basics" by Yuvraj/Siddhika/Aaradhya (email)

    for user in users:
        if user.get('can_teach'):
            skills = user.get('can_teach', '').split(',')
            for skill in skills:
                st.write(f"• **{skill.strip()}** - {user.get('name')} ({user.get('email')})")

with col_learn:
    st.markdown("### 🎯 Skills People Want to Learn")
    # Loop through all users
    # Extract and display skills from 'wants_to_learn' field
    # Format: "Data Visualization" wanted by Yuvraj/Siddhika/Aaradhya

    for user in users:
        if user.get('wants_to_learn'):
            skills = user.get('wants_to_learn', '').split(',')
            for skill in skills:
                st.write(f"• **{skill.strip()}** - {user.get('name')}")

# Bonus filters
st.sidebar.markdown("---")
st.sidebar.subheader("🔍 Filters (Bonus)")
# Add filters for major, skills, etc.
# major_filter = st.sidebar.selectbox("Filter by Major", ["All"] + list(set([u.get('major') for u in users])))
