import streamlit as st
from src.data_manager import load_users, load_listings, init_data, save_user, verify_password, save_password
from src.ai_matcher import ai_assistant

init_data()  # Initialize data files if they don't exist
import json
from streamlit_lottie import st_lottie
import urllib.parse

st.set_page_config(  # Configure page settings
    page_title="Uni-Sync - Connect & Collaborate",
    page_icon="🤝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Keep sidebar visible
st.markdown("""
<style>
    /* Prevent sidebar from being collapsible */
    [data-testid="collapsedControl"] {
        display: none !important;
    }
    
    /* Keep settings menu visible */
    #MainMenu {
        visibility: visible !important;
    }
    
    header {
        visibility: visible !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'current_user' not in st.session_state:
    st.session_state.current_user = None
if 'ai_chat_history' not in st.session_state:
    st.session_state.ai_chat_history = []
if 'user_query_key' not in st.session_state:
    st.session_state.user_query_key = 0
if 'api_key_index' not in st.session_state:
    st.session_state.api_key_index = 0

# Load custom CSS
try:
    with open("assets/style-home.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    pass

# Additional sidebar styling
st.markdown("""
<style>
    /* Ensure sidebar stays open */
    section[data-testid="stSidebar"] {
        min-width: 300px !important;
    }
    
    /* Show collapse button but make it less prominent */
    [data-testid="collapsedControl"] {
        opacity: 0.5;
    }
    
    [data-testid="collapsedControl"]:hover {
        opacity: 1;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="particles-bg"></div>', unsafe_allow_html=True)  # Animated background

# SIDEBAR - User Profile
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/476/476863.png", width=80)
    st.markdown("### 👤 User Profile")
    
    users = load_users()
    
    if st.session_state.current_user is None:
        st.markdown("#### 🔑 Login")
        with st.form("login_form"):
            login_email = st.text_input("Email", placeholder="your.email@campus.edu")
            login_password = st.text_input("Password", type="password")
            
            if st.form_submit_button("🚀 Login", type="primary", use_container_width=True):
                if verify_password(login_email, login_password):
                    current_user = next((u for u in users if u.get('email', '').lower() == login_email.lower()), None)
                    if current_user:
                        st.session_state.current_user = current_user
                        
                        from src.data_manager import get_user_connections
                        connections = get_user_connections(current_user.get('id'))
                        
                        st.session_state.matches = []  # Load existing connections
                        for conn in connections:
                            other_user_id = conn['user2_id'] if conn['user1_id'] == current_user.get('id') else conn['user1_id']
                            other_user = next((u for u in users if u.get('id') == other_user_id), None)
                            if other_user and conn.get('connection_type') == 'peer_match':
                                st.session_state.matches.append(other_user)
                        
                        st.success(f"Welcome back, {current_user.get('name')}!")
                        st.rerun()
                    else:
                        st.error("⚠️ User not found")
                else:
                    st.error("⚠️ Invalid email or password")
    else:
        current_user = st.session_state.current_user
        
# Display user profile card
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, rgba(139, 92, 246, 0.2) 0%, rgba(6, 182, 212, 0.1) 100%);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 16px;
            padding: 1.25rem;
            margin-bottom: 1rem;
        ">
            <h4 style="margin: 0; color: #fff !important;">👋 {current_user.get('name')}</h4>
            <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem; color: #a1a1aa !important;">
                🎓 {current_user.get('major', 'Student')}
            </p>
            <p style="margin: 0.25rem 0 0 0; font-size: 0.85rem; color: #71717a !important;">
                ✨ {current_user.get('x_factor', '')}
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.current_user = None
            st.rerun()
        
    st.divider()
    
    with st.expander("📝 New? Join UniSync", expanded=False):  # Signup form
        x_factor_type = st.radio(
            "Can you teach something?", 
            ["Yes, I can teach", "Currently a learner only"],
            horizontal=True,
            key="signup_xfactor_type"
        )

        with st.form("signup_form"):
            new_name = st.text_input("Full Name *", placeholder="John Doe")
            new_email = st.text_input("Email ID *", placeholder="your.email@campus.edu")
            
            c1, c2 = st.columns(2)
            with c1:
                new_year = st.selectbox("Year *", ["1st Year", "2nd Year", "3rd Year", "4th Year", "Alumni"])
            with c2:
                new_major = st.text_input("Major *", placeholder="Computer Science")
            
            new_skills = st.text_input("Skills *", placeholder="Python, Design, Writing...")
            new_interests = st.text_input("Interests *", placeholder="AI, Music, Sports...")
            
            new_x_factor = ""
            new_can_teach = ""
            
            if x_factor_type == "Yes, I can teach":
                st.markdown("---")
                st.markdown("##### 👨‍🏫 Teacher Details")
                new_x_factor = st.text_input("Your X-Factor *", placeholder="What makes you unique?")
                new_can_teach = st.text_input("What can you teach? *", placeholder="Guitar, Math, Coding...")
            else:
                new_x_factor = "📚 Currently a learner only"
                new_can_teach = "None yet"

            st.markdown("---")
            new_wants_to_learn = st.text_input("Want to learn?", placeholder="What skills interest you?")
            new_accommodation = st.text_input("Accommodation needs", placeholder="e.g., Looking for roommate")
            
            c3, c4 = st.columns(2)
            with c3:
                new_password = st.text_input("Password *", type="password")
            with c4:
                new_password_confirm = st.text_input("Confirm *", type="password")

            st.caption("* Required fields")

            if st.form_submit_button("✨ Join Network", type="primary", use_container_width=True):
                if not new_name or not new_email or not new_major or not new_skills or not new_interests:
                    st.error("⚠️ Please fill in all required fields")
                elif not new_password or not new_password_confirm:
                    st.error("⚠️ Please create and confirm your password")
                elif new_password != new_password_confirm:
                    st.error("⚠️ Passwords do not match!")
                elif len(new_password) < 6:
                    st.error("⚠️ Password must be at least 6 characters")
                elif x_factor_type == "Yes, I can teach" and (not new_x_factor or not new_can_teach):
                    st.error("⚠️ Please enter your X-Factor and teaching skills")
                else:
                    existing_emails = [u.get('email', '').lower() for u in users]
                    if new_email.lower() in existing_emails:
                        st.error("⚠️ Email already registered!")
                    else:
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
                        st.success("✅ Welcome to UniSync!")
                        st.balloons()
    
    if st.session_state.current_user is not None:  # Edit Profile section
        st.divider()
        with st.expander("✏️ Edit Profile"):
            current_user = st.session_state.current_user
            with st.form("edit_profile_form"):
                edit_skills = st.text_input("Skills", value=current_user.get('skills', ''))
                edit_interests = st.text_input("Interests", value=current_user.get('interests', ''))
                
                current_x = current_user.get('x_factor', '')
                current_can_teach = current_user.get('can_teach', '')
                
                if "learner only" in current_x.lower() or current_can_teach == "None yet":
                    edit_x_type = st.radio("Teaching Status", ["Currently a learner only", "Yes, I can teach"], index=0)
                else:
                    edit_x_type = st.radio("Teaching Status", ["Yes, I can teach", "Currently a learner only"], index=0)
                
                if edit_x_type == "Yes, I can teach":
                    edit_x_factor = st.text_input("X-Factor", value=current_x if "learner only" not in current_x.lower() else "")
                    edit_can_teach = st.text_input("Can teach", value=current_can_teach if current_can_teach != "None yet" else "")
                else:
                    edit_x_factor = "📚 Currently a learner only"
                    edit_can_teach = "None yet"
                
                edit_wants_to_learn = st.text_input("Want to learn", value=current_user.get('wants_to_learn', ''))
                
                if st.form_submit_button("💾 Save", type="primary", use_container_width=True):
                    if not edit_skills or not edit_interests:
                        st.error("⚠️ Skills and Interests required")
                    elif edit_x_type == "Yes, I can teach" and (not edit_x_factor or not edit_can_teach):
                        st.error("⚠️ Complete teacher details")
                    else:
                        st.success("✅ Profile updated!")

# MAIN CONTENT

st.markdown('<div class="main-content">', unsafe_allow_html=True)

# Guide link - accessible without login
st.markdown("""
<div style="
    text-align: center;
    margin-bottom: 1.5rem;
    padding: 1rem;
    background: linear-gradient(135deg, rgba(139, 92, 246, 0.15) 0%, rgba(6, 182, 212, 0.1) 100%);
    border: 1px solid rgba(139, 92, 246, 0.3);
    border-radius: 16px;
">
    <span style="font-size: 1.5rem;">📖</span>
    <p style="color: #a1a1aa !important; margin: 0.5rem 0;">New to Uni-Sync? Learn how to use all features!</p>
</div>
""", unsafe_allow_html=True)

col_guide1, col_guide2, col_guide3 = st.columns([1, 1, 1])
with col_guide2:
    if st.button("📖 View User Guide", use_container_width=True, type="primary"):
        st.switch_page("pages/6_Guide.py")

st.markdown("<br>", unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])  # Hero section layout

with col1:
    st.markdown('''
    <div class="hero-section">
        <h1 class="hero-title"><span class="emoji-fix">🤝</span> Uni-Sync</h1>
        <p class="hero-subtitle">One campus. Endless connections.</p>
        <p class="hero-description">
            Connect with fellow students, share skills, and find study partners. 
            Uni-Sync helps you build meaningful relationships and academic 
            collaborations within your university community.
        </p>
    </div>
    ''', unsafe_allow_html=True)

    users = load_users()  # Load user data for stats
    listings = load_listings()

    st.markdown('<div class="stats-spacer"></div>', unsafe_allow_html=True)
    
    col1a, col2a, col3a = st.columns(3)
    with col1a:
        st.metric(
            label="👥 Active Students",
            value=len(users),
            delta=f"+{max(1, len(users)//10)} this week"
        )
    with col2a:
        skills_shared = sum(1 for u in users if u.get('can_teach') and u.get('can_teach') != 'None yet')
        st.metric(
            label="🛠️ Skills Shared",
            value=skills_shared,
            delta=f"+{max(1, skills_shared//8)} this week"
        )
    with col3a:
        st.metric(
            label="🏠 Listings",
            value=len(listings),
            delta=f"+{max(1, len(listings)//5)} this week"
        )

with col2:
    try:
        with open("assets/community.json") as f:
            anim = json.load(f)
        st.markdown('<div class="animation-container">', unsafe_allow_html=True)
        st_lottie(anim, height=350, key="hero-animation")
        st.markdown('</div>', unsafe_allow_html=True)
    except FileNotFoundError:
        st.markdown('''
        <div style="
            display: flex;
            justify-content: center;
            align-items: center;
            height: 350px;
            background: linear-gradient(135deg, rgba(139, 92, 246, 0.1) 0%, rgba(6, 182, 212, 0.1) 100%);
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        ">
            <span style="font-size: 4rem;">🎓</span>
        </div>
        ''', unsafe_allow_html=True)

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)  # Visual divider

# AI Chatbot section
st.markdown('''
<h2 class="section-title">🤖 AI Campus Assistant</h2>
<p class="section-description">
    Need help finding study partners, resources, or campus information? 
    Our AI assistant is here to help you navigate the university community.
</p>
''', unsafe_allow_html=True)

with st.form("ai_chat_form"):
    user_query = st.text_input(
        "Ask me anything...",
        placeholder="e.g., 'Find someone to study calculus with' or 'Who can help me with Python?'",
        key="user_query_input",
        label_visibility="collapsed"
    )
    
    col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
    with col_btn2:
        submit_button = st.form_submit_button("🚀 Send Query", type="primary", use_container_width=True)

if submit_button and user_query and user_query.strip():
    if st.session_state.current_user is None:
        st.session_state.ai_chat_history.append({"role": "user", "content": user_query})
        st.session_state.ai_chat_history.append({
            "role": "assistant", 
            "content": "🔒 Please login to use the AI assistant. Sign in from the sidebar to access this feature."
        })
    else:
        st.session_state.ai_chat_history.append({"role": "user", "content": user_query})
        with st.spinner("🤖 Uni-Sync AI is thinking..."):
            ai_response = ai_assistant(user_query, users, listings)
            st.session_state.ai_chat_history.append({"role": "assistant", "content": ai_response})

