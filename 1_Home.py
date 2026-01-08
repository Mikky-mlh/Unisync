import streamlit as st
from src.data_manager import load_users, load_listings, init_data, save_user, verify_password, save_password
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
    initial_sidebar_state="expanded"
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

# SIDEBAR - User Profile
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/476/476863.png", width=80)
    st.title("👤 User Profile")
    
    # Simple Login System
    users = load_users()
    
    # Login Form
    if st.session_state.current_user is None:
        st.subheader("🔑 Login")
        with st.form("login_form"):
            login_email = st.text_input("Email")
            login_password = st.text_input("Password", type="password")
            
            if st.form_submit_button("🚀 Login", type="primary"):
                if verify_password(login_email, login_password):
                    # Find user by email
                    current_user = next((u for u in users if u.get('email', '').lower() == login_email.lower()), None)
                    if current_user:
                        st.session_state.current_user = current_user
                        st.success(f"Welcome back, {current_user.get('name')}!")
                        st.rerun()
                    else:
                        st.error("⚠️ User not found")
                else:
                    st.error("⚠️ Invalid email or password")
    else:
        # Show logged-in user info
        current_user = st.session_state.current_user
        st.success(f"Welcome, {current_user.get('name')}!")
        st.caption(f"🎓 {current_user.get('major', 'Student')}")
        st.caption(f"✨ {current_user.get('x_factor', '')}")
        
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.current_user = None
            st.rerun()
        
    st.divider()
    
    # "Join Now" Expander
    with st.expander("📝 New? Join UniSync"):
        # STEP 1: Put the decision OUTSIDE the form so it updates instantly
        x_factor_type = st.radio(
            "Can you teach something?", 
            ["Yes, I can teach", "Currently a learner only"],
            horizontal=True
        )

        # STEP 2: Start the form
        with st.form("signup_form"):
            new_name = st.text_input("Full Name *")
            new_email = st.text_input("Email ID *", placeholder="your.email@campus.edu")
            
            c1, c2 = st.columns(2)
            with c1:
                new_year = st.selectbox("Year *", ["1st Year", "2nd Year", "3rd Year", "4th Year", "Alumni"])
            with c2:
                new_major = st.text_input("Major *")
            
            new_skills = st.text_input("Skills (comma separated) *")
            new_interests = st.text_input("Interests (comma separated) *")
            
            # STEP 3: Conditionally show fields based on the outside selection
            new_x_factor = ""
            new_can_teach = ""
            
            if x_factor_type == "Yes, I can teach":
                st.markdown("---")
                st.markdown("### 👨‍🏫 Teacher Details")
                new_x_factor = st.text_input("Your X-Factor (What makes you unique?) *")
                new_can_teach = st.text_input("What can you teach? (comma separated) *")
            else:
                # Set default values for learners so logic doesn't break
                new_x_factor = "📚 Currently a learner only"
                new_can_teach = "None yet"

            st.markdown("---")
            new_wants_to_learn = st.text_input("What do you want to learn? (comma separated)")
            new_accommodation = st.text_input("Accommodation needs (optional)", placeholder="e.g., Looking for roommate")
            
            c3, c4 = st.columns(2)
            with c3:
                new_password = st.text_input("Create Password *", type="password")
            with c4:
                new_password_confirm = st.text_input("Confirm Password *", type="password")

            st.caption("* Required fields")

            # STEP 4: Submit Logic
            if st.form_submit_button("Join Network", type="primary"):
                # Validate all required fields
                if not new_name or not new_email or not new_major or not new_skills or not new_interests:
                    st.error("⚠️ Please fill in all required fields")
                elif not new_password or not new_password_confirm:
                    st.error("⚠️ Please create and confirm your password")
                elif new_password != new_password_confirm:
                    st.error("⚠️ Passwords do not match!")
                elif len(new_password) < 6:
                    st.error("⚠️ Password must be at least 6 characters long")
                # Only validate X-Factor if they claimed to be a teacher
                elif x_factor_type == "Yes, I can teach" and (not new_x_factor or not new_can_teach):
                    st.error("⚠️ Please enter your X-Factor and what you can teach")
                else:
                    # Check if email already exists
                    existing_emails = [u.get('email', '').lower() for u in users]
                    if new_email.lower() in existing_emails:
                        st.error("⚠️ This email is already registered! Please use a different email or sign in.")
                    else:
                        # Create user dict matching CSV structure
                        new_user = {
                            "id": len(users) + 1,
                            "name": new_name,
                            "email": new_email,
                            "year": new_year,
                            "major": new_major,
                            "skills": new_skills,
                            "interests": new_interests,
                            "x_factor": new_x_factor,
                            "can_teach": new_can_teach,
                            "wants_to_learn": new_wants_to_learn if new_wants_to_learn else "Open to learning",
                            "accommodation_need": new_accommodation if new_accommodation else "None"
                        }
                        save_user(new_user)
                        save_password(new_email, new_password)
                        st.success("✅ Welcome to UniSync! You can now login with your credentials.")
                        st.balloons()
    
    # Edit Profile for logged-in users
    if st.session_state.current_user is not None:
        st.divider()
        with st.expander("✏️ Edit My Profile"):
            current_user = st.session_state.current_user
            with st.form("edit_profile_form"):
                edit_skills = st.text_input("Update Skills", value=current_user.get('skills', ''))
                edit_interests = st.text_input("Update Interests", value=current_user.get('interests', ''))
                
                # X-Factor edit with learner-only option
                current_x = current_user.get('x_factor', '')
                current_can_teach = current_user.get('can_teach', '')
                
                if "learner only" in current_x.lower() or current_can_teach == "None yet":
                    edit_x_type = st.radio("Teaching Status", ["Currently a learner only", "Yes, I can teach"], index=0)
                else:
                    edit_x_type = st.radio("Teaching Status", ["Yes, I can teach", "Currently a learner only"], index=0)
                
                if edit_x_type == "Yes, I can teach":
                    edit_x_factor = st.text_input("Your X-Factor", value=current_x if "learner only" not in current_x.lower() else "")
                    edit_can_teach = st.text_input("What can you teach?", value=current_can_teach if current_can_teach != "None yet" else "")
                else:
                    edit_x_factor = "📚 Currently a learner only"
                    edit_can_teach = "None yet"
                
                edit_wants_to_learn = st.text_input("What do you want to learn?", value=current_user.get('wants_to_learn', ''))
                
                if st.form_submit_button("💾 Save Changes", type="primary"):
                    if not edit_skills or not edit_interests:
                        st.error("⚠️ Skills and Interests cannot be empty")
                    elif edit_x_type == "Yes, I can teach" and (not edit_x_factor or not edit_can_teach):
                        st.error("⚠️ Please enter your X-Factor and what you can teach")
                    else:
                        st.success("✅ Profile updated! (In full app, this would update the CSV)")
                        st.info("💡 Refresh the page to see changes")

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

