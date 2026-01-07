import streamlit as st
from src.data_manager import load_users, load_listings, init_data
from src.ai_matcher import ai_assistant

# Initialize data
init_data()
import json
from streamlit_lottie import st_lottie

# Page config
st.set_page_config(
    page_title="Uni-Sync - Connect & Collaborate",
    page_icon="🤝",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize session state
if 'current_user' not in st.session_state:
    st.session_state.current_user = None
if 'ai_chat_history' not in st.session_state:
    st.session_state.ai_chat_history = []
if 'user_query_key' not in st.session_state:
    st.session_state.user_query_key = 0

# Custom CSS
try:
    with open("assets/style-home.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    pass

# Main content container
st.markdown('<div class="main-content">', unsafe_allow_html=True)

# HERO SECTION
col1, col2 = st.columns([2, 1])
with col1:
    st.markdown('<div class="hero-section">', unsafe_allow_html=True)
    st.markdown('<h1 class="hero-title">🤝 Uni-Sync</h1>', unsafe_allow_html=True)
    st.markdown('<p class="hero-subtitle">One campus. Endless connections.</p>', unsafe_allow_html=True)
    st.markdown('<p class="hero-description">Connect with fellow students, share skills, and find study partners. Uni-Sync helps you build meaningful relationships and academic collaborations within your university community.</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Quick stats
    users = load_users()
    listings = load_listings()

    st.markdown('<div class="stats-spacer"></div>', unsafe_allow_html=True)
    col1a, col2a, col3a = st.columns(3)
    with col1a:
        st.metric(
            label="👥 Active Students",
            value=len(users),
            delta=f"+{len(users)//10 if len(users) > 0 else 0} this week"
        )
    with col2a:
        skills_shared = sum(1 for u in users if u.get('can_teach'))
        st.metric(
            label="🛠️ Skills Shared",
            value=skills_shared,
            delta=f"+{skills_shared//8 if skills_shared > 0 else 0} this week"
        )
    with col3a:
        st.metric(
            label="🏠 Available Listings",
            value=len(listings),
            delta=f"+{len(listings)//5 if len(listings) > 0 else 0} this week"
        )

with col2:
    # Lottie animation
    try:
        with open("assets/community.json") as f:
            anim = json.load(f)
        st.markdown('<div class="animation-container">', unsafe_allow_html=True)
        st_lottie(anim, height=350, key="hero-animation")
        st.markdown('</div>', unsafe_allow_html=True)
    except FileNotFoundError:
        st.info("🎨 Community animation loading...")

# Divider
st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

# AI CHATBOT SECTION
st.markdown('<h2 class="section-title">🤖 AI Campus Assistant</h2>', unsafe_allow_html=True)
st.markdown('<p class="section-description">Need help finding study partners, resources, or campus information? Our AI assistant is here to help you navigate the university community.</p>', unsafe_allow_html=True)

with st.form("ai_chat_form"):
    user_query = st.text_input(
        "Ask me anything: Find study buddies, skills, or campus resources...",
        placeholder="e.g., 'Find someone to study calculus with' or 'Who can help me with Python?'",
        key="user_query_input"
    )
    submit_button = st.form_submit_button("🚀 Send Query", type="primary")

if submit_button and user_query and user_query.strip():
    st.session_state.ai_chat_history.append({"role": "user", "content": user_query})
    with st.spinner("🤖 Uni-Sync AI is thinking..."):
        ai_response = ai_assistant(user_query, users, listings)
        st.session_state.ai_chat_history.append({"role": "assistant", "content": ai_response})

# Display chat history
for chat in st.session_state.ai_chat_history:
    if chat["role"] == "user":
        st.markdown(f"<div class='chat-user'><b>You:</b> {chat['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='chat-assistant'><b>🤖 AI Assistant:</b> {chat['content']}</div>", unsafe_allow_html=True)

# Footer
st.markdown('</div>', unsafe_allow_html=True)  # Close main-content div
st.markdown('<footer><p>Made with ❤️ for the university community | Uni-Sync © 2024</p></footer>', unsafe_allow_html=True)