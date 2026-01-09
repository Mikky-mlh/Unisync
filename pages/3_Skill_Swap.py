import streamlit as st
import sys
import os
from datetime import datetime, timedelta
import random
import urllib.parse

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  # Add parent directory to path

from src.data_manager import load_users

st.set_page_config(  # Configure page settings
    page_title="Skill Swap - Uni-Sync",
    page_icon="🔄",
    layout="wide"
)

try:  # Load custom CSS
    with open("assets/style-skill.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except:
    pass

# Helper function to create skill card HTML
def skill_card(cat, skill_category, skill_level, type_emoji, skill_name, skill_description, skill_user, type_label):
    return f"""<div style="background: rgba(30, 30, 45, 0.7); backdrop-filter: blur(16px); border: 1px solid rgba(255, 255, 255, 0.12); border-top: 3px solid {cat['color']}; border-radius: 20px; padding: 1.5rem; margin-bottom: 1rem;">
<div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.75rem;">
<span class="category-badge {skill_category}">{cat['icon']} {cat['name']}</span>
<span class="level-badge {skill_level}">{skill_level.upper()}</span></div>
<h4 style="color: white !important; font-size: 1.15rem; margin-bottom: 0.5rem;">{type_emoji} {skill_name}</h4>
<p style="color: #a1a1aa !important; font-size: 0.9rem; margin-bottom: 1rem;">{skill_description[:100]}{'...' if len(skill_description) > 100 else ''}</p>
<div style="display: flex; justify-content: space-between; padding-top: 0.75rem; border-top: 1px solid rgba(255, 255, 255, 0.08);">
<span style="color: #71717a !important; font-size: 0.85rem;">👤 {skill_user} • {type_label}</span></div></div>"""

if 'current_user' not in st.session_state or st.session_state.current_user is None:  # Check authentication
    st.markdown("""
    <div style="
        text-align: center;
        padding: 4rem 2rem;
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.15) 0%, rgba(245, 158, 11, 0.08) 100%);
        border: 1px solid rgba(245, 158, 11, 0.3);
        border-radius: 20px;
        margin: 2rem auto;
        max-width: 500px;
    ">
        <span style="font-size: 4rem; display: block; margin-bottom: 1rem;">🔒</span>
        <h2 style="color: #f59e0b !important; margin-bottom: 0.75rem;">Login Required</h2>
        <p style="color: #a1a1aa !important;">Please login from the Home page to access Skill Swap</p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

users = load_users()  # Load all users
current_user = st.session_state.current_user

# Initialize skill offerings in session state
if 'skill_offerings' not in st.session_state:
    st.session_state.skill_offerings = []
    
    for user in users:
        name = user.get('name')
        
        can_teach = user.get('can_teach', '')
        if can_teach and can_teach.lower() not in ['none', 'none yet', '']:
            for skill in can_teach.split(','):
                skill = skill.strip()
                if skill:
                    skill_lower = skill.lower()
                    if any(x in skill_lower for x in ['python', 'java', 'web', 'data', 'programming', 'matlab', 'cad', 'solidworks', 'embedded']):
                        category = 'tech'
                    elif any(x in skill_lower for x in ['guitar', 'music', 'singing', 'piano']):
                        category = 'music'
                    elif any(x in skill_lower for x in ['design', 'art', 'figma', 'photography', 'sketching']):
                        category = 'art'
                    elif any(x in skill_lower for x in ['calculus', 'statistics', 'chemistry', 'tutoring', 'math']):
                        category = 'academic'
                    elif any(x in skill_lower for x in ['spanish', 'language']):
                        category = 'language'
                    else:
                        category = 'other'
                    
                    st.session_state.skill_offerings.append({
                        'user': name,
                        'skill': skill,
                        'category': category,
                        'level': 'intermediate',
                        'type': 'teach',
                        'description': f"{name} can teach {skill}",
                        'email': user.get('email')
                    })
        
        wants_to_learn = user.get('wants_to_learn', '')
        if wants_to_learn and wants_to_learn.lower() not in ['none', 'open to learning', '']:
            for skill in wants_to_learn.split(','):
                skill = skill.strip()
                if skill:
                    skill_lower = skill.lower()
                    if any(x in skill_lower for x in ['python', 'java', 'web', 'data', 'programming', 'matlab', 'ai', 'machine learning', 'cloud', 'backend', 'react']):
                        category = 'tech'
                    elif any(x in skill_lower for x in ['music', 'production']):
                        category = 'music'
                    elif any(x in skill_lower for x in ['design', 'ui/ux']):
                        category = 'art'
                    elif any(x in skill_lower for x in ['calculus', 'math', 'leadership']):
                        category = 'academic'
                    elif any(x in skill_lower for x in ['spanish', 'language']):
                        category = 'language'
                    else:
                        category = 'other'
                    
                    st.session_state.skill_offerings.append({
                        'user': name,
                        'skill': skill,
                        'category': category,
                        'level': 'beginner',
                        'type': 'learn',
                        'description': f"{name} wants to learn {skill}",
                        'email': user.get('email')
                    })

if 'recent_exchanges' not in st.session_state:
    st.session_state.recent_exchanges = [
        {"user1": "Yuvraj Sarathe", "user2": "Siddhika Dhanelia", "skill1": "Python", "skill2": "Figma design", "time": "2 hours ago"},
        {"user1": "Rohan Gupta", "user2": "Aaradhya Tiwari", "skill1": "Calculus", "skill2": "Data Visualization", "time": "5 hours ago"},
        {"user1": "Karan Mehta", "user2": "Priya Reddy", "skill1": "Guitar", "skill2": "Android development", "time": "1 day ago"},
    ]

# Page header
st.markdown("""
<div style="text-align: center; margin-bottom: 0.5rem;">
    <h1><span class="emoji-fix">🔄</span> Skill Swap</h1>
</div>
""", unsafe_allow_html=True)

# Hero section with description
st.markdown("""
<div class="hero-swap">
    <div class="hero-icon">🔄</div>
    <h2 class="hero-title">Exchange Knowledge, Grow Together</h2>
    <p class="hero-subtitle">
        Share what you know, learn what you don't. Connect with peers for skill exchanges 
        that help everyone level up. Teaching is the best way to learn!
    </p>
</div>
""", unsafe_allow_html=True)

# Calculate and display statistics
total_skills = len(st.session_state.skill_offerings)
skills_to_teach = len([s for s in st.session_state.skill_offerings if s['type'] == 'teach'])
skills_to_learn = len([s for s in st.session_state.skill_offerings if s['type'] == 'learn'])
total_exchanges = len(st.session_state.recent_exchanges)
active_swappers = len(set([s['user'] for s in st.session_state.skill_offerings]))

st.markdown(f"""
<div class="exchange-stats">
    <div class="stat-card">
        <div class="stat-icon">📚</div>
        <div class="stat-value">{total_skills}</div>
        <div class="stat-label">Skills Listed</div>
    </div>
    <div class="stat-card">
        <div class="stat-icon">🎓</div>
        <div class="stat-value">{skills_to_teach}</div>
        <div class="stat-label">Teachers Ready</div>
    </div>
    <div class="stat-card">
        <div class="stat-icon">🌱</div>
        <div class="stat-value">{skills_to_learn}</div>
        <div class="stat-label">Learners Seeking</div>
    </div>
    <div class="stat-card">
        <div class="stat-icon">🤝</div>
        <div class="stat-value">{total_exchanges}</div>
        <div class="stat-label">Exchanges Made</div>
    </div>
</div>
""", unsafe_allow_html=True)

# How it works section
st.markdown("""
<div class="how-it-works">
    <div class="section-header">
        <h2>🚀 How It Works</h2>
        <p>Three simple steps to start exchanging skills</p>
    </div>
    <div class="steps-grid">
        <div class="step-card">
            <div class="step-number">1</div>
            <div class="step-icon">📝</div>
            <h4>List Your Skills</h4>
            <p>Share what you can teach and what you want to learn. Be specific about your experience level.</p>
        </div>
        <div class="step-card">
            <div class="step-number">2</div>
            <div class="step-icon">🔍</div>
            <h4>Find a Match</h4>
            <p>Browse available skills and find someone whose offerings complement your needs.</p>
        </div>
        <div class="step-card">
            <div class="step-number">3</div>
            <div class="step-icon">🤝</div>
            <h4>Start Swapping</h4>
            <p>Connect, schedule sessions, and begin your knowledge exchange journey!</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")  # Section divider

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("""
    <div class="skill-form">
        <div class="form-header">
            <h3>➕ Add Your Skill</h3>
            <p>Share what you can teach or want to learn</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("add_skill_form", clear_on_submit=True):
        skill_name = st.text_input("Skill Name", placeholder="e.g., Python Programming, Spanish, Guitar...")
        
        col_a, col_b = st.columns(2)
        with col_a:
            skill_type = st.selectbox("I want to...", ["Teach this skill", "Learn this skill"])
        with col_b:
            category = st.selectbox("Category", ["Technology", "Language", "Art & Design", "Music", "Sports & Fitness", "Academic", "Other"])
        
        level = st.select_slider(
            "Skill Level",
            options=["Beginner", "Intermediate", "Advanced"],
            value="Intermediate"
        )
        
        description = st.text_area("Description", placeholder="Describe your experience or what you want to learn...", height=100)
        
        submitted = st.form_submit_button("🚀 Add Skill", use_container_width=True)
        
        if submitted:
            if skill_name and description:
                category_map = {
                    "Technology": "tech",
                    "Language": "language",
                    "Art & Design": "art",
                    "Music": "music",
                    "Sports & Fitness": "sports",
                    "Academic": "academic",
                    "Other": "other"
                }
                
                new_skill = {
                    "user": current_user.get('name'),
                    "skill": skill_name,
                    "category": category_map.get(category, "other"),
                    "level": level.lower(),
                    "type": "teach" if "Teach" in skill_type else "learn",
                    "description": description
                }
                
                st.session_state.skill_offerings.append(new_skill)
                st.success(f"✨ '{skill_name}' added successfully! Others can now find you.")
                st.balloons()
            else:
                st.error("Please fill in all required fields!")

with col2:
    st.markdown("""
    <div class="tip-card">
        <div class="tip-icon">💡</div>
        <div class="tip-content">
            <p><strong>Pro Tip:</strong> The more specific your skill description, the better matches you'll find! Include your experience level and availability.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Show user's current skills
    user_skills = [s for s in st.session_state.skill_offerings if s['user'] == current_user.get('name')]
    
    if user_skills:
        st.markdown("""
        <div style="
            background: rgba(30, 30, 45, 0.7);
            border: 1px solid rgba(255, 255, 255, 0.12);
            border-radius: 20px;
            padding: 1.5rem;
            margin-top: 1rem;
        ">
            <h4 style="color: #8b5cf6 !important; margin-bottom: 1rem;">📋 Your Listed Skills</h4>
        </div>
        """, unsafe_allow_html=True)
        
        for skill in user_skills:
            type_emoji = "🎓" if skill['type'] == 'teach' else "🌱"
            type_label = "Teaching" if skill['type'] == 'teach' else "Learning"
            
            st.markdown(f"""
            <div style="
                background: rgba(255, 255, 255, 0.03);
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 12px;
                padding: 1rem;
                margin: 0.5rem 0;
            ">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="color: white !important; font-weight: 600;">{type_emoji} {skill['skill']}</span>
                    <span class="level-badge {skill['level']}">{skill['level'].upper()}</span>
                </div>
                <p style="font-size: 0.85rem; margin-top: 0.5rem; color: #71717a !important;">{type_label} • {skill['category'].title()}</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="
            background: rgba(30, 30, 45, 0.7);
            border: 1px solid rgba(255, 255, 255, 0.12);
            border-radius: 20px;
            padding: 2rem;
            margin-top: 1rem;
            text-align: center;
        ">
            <span style="font-size: 3rem;">🎯</span>
            <h4 style="color: #a1a1aa !important; margin-top: 1rem;">No Skills Listed Yet</h4>
            <p style="color: #71717a !important; font-size: 0.9rem;">Add your first skill to start connecting with others!</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")  # Browse skills section

st.markdown("""
<div class="section-header">
    <h2>🔍 Browse Available Skills</h2>
    <p>Find the perfect skill exchange partner</p>
</div>
""", unsafe_allow_html=True)

filter_col1, filter_col2, filter_col3 = st.columns([1, 1, 1])  # Filter controls

with filter_col1:
    filter_type = st.selectbox("Filter by Type", ["All", "Teaching", "Learning"], key="filter_type")

with filter_col2:
    filter_category = st.selectbox(
        "Filter by Category", 
        ["All", "Technology", "Language", "Art & Design", "Music", "Sports & Fitness", "Academic", "Other"],
        key="filter_category"
    )

with filter_col3:
    search_query = st.text_input("🔍 Search Skills", placeholder="Search...", key="search_skills")

filtered_skills = st.session_state.skill_offerings.copy()  # Start with all skills

if filter_type != "All":
    type_value = "teach" if filter_type == "Teaching" else "learn"
    filtered_skills = [s for s in filtered_skills if s['type'] == type_value]

if filter_category != "All":
    category_map = {
        "Technology": "tech",
        "Language": "language", 
        "Art & Design": "art",
        "Music": "music",
        "Sports & Fitness": "sports",
        "Academic": "academic",
        "Other": "other"
    }
    cat_value = category_map.get(filter_category, "other")
    filtered_skills = [s for s in filtered_skills if s['category'] == cat_value]

if search_query:
    filtered_skills = [s for s in filtered_skills if search_query.lower() in s['skill'].lower() or search_query.lower() in s['description'].lower()]

if filtered_skills:  # Display filtered skills
    # Group by category for display
    skill_cols = st.columns(3)
    
    for idx, skill in enumerate(filtered_skills):
        col_idx = idx % 3
        
        category_config = {
            "tech": {"icon": "💻", "color": "#3b82f6", "name": "Technology"},
            "language": {"icon": "🗣️", "color": "#8b5cf6", "name": "Language"},
            "art": {"icon": "🎨", "color": "#ec4899", "name": "Art & Design"},
            "music": {"icon": "🎵", "color": "#f59e0b", "name": "Music"},
            "sports": {"icon": "⚽", "color": "#10b981", "name": "Sports"},
            "academic": {"icon": "📖", "color": "#06b6d4", "name": "Academic"},
            "other": {"icon": "✨", "color": "#6366f1", "name": "Other"}
        }
        
        cat = category_config.get(skill['category'], category_config['other'])
        type_emoji = "🎓" if skill['type'] == 'teach' else "🌱"
        type_label = "Teaching" if skill['type'] == 'teach' else "Wants to Learn"
        
        with skill_cols[col_idx]:
            st.markdown(skill_card(
                cat,
                skill['category'],
                skill['level'],
                type_emoji,
                skill['skill'],
                skill.get('description', ''),
                skill['user'],
                type_label
            ), unsafe_allow_html=True)
            
            if skill['user'] != current_user.get('name'):
                user_email = skill.get('email', '')
                if user_email:
                    import urllib.parse
                    subject = f"UniSync: Interested in learning {skill['skill']}"
                    body = f"Hi {skill['user']},\n\nI found your skill listing on UniSync and I'm interested in learning {skill['skill']}.\n\nLet's connect!\n\nBest regards,\n{current_user.get('name')}"
                    mailto_link = f"mailto:{user_email}?subject={urllib.parse.quote(subject)}&body={urllib.parse.quote(body)}"
                    
                    if st.button(f"📧 Contact {skill['user']}", key=f"contact_{idx}", use_container_width=True):
                        st.markdown(f'<meta http-equiv="refresh" content="0; url={mailto_link}">', unsafe_allow_html=True)
                        st.success(f"✉️ Opening email to {skill['user']}...")
                else:
                    if st.button(f"🤝 Connect", key=f"connect_{idx}", use_container_width=True):
                        st.success(f"Request sent to {skill['user']}! They'll be notified about your interest in '{skill['skill']}'")
else:
    st.markdown("""
    <div style="
        text-align: center;
        padding: 3rem;
        background: rgba(30, 30, 45, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 20px;
    ">
        <span style="font-size: 4rem;">🔍</span>
        <h3 style="color: #a1a1aa !important; margin-top: 1rem;">No Skills Found</h3>
        <p style="color: #71717a !important;">Try adjusting your filters or search terms</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")  # Section divider

st.markdown("""
<div class="trending-section">
    <div class="section-header">
        <h2>🔥 Trending Skills by Category</h2>
        <p>Most popular skills being exchanged right now</p>
    </div>
</div>
""", unsafe_allow_html=True)

trend_col1, trend_col2, trend_col3 = st.columns(3)

tech_skills = [s for s in st.session_state.skill_offerings if s['category'] == 'tech']  # Filter tech skills
with trend_col1:
    st.markdown("""
    <div class="column tech">
        <h4>💻 Technology</h4>
        <ul>
    """, unsafe_allow_html=True)

    for skill in tech_skills[:4]:
        skill_name = skill['skill']
        skill_user = skill['user']
        skill_level = skill['level']
        st.markdown(f"""
        <li>
            <div class="skill-text">
                <div class="skill-name">{skill_name}</div>
                <div class="skill-teacher">by {skill_user}</div>
            </div>
            <span class="level-badge {skill_level}">{skill_level[:3].upper()}</span>
        </li>
        """, unsafe_allow_html=True)

    if not tech_skills:
        st.markdown("<li><div class='skill-text'><div class='skill-name'>No skills yet</div></div></li>", unsafe_allow_html=True)

    st.markdown("</ul></div>", unsafe_allow_html=True)

creative_skills = [s for s in st.session_state.skill_offerings if s['category'] in ['art', 'music']]  # Filter creative skills
with trend_col2:
    st.markdown("""
    <div class="column creative">
        <h4>🎨 Creative Arts</h4>
        <ul>
    """, unsafe_allow_html=True)

    for skill in creative_skills[:4]:
        skill_name = skill['skill']
        skill_user = skill['user']
        skill_level = skill['level']
        st.markdown(f"""
        <li>
            <div class="skill-text">
                <div class="skill-name">{skill_name}</div>
                <div class="skill-teacher">by {skill_user}</div>
            </div>
            <span class="level-badge {skill_level}">{skill_level[:3].upper()}</span>
        </li>
        """, unsafe_allow_html=True)

    if not creative_skills:
        st.markdown("<li><div class='skill-text'><div class='skill-name'>No skills yet</div></div></li>", unsafe_allow_html=True)

    st.markdown("</ul></div>", unsafe_allow_html=True)

academic_skills = [s for s in st.session_state.skill_offerings if s['category'] in ['academic', 'language']]  # Filter academic skills
with trend_col3:
    st.markdown("""
    <div class="column academic">
        <h4>📚 Academic & Language</h4>
        <ul>
    """, unsafe_allow_html=True)

    for skill in academic_skills[:4]:
        skill_name = skill['skill']
        skill_user = skill['user']
        skill_level = skill['level']
        st.markdown(f"""
        <li>
            <div class="skill-text">
                <div class="skill-name">{skill_name}</div>
                <div class="skill-teacher">by {skill_user}</div>
            </div>
            <span class="level-badge {skill_level}">{skill_level[:3].upper()}</span>
        </li>
        """, unsafe_allow_html=True)

    if not academic_skills:
        st.markdown("<li><div class='skill-text'><div class='skill-name'>No skills yet</div></div></li>", unsafe_allow_html=True)

    st.markdown("</ul></div>", unsafe_allow_html=True)

st.markdown("---")  # Section divider

st.markdown("""
<div class="recent-exchanges">
    <div class="section-header">
        <h2>🤝 Recent Skill Exchanges</h2>
        <p>See what skills are being swapped in the community</p>
    </div>
    <div class="exchange-feed">
""", unsafe_allow_html=True)

for exchange in st.session_state.recent_exchanges:
    st.markdown(f"""
    <div class="exchange-item">
        <div class="exchange-avatars">
            <div class="avatar left">👤</div>
            <div class="avatar right">👤</div>
        </div>
        <span class="exchange-icon">🔄</span>
        <div class="exchange-content">
            <div class="exchange-skill">{exchange['skill1']} ↔️ {exchange['skill2']}</div>
            <div class="exchange-users">{exchange['user1']} & {exchange['user2']}</div>
        </div>
        <div class="exchange-time">{exchange['time']}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("</div></div>", unsafe_allow_html=True)

st.markdown("---")  # Section divider

st.markdown("""
<div style="
    background: linear-gradient(135deg, rgba(249, 115, 22, 0.15) 0%, rgba(236, 72, 153, 0.1) 100%);
    border: 1px solid rgba(249, 115, 22, 0.3);
    border-radius: 24px;
    padding: 2.5rem;
    text-align: center;
    margin: 2rem 0;
">
    <span style="font-size: 3rem; display: block; margin-bottom: 1rem;">⚡</span>
    <h3 style="
        background: linear-gradient(135deg, #f97316 0%, #ec4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 1.75rem !important;
        margin-bottom: 0.75rem !important;
    ">Quick Match</h3>
    <p style="color: #a1a1aa !important; max-width: 500px; margin: 0 auto 1.5rem;">
        Let us find the perfect skill swap partner for you based on your interests and availability!
    </p>
</div>
""", unsafe_allow_html=True)

col_match1, col_match2, col_match3 = st.columns([1, 2, 1])

with col_match2:
    if st.button("🎯 Find My Match", use_container_width=True, type="primary"):
        available_skills = [s for s in st.session_state.skill_offerings if s['user'] != current_user.get('name')]
        if available_skills:
            match = random.choice(available_skills)
            match_user = match['user']
            match_skill = match['skill']
            match_description = match['description']
            match_type = 'teach' if match['type'] == 'teach' else 'learn'

            st.markdown(f"""
            <div style="
                background: rgba(16, 185, 129, 0.15);
                border: 1px solid rgba(16, 185, 129, 0.3);
                border-radius: 16px;
                padding: 1.5rem;
                margin-top: 1rem;
                text-align: center;
            ">
                <span style="font-size: 2rem;">🎉</span>
                <h4 style="color: #10b981 !important; margin: 0.5rem 0;">Match Found!</h4>
                <p style="color: white !important; font-size: 1.1rem;">
                    <strong>{match_user}</strong> can {match_type} <strong>{match_skill}</strong>
                </p>
                <p style="color: #71717a !important; font-size: 0.9rem;">{match_description}</p>
            </div>
            """, unsafe_allow_html=True)
            st.balloons()
        else:
            st.info("No matches available yet. Be the first to add more skills!")

# Footer
st.markdown("""
<div class="footer">
    <p>🔄 Skill Swap • Share Knowledge, Grow Together • Uni-Sync Platform</p>
</div>
""", unsafe_allow_html=True)