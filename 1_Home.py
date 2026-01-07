import streamlit as st
from src.data_manager import load_users, load_listings
from src.ai_matcher import ai_assistant
import json
from streamlit_lottie import st_lottie

# Page config
st.set_page_config(page_title="Uni-Sync", page_icon="🤝", layout="wide")

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

# HERO SECTION
col1, col2 = st.columns([2, 1])
with col1:
    st.markdown("""
    <div style="padding: 3rem 0;">
        <h1 style="font-size: 4rem; margin-bottom: 1rem;">🤝 Uni-Sync</h1>
        <p style="font-size: 1.5rem; color: #666; margin-bottom: 2rem;">
            One campus. Endless connections.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick stats
    users = load_users()
    listings = load_listings()
    
    col1a, col2a, col3a = st.columns(3)
    with col1a:
        st.metric("👥 Active Students", len(users))
    with col2a:
        st.metric("🛠️ Skills Shared", sum(1 for u in users if u.get('can_teach')))
    with col3a:
        st.metric("🏠 Available Listings", len(listings))

with col2:
    # Lottie animation
    try:
        with open("assets/community.json") as f:
            anim = json.load(f)
        st_lottie(anim, height=300)
    except FileNotFoundError:
        st.info("🎨 Animation loading...")

# AI CHATBOT
st.markdown("---")
st.subheader("🤖 AI Campus Assistant")

with st.form("ai_chat_form"):
    user_query = st.text_input("Ask me anything: Find study buddies, skills, or campus resources...")
    submit_button = st.form_submit_button("Send")

if submit_button and user_query and user_query.strip():
    st.session_state.ai_chat_history.append({"role": "user", "content": user_query})
    with st.spinner("Thinking..."):
        ai_response = ai_assistant(user_query, users, listings)
        st.session_state.ai_chat_history.append({"role": "assistant", "content": ai_response})

for chat in st.session_state.ai_chat_history:
    if chat["role"] == "user":
        st.markdown(f"<div style='background: #e6f7ff; padding: 1rem; border-radius: 10px; margin: 0.5rem 0; text-align: right;'><b>You:</b> {chat['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div style='background: #f0f2f6; padding: 1rem; border-radius: 10px; margin: 0.5rem 0;'><b>AI Assistant:</b> {chat['content']}</div>", unsafe_allow_html=True)