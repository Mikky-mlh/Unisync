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

# Check if user is logged in
if 'current_user' not in st.session_state or st.session_state.current_user is None:
    st.warning("🔒 Please login from the Home page to access Find Peers")
    st.stop()

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

# Bonus filters
st.sidebar.markdown("---")
st.sidebar.subheader("🔍 Advanced Search")

# Get unique values for filters
all_majors = ["All"] + sorted(set(u.get("major", "") for u in users if u.get("major")))
all_years = ["All"] + sorted(set(u.get("year", "") for u in users if u.get("year")))

# Filter options
selected_major = st.sidebar.selectbox("🎓 Filter by Major", all_majors)
selected_year = st.sidebar.selectbox("📅 Filter by Year", all_years)

# Skills and interests filters
all_skills = set()
all_interests = set()

for user in users:
    if user.get("skills"):
        skills = [s.strip() for s in user.get("skills", "").split(",")]
        all_skills.update(skills)
    if user.get("interests"):
        interests = [i.strip() for i in user.get("interests", "").split(",")]
        all_interests.update(interests)

selected_skills = st.sidebar.multiselect("🛠️ Filter by Skills", sorted(all_skills))
selected_interests = st.sidebar.multiselect("❤️ Filter by Interests", sorted(all_interests))

# Search functionality
search_query = st.sidebar.text_input("🔍 Search by name or keywords")

def filter_users(users, major_filter, year_filter, skills_filter, interests_filter, search_query):
    """Filter users based on criteria"""
    filtered = []

    for user in users:
        # Skip current user
        if user.get('id') == st.session_state.current_user.get('id'):
            continue

        # Major filter
        if major_filter != "All" and user.get("major") != major_filter:
            continue

        # Year filter
        if year_filter != "All" and user.get("year") != year_filter:
            continue

        # Skills filter
        if skills_filter:
            user_skills = [s.strip() for s in user.get("skills", "").split(",") if s.strip()]
            if not any(skill in user_skills for skill in skills_filter):
                continue

        # Interests filter
        if interests_filter:
            user_interests = [i.strip() for i in user.get("interests", "").split(",") if i.strip()]
            if not any(interest in user_interests for interest in interests_filter):
                continue

        # Search query filter
        if search_query:
            search_text = f"{user.get('name', '')} {user.get('major', '')} {user.get('skills', '')} {user.get('interests', '')}".lower()
            if search_query.lower() not in search_text:
                continue

        filtered.append(user)

    return filtered

# Apply filters
filtered_users = filter_users(users, selected_major, selected_year, selected_skills, selected_interests, search_query)

# Determine which users to show based on filters
if selected_major != "All" or selected_year != "All" or selected_skills or selected_interests or search_query:
    # Use filtered users if filters are active
    available_users = [u for u in filtered_users if u.get('id') != st.session_state.current_user.get('id') and u.get('id') not in st.session_state.viewed_users]
else:
    # Use all users if no filters are active
    current_user_id = st.session_state.current_user.get('id')
    available_users = [u for u in users if u.get('id') != current_user_id and u.get('id') not in st.session_state.viewed_users]

if not available_users:
    st.info("🎉 You've seen all available users! Check your matches below or adjust your filters.")
else:
    # Get current user to display
    if st.session_state.current_user_index >= len(available_users):
        st.session_state.current_user_index = 0

    user = available_users[st.session_state.current_user_index]

    # Center the user card
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # Display user profile
        st.markdown(f"""
        <div class="swipe-card">
            <div class="user-header">
                <h3>{user.get('name', 'Unknown')}</h3>
            </div>
            <div class="user-details">
                <p><strong>Major:</strong> {user.get('major', 'N/A')}</p>
                <p><strong>Year:</strong> {user.get('year', 'N/A')}</p>
                <p><strong>Skills:</strong> {user.get('skills', 'N/A')}</p>
                <p><strong>Interests:</strong> {user.get('interests', 'N/A')}</p>
            </div>
            <div class="x-factor">
                ✨ {user.get('x_factor', 'No special skill listed')}
            </div>
        </div>
        """, unsafe_allow_html=True)

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
    st.markdown('<div class="skill-card teach">', unsafe_allow_html=True)
    st.markdown("### 📚 Skills Available to Learn")
    # Loop through all users
    # Extract and display skills from 'can_teach' field
    # Format: "Python basics" by Yuvraj/Siddhika/Aaradhya (email)

    for user in users:
        if user.get('can_teach'):
            skills = user.get('can_teach', '').split(',')
            for skill in skills:
                st.write(f"• **{skill.strip()}** - {user.get('name')} ({user.get('email')})")
    st.markdown('</div>', unsafe_allow_html=True)

with col_learn:
    st.markdown('<div class="skill-card learn">', unsafe_allow_html=True)
    st.markdown("### 🎯 Skills People Want to Learn")
    # Loop through all users
    # Extract and display skills from 'wants_to_learn' field
    # Format: "Data Visualization" wanted by Yuvraj/Siddhika/Aaradhya

    for user in users:
        if user.get('wants_to_learn'):
            skills = user.get('wants_to_learn', '').split(',')
            for skill in skills:
                st.write(f"• **{skill.strip()}** - {user.get('name')}")
    st.markdown('</div>', unsafe_allow_html=True)