# MY CONNECTIONS SECTION
if st.session_state.current_user:
    st.markdown("---")
    st.markdown('<h2 class="section-title">🤝 My Connections</h2>', unsafe_allow_html=True)
    
    # Get connections from session state (matches from Find Peers)
    if 'matches' in st.session_state and st.session_state.matches:
        connections = st.session_state.matches
        st.success(f"You have {len(connections)} connections!")
        
        cols = st.columns(3)
        for idx, conn in enumerate(connections):
            with cols[idx % 3]:
                st.markdown(f"""
                <div style="
                    border: 2px solid #4f46e5;
                    border-radius: 15px;
                    padding: 1.5rem;
                    margin-bottom: 1rem;
                    background: rgba(79, 70, 229, 0.1);
                ">
                    <h3>👤 {conn.get('name', 'Unknown')}</h3>
                    <p><strong>🎓 Major:</strong> {conn.get('major', 'N/A')}</p>
                    <p><strong>📧 Email:</strong> {conn.get('email', 'N/A')}</p>
                    <p><strong>📚 Can teach:</strong> {conn.get('can_teach', 'N/A')}</p>
                    <p><strong>🎯 Wants to learn:</strong> {conn.get('wants_to_learn', 'N/A')}</p>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"📧 Email {conn.get('name')}", key=f"email_{conn.get('id')}", use_container_width=True):
                    st.info(f"mailto:{conn.get('email')}")
    else:
        st.info("👉 No connections yet. Start swiping in Find Peers to make connections!")

# Footer
st.markdown('</div>', unsafe_allow_html=True)  # Close main-content div
st.markdown('<footer><p>Made with ❤️ for the university community | Uni-Sync © 2024</p></footer>', unsafe_allow_html=True)
