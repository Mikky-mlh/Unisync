import streamlit as st

st.set_page_config(page_title="User Guide - Uni-Sync", page_icon="📖", layout="wide")

try:
    with open("assets/style-guide.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except:
    pass

with st.sidebar:
    col_s1, col_s2, col_s3 = st.columns([1, 3, 1])
    with col_s2:
        st.image("assets/logo.png", width=120)

st.markdown("""
<div style="text-align: center; margin-bottom: 0.5rem;">
    <h1><span class="emoji-fix">📖</span> Uni-Sync User Guide</h1>
</div>
""", unsafe_allow_html=True)
st.markdown("### Learn how to make the most of your campus connections")

st.markdown("---")

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("""
    ## 🚀 Getting Started
    
    ### 1️⃣ Create Your Account
    - Click **"New? Join UniSync"** in the sidebar on the Home page
    - Fill in your details: name, email, year, major, skills, and interests
    - Add your **X-Factor** - what makes you unique!
    - Set a secure password
    
    ### 2️⃣ Login
    - Enter your email and password in the sidebar
    - Access all features once logged in
    
    ---
    
    ## 👥 Campus Tribe - Find Peers
    
    ### Swipe to Connect
    - Browse student profiles one by one
    - **👎 Pass** - Skip to the next profile
    - **👍 Connect** - Add them to your matches
    
    ### Advanced Filters
    - Filter by **Major**, **Year**, **Skills**, or **Interests**
    - Use the search bar to find specific keywords
    - Reset filters anytime to see all users
    
    ### Your Matches
    - View all your connections at the bottom
    - Contact them directly via email
    - Rate your experience with them (1-5 stars)
    
    ---
    
    ## 🔄 Skill Swap
    
    ### Share Your Skills
    - Click **"Add Your Skill"**
    - Choose if you want to **Teach** or **Learn**
    - Select a category and skill level
    - Add a detailed description
    
    ### Find Skill Partners
    - Browse available skills by category
    - Filter by Teaching/Learning and Category
    - Use search to find specific skills
    - Contact users directly to arrange exchanges
    
    ### Quick Match
    - Click **"Find My Match"** for instant suggestions
    - Get personalized skill swap recommendations
    """)

with col2:
    st.markdown("""
    ## 🏢 Dorm Deals - Marketplace
    
    ### Browse Listings
    - View rooms, furniture, textbooks, electronics, and more
    - Use filters to narrow down by:
        - **Item Type** (room, furniture, etc.)
        - **Price Range** (including free items)
        - **Location** (search by dorm/area)
    
    ### Post Your Listing
    - Fill in the listing form:
        - Title and description
        - Type and price
        - Location and contact info
    - Click **"Post Listing"** to publish
    - Your listing appears immediately for others
    
    ### Express Interest
    - Click **"I'm Interested"** on any listing
    - Opens email to contact the poster directly
    - Your interest is saved in connections
    
    ---
    
    ## ⭐ Reviews & Ratings
    
    ### Rate Your Connections
    - Go to your matches on any page
    - Click **"⭐ Rate"** button
    - Choose 1-5 stars and write a review
    - Help build trust in the community
    
    ### View Reviews
    - Visit the **Reviews** page
    - See ratings for all users
    - Filter by minimum rating
    - Sort by highest/lowest rated or most reviews
    
    ---
    
    ## 🤖 AI Campus Assistant
    
    ### Ask Anything
    - Type your question in the chat box on Home page
    - Examples:
        - "Find someone to study calculus with"
        - "Who can help me with Python?"
        - "Looking for a room near campus"
    - Get personalized matches with contact info
    - AI analyzes all users, skills, and listings
    """)

st.markdown("---")

st.markdown("""
## 💡 Pro Tips

<div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 1rem; margin: 1.5rem 0;">
    <div style="background: rgba(139, 92, 246, 0.1); border: 1px solid rgba(139, 92, 246, 0.3); border-radius: 12px; padding: 1.25rem;">
        <h4 style="color: #8b5cf6 !important; margin-top: 0;">✨ Complete Your Profile</h4>
        <p style="color: #a1a1aa !important;">Add detailed skills and interests to get better matches. Your X-Factor makes you stand out!</p>
    </div>
    <div style="background: rgba(6, 182, 212, 0.1); border: 1px solid rgba(6, 182, 212, 0.3); border-radius: 12px; padding: 1.25rem;">
        <h4 style="color: #06b6d4 !important; margin-top: 0;">🤝 Be Active</h4>
        <p style="color: #a1a1aa !important;">The more you connect and engage, the more opportunities you'll find. Don't be shy!</p>
    </div>
    <div style="background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 12px; padding: 1.25rem;">
        <h4 style="color: #10b981 !important; margin-top: 0;">⭐ Leave Reviews</h4>
        <p style="color: #a1a1aa !important;">Help others by rating your connections. Good reviews build trust in the community.</p>
    </div>
    <div style="background: rgba(245, 158, 11, 0.1); border: 1px solid rgba(245, 158, 11, 0.3); border-radius: 12px; padding: 1.25rem;">
        <h4 style="color: #f59e0b !important; margin-top: 0;">🔍 Use Filters</h4>
        <p style="color: #a1a1aa !important;">Save time by filtering for exactly what you need. Combine multiple filters for best results.</p>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

st.markdown("""
## ❓ Frequently Asked Questions

**Q: Is Uni-Sync free to use?**  
A: Yes! Uni-Sync is completely free for all students.

**Q: How do I contact someone?**  
A: Click the contact/email button on their profile or listing. It opens your email client automatically.

**Q: Can I edit my profile after signing up?**  
A: Yes! Use the "Edit Profile" section in the sidebar on the Home page.

**Q: What if I accidentally passed on someone?**  
A: Click the "Reset" button on the Find Peers page to review all users again.

**Q: How does the AI Assistant work?**  
A: It analyzes all users, skills, and listings to find the best matches for your query using Google Gemini AI.

**Q: Can I delete my listing?**  
A: Currently, listings remain active. Contact support if you need to remove one.

**Q: How are ratings calculated?**  
A: Average of all ratings received. More ratings = more accurate score.

---

## 🆘 Need Help?

<div style="text-align: center; padding: 2rem; background: rgba(255, 255, 255, 0.03); border-radius: 16px; margin: 1.5rem 0;">
    <h3 style="color: #8b5cf6 !important;">Still have questions?</h3>
    <p style="color: #a1a1aa !important; margin-bottom: 1rem;">We're here to help!</p>
    <p style="color: #71717a !important;">Contact us at: <strong style="color: #06b6d4 !important;">support@unisync.edu</strong></p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<footer style="text-align: center; padding: 2rem; margin-top: 3rem; border-top: 1px solid rgba(255, 255, 255, 0.08);">
    <p style="color: #71717a !important;">Made with ❤️ for the university community | <strong>Uni-Sync</strong> © 2024</p>
</footer>
""", unsafe_allow_html=True)
