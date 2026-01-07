# File: 3_Skill_Swap.py
# Purpose: Simple skill exchange page (optional/bonus)
# Assigned to: Yuvraj & Siddhika
# Note: Most functionality is in Find Peers page

import streamlit as st
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

st.set_page_config(page_title="Skill Swap", page_icon="🔄", layout="wide")

st.title("🔄 Skill Swap")
st.markdown("### Quick skill exchange - Full marketplace in Find Peers page")

# Option 1: Redirect to Find Peers
st.info("💡 **Tip:** The full skill exchange marketplace is in the Find Peers page!")
if st.button("👉 Go to Skill Exchange in Find Peers", type="primary"):
    st.switch_page("pages/2_Find_Peers.py")

# Option 2: Quick skill posting form
st.markdown("---")
st.subheader("📝 Quick Skill Post")
st.caption("Post a skill you can teach or want to learn")

with st.form("post_skill"):
    col1, col2 = st.columns(2)
    
    with col1:
        skill_name = st.text_input("🎯 Skill Name", placeholder="e.g., Python Programming")
        skill_type = st.radio("Type", ["I can teach this", "I want to learn this"])
    
    with col2:
        category = st.selectbox("📚 Category", ["Tech", "Language", "Art", "Music", "Sports", "Academic", "Other"])
        level = st.select_slider("Level", ["Beginner", "Intermediate", "Advanced"])
    
    description = st.text_area("📝 Description (optional)", placeholder="Tell us more about this skill...")
    
    submit = st.form_submit_button("🚀 Post Skill", type="primary", use_container_width=True)
    
    if submit and skill_name:
        st.success(f"✅ Skill '{skill_name}' posted successfully!")
        st.balloons()
        st.info("💡 In the full app, this would be saved to the database and shown to other students.")
    elif submit:
        st.error("⚠️ Please enter a skill name")

# Show some example skills
st.markdown("---")
st.subheader("🌟 Trending Skills")

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
    **💻 Tech Skills**
    - Python Programming (Yuvraj)
    - Web Development (Siddhika)
    - Data Analysis (Aaradhya)
    - Machine Learning (Yuvraj)
    """)
with col2:
    st.markdown("""
    **🎵 Creative Skills**
    - Guitar Playing (Aaradhya)
    - Digital Art (Siddhika)
    - Photography (Yuvraj)
    - Video Editing (Siddhika)
    """)
with col3:
    st.markdown("""
    **📚 Academic Skills**
    - Calculus Tutoring (Yuvraj)
    - Essay Writing (Siddhika)
    - Public Speaking (Aaradhya)
    - Research Methods (Yuvraj)
    """)