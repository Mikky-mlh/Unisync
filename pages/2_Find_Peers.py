import streamlit as st
import sys
import os
import html

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  # Add parent directory to path

from src.data_manager import load_users
from src.utils import calculate_compatibility
import pandas as pd

st.set_page_config(page_title="Find Peers", page_icon="👥", layout="wide")  # Configure page

if 'current_user' not in st.session_state or st.session_state.current_user is None:  # Check authentication
    st.warning("🔒 Please login from the Home page to access Find Peers")
    st.stop()

try:  # Load custom CSS
    with open("assets/style-peer.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except:
    pass

# Initialize session state variables
if 'viewed_users' not in st.session_state:
    st.session_state.viewed_users = []
if 'matches' not in st.session_state:
    st.session_state.matches = []
if 'current_user_index' not in st.session_state:
    st.session_state.current_user_index = 0

users = load_users()  # Load all users from database

st.title("👥 Campus Tribe - Find Your People")  # Page title
st.markdown("### Swipe to connect with fellow students")

col_title, col_reset = st.columns([3, 1])  # Layout with reset button
with col_reset:
    if st.session_state.viewed_users:
        if st.button("🔄 Reset", help="Review all users again", use_container_width=True):
            st.session_state.viewed_users = []
            st.session_state.current_user_index = 0
            st.rerun()

st.sidebar.markdown("---")  # Sidebar divider
st.sidebar.subheader("🔍 Advanced Search")

all_majors = ["All"] + sorted(set(u.get("major", "") for u in users if u.get("major")))  # Get unique majors
all_years = ["All"] + sorted(set(u.get("year", "") for u in users if u.get("year")))

selected_major = st.sidebar.selectbox("🎓 Filter by Major", all_majors)  # Major filter UI
selected_year = st.sidebar.selectbox("📅 Filter by Year", all_years)

all_skills = set()  # Collect all unique skills
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

search_query = st.sidebar.text_input("🔍 Search by name or keywords")  # Search input

def filter_users(users, major_filter, year_filter, skills_filter, interests_filter, search_query):  # Apply all filters
    filtered = []

    for user in users:
        if user.get('id') == st.session_state.current_user.get('id'):
            continue

        if major_filter != "All" and user.get("major") != major_filter:
            continue

        if year_filter != "All" and user.get("year") != year_filter:
            continue

        if skills_filter:
            user_skills = [s.strip() for s in user.get("skills", "").split(",") if s.strip()]
            if not any(skill in user_skills for skill in skills_filter):
                continue

        if interests_filter:
            user_interests = [i.strip() for i in user.get("interests", "").split(",") if i.strip()]
            if not any(interest in user_interests for interest in interests_filter):
                continue

        if search_query:
            search_text = f"{user.get('name', '')} {user.get('major', '')} {user.get('skills', '')} {user.get('interests', '')}".lower()
            if search_query.lower() not in search_text:
                continue

        filtered.append(user)

    return filtered

filtered_users = filter_users(users, selected_major, selected_year, selected_skills, selected_interests, search_query)  # Get filtered results

if selected_major != "All" or selected_year != "All" or selected_skills or selected_interests or search_query:  # Determine which users to show
    available_users = [u for u in filtered_users if u.get('id') != st.session_state.current_user.get('id') and u.get('id') not in st.session_state.viewed_users]
else:
    current_user_id = st.session_state.current_user.get('id')
    available_users = [u for u in users if u.get('id') != current_user_id and u.get('id') not in st.session_state.viewed_users]

if not available_users:
    st.info("🎉 You've seen all available users! Check your matches below or adjust your filters.")
    
    if st.session_state.viewed_users:
        st.markdown("<div style='text-align: center; margin: 2rem 0;'>", unsafe_allow_html=True)
        if st.button("🔄 Review Passed Users", use_container_width=False, type="primary"):
            st.session_state.viewed_users = []
            st.session_state.current_user_index = 0
            st.success("✨ Showing all users again! Give them another chance.")
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
else:
    if st.session_state.current_user_index >= len(available_users):
        st.session_state.current_user_index = 0

    user = available_users[st.session_state.current_user_index]

    from src.data_manager import get_user_rating
    avg_rating, num_ratings = get_user_rating(user.get('id'))

    col1, col2, col3 = st.columns([1, 2, 1])  # Center the user card
    with col2:
        # Clean up X-factor display
        x_factor = user.get('x_factor', 'Discovering their unique skill...')
        x_factor_clean = x_factor.replace('"', '').replace("'", "").replace("`", "").strip()
        if not x_factor_clean or x_factor_clean.lower() == "none":
            x_factor_clean = "Discovering their unique skill..."
        
        # Display user profile
        st.markdown(f"""
        <div class="swipe-card">
            <div class="user-header">
                <h3>{html.escape(user.get('name', 'Unknown'))}</h3>
                <p style="color: #f59e0b; font-size: 1.2rem;">
                    {'⭐' * int(avg_rating)} {avg_rating}/5.0 ({num_ratings} ratings)
                </p>
            </div>
            <div class="user-details">
                <p><strong>Major:</strong> {html.escape(user.get('major', 'N/A'))}</p>
                <p><strong>Year:</strong> {html.escape(user.get('year', 'N/A'))}</p>
                <p><strong>Skills:</strong> {html.escape(user.get('skills', 'N/A'))}</p>
                <p><strong>Interests:</strong> {html.escape(user.get('interests', 'N/A'))}</p>
            </div>
            <div class="x-factor">
                ✨ {html.escape(x_factor_clean)}
            </div>
        </div>
        """, unsafe_allow_html=True)

        col_left, col_right = st.columns(2)  # Swipe action buttons
        with col_left:
            if st.button("👎 Pass", use_container_width=True, key=f"pass_{user.get('id')}"):
                st.session_state.viewed_users.append(user.get('id'))
                st.session_state.current_user_index += 1
                st.rerun()

        with col_right:
            already_connected = any(m.get('id') == user.get('id') for m in st.session_state.matches)
            
            if already_connected:
                st.button("✅ Already Connected", use_container_width=True, disabled=True, key=f"connected_{user.get('id')}")
            elif st.button("👍 Connect", use_container_width=True, key=f"connect_{user.get('id')}"):
                from src.data_manager import save_connection
                
                save_connection(
                    st.session_state.current_user.get('id'),
                    user.get('id'),
                    'peer_match'
                )
                
                st.session_state.matches.append(user)
                st.session_state.viewed_users.append(user.get('id'))
                st.session_state.current_user_index += 1
                st.success(f"✅ Connected with {user.get('name')}!")
                st.rerun()

st.markdown("---")  # Section divider
st.subheader("🎓 Your Study Buddy Matches")

if st.session_state.matches:
    st.success(f"You have {len(st.session_state.matches)} matches!")

    for match in st.session_state.matches:  # Display each match
        with st.expander(f"👤 {match.get('name', 'Unknown')}"):
            st.write(f"**Email:** {match.get('email', 'N/A')}")
            st.write(f"**Major:** {match.get('major', 'N/A')}")
            st.write(f"**Can teach:** {match.get('can_teach', 'N/A')}")
            st.write(f"**Wants to learn:** {match.get('wants_to_learn', 'N/A')}")
else:
    st.info("No matches yet. Start swiping to find your study buddies!")

st.markdown("---")  # Section divider
st.subheader("🔄 Skill Exchange Marketplace")
st.caption("Connect with students to learn new skills or teach what you know")

col_teach, col_learn = st.columns(2)  # Two column layout

with col_teach:
    st.markdown('<div class="skill-card teach">', unsafe_allow_html=True)
    st.markdown("### 📚 Skills Available to Learn")
    
    for user in users:
        if user.get('can_teach'):
            skills = user.get('can_teach', '').split(',')
            for skill in skills:
                st.write(f"• **{skill.strip()}** - {user.get('name')} ({user.get('email')})")
    st.markdown('</div>', unsafe_allow_html=True)

with col_learn:
    st.markdown('<div class="skill-card learn">', unsafe_allow_html=True)
    st.markdown("### 🎯 Skills People Want to Learn")
    
    for user in users:
        if user.get('wants_to_learn'):
            skills = user.get('wants_to_learn', '').split(',')
            for skill in skills:
                st.write(f"• **{skill.strip()}** - {user.get('name')}")
    st.markdown('</div>', unsafe_allow_html=True)