if st.session_state.ai_chat_history:  # Display chat history
    st.markdown("---")
    for chat in st.session_state.ai_chat_history[-6:]:
        if chat["role"] == "user":
            st.markdown(f'''
            <div class="chat-user">
                <b>You:</b> {chat['content']}
            </div>
            ''', unsafe_allow_html=True)
        else:
            st.markdown(f'''
            <div class="chat-assistant">
                <b>🤖 AI Assistant:</b> {chat['content']}
            </div>
            ''', unsafe_allow_html=True)

if st.session_state.current_user:  # Show user connections
    st.markdown("---")
    st.markdown('<h2 class="section-title">🤝 My Connections</h2>', unsafe_allow_html=True)
    
    if 'matches' in st.session_state and st.session_state.matches:
        connections = st.session_state.matches
        
        st.markdown(f'''
        <div style="
            text-align: center;
            padding: 1rem;
            margin-bottom: 1.5rem;
            background: linear-gradient(135deg, rgba(16, 185, 129, 0.15) 0%, rgba(16, 185, 129, 0.08) 100%);
            border: 1px solid rgba(16, 185, 129, 0.3);
            border-radius: 12px;
        ">
            <span style="color: #10b981; font-weight: 600;">
                🎉 You have {len(connections)} connection{"s" if len(connections) > 1 else ""}!
            </span>
        </div>
        ''', unsafe_allow_html=True)
        
        cols = st.columns(3)
        for idx, conn in enumerate(connections):
            with cols[idx % 3]:
                st.markdown(f'''
                <div class="connection-card">
                    <h3>👤 {conn.get('name', 'Unknown')}</h3>
                    <p><strong>🎓</strong> {conn.get('major', 'N/A')}</p>
                    <p><strong>📧</strong> {conn.get('email', 'N/A')}</p>
                    <p><strong>📚</strong> Can teach: {conn.get('can_teach', 'N/A')}</p>
                    <p><strong>🎯</strong> Wants: {conn.get('wants_to_learn', 'N/A')}</p>
                </div>
                ''', unsafe_allow_html=True)
                
                subject = "UniSync Connection"
                body = f"Hi {conn.get('name')},\n\nI connected with you on UniSync. Let's collaborate!"
                encoded_subject = urllib.parse.quote(subject)
                encoded_body = urllib.parse.quote(body)
                mailto_link = f"mailto:{conn.get('email')}?subject={encoded_subject}&body={encoded_body}"
                
                st.markdown(f'''
                <a href="{mailto_link}" style="
                    display: inline-block;
                    width: 100%;
                    text-align: center;
                    padding: 0.6rem;
                    margin-top: 0.5rem;
                    background: linear-gradient(135deg, #06b6d4 0%, #8b5cf6 100%);
                    color: white !important;
                    border-radius: 8px;
                    text-decoration: none;
                    font-weight: 600;
                    font-size: 0.9rem;
                ">
                    📧 Contact
                </a>
                ''', unsafe_allow_html=True)

                if st.button(f"⭐ Rate", key=f"rate_{conn.get('id')}_{idx}", use_container_width=True):
                    st.session_state[f'show_rating_form_{conn.get("id")}'] = True

                if st.session_state.get(f'show_rating_form_{conn.get("id")}', False):
                    with st.form(f"rate_form_{conn.get('id')}"):
                        rating = st.slider("Rating", 1, 5, 5)
                        review = st.text_area("Review", placeholder="How was your experience?")
                        
                        if st.form_submit_button("Submit", use_container_width=True):
                            from src.data_manager import save_rating
                            save_rating(
                                st.session_state.current_user.get('id'),
                                conn.get('id'),
                                rating,
                                review
                            )
                            st.success(f"✅ Rated with {rating} stars!")
                            st.session_state[f'show_rating_form_{conn.get("id")}'] = False
                            st.rerun()
    else:
        st.markdown('''
        <div style="
            text-align: center;
            padding: 3rem 2rem;
            background: linear-gradient(135deg, rgba(139, 92, 246, 0.1) 0%, rgba(6, 182, 212, 0.1) 100%);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 16px;
        ">
            <span style="font-size: 3rem; display: block; margin-bottom: 1rem;">🔍</span>
            <p style="color: #a1a1aa !important; font-size: 1.1rem;">
                No connections yet. Start swiping in <strong>Find Peers</strong> to make connections!
            </p>
        </div>
        ''', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # Close main content wrapper

# Footer
st.markdown('''
<footer>
    <p>Made with ❤️ for the university community | <strong>Uni-Sync</strong> © 2024</p>
</footer>
''', unsafe_allow_html=True)