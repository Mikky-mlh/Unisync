import streamlit as st
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.data_manager import load_users, get_user_reviews

st.set_page_config(page_title="Reviews", page_icon="⭐", layout="wide")  # Configure page

try:
    with open("assets/style-review.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except:
    pass

with st.sidebar:
    col_s1, col_s2, col_s3 = st.columns([1, 3, 1])
    with col_s2:
        st.image("assets/logo.png", width=120)

# JavaScript to force scrollbar styling
st.markdown("""
<style id="custom-scrollbar">
.custom-scroll::-webkit-scrollbar {
    width: 12px !important;
}
.custom-scroll::-webkit-scrollbar-track {
    background: #0a0a0f !important;
}
.custom-scroll::-webkit-scrollbar-thumb {
    background: linear-gradient(180deg, #fbbf24, #f59e0b) !important;
    border-radius: 10px !important;
    border: 3px solid #0a0a0f !important;
}
.custom-scroll::-webkit-scrollbar-thumb:hover {
    background: #fbbf24 !important;
    box-shadow: 0 0 10px rgba(251, 191, 36, 0.5) !important;
}
</style>

<script>
(function() {
    function applyScrollbar() {
        const selectors = [
            '[data-testid="stAppViewContainer"]',
            '[data-testid="stMain"]',
            '.main',
            'section.main',
            '[data-testid="stVerticalBlock"]',
            'body',
            'html'
        ];
        
        selectors.forEach(selector => {
            document.querySelectorAll(selector).forEach(el => {
                el.classList.add('custom-scroll');
            });
        });
    }
    
    applyScrollbar();
    setTimeout(applyScrollbar, 500);
    setTimeout(applyScrollbar, 1500);
    
    const observer = new MutationObserver(applyScrollbar);
    observer.observe(document.body, { childList: true, subtree: true });
})();
</script>
""", unsafe_allow_html=True)

if 'current_user' not in st.session_state or st.session_state.current_user is None:
    st.warning("🔒 Please login to see reviews")
    st.stop()

st.markdown("""
<div style="text-align: center; margin-bottom: 0.5rem;">
    <h1><span class="emoji-fix">⭐</span> User Reviews</h1>
</div>
""", unsafe_allow_html=True)

users = load_users()

st.sidebar.markdown("""
<h3><span class="emoji-fix">🔍</span> Filter & Sort</h3>
""", unsafe_allow_html=True)
st.sidebar.caption("Refine your search")

min_rating = st.sidebar.slider("⭐ Minimum Rating", 1, 5, 1)
sort_by = st.sidebar.selectbox(
    "🔄 Sort By",
    ["Highest Rated", "Lowest Rated", "Most Reviews", "Fewest Reviews", "Name (A-Z)", "Name (Z-A)"]
)

show_only_reviewed = st.sidebar.checkbox("✅ Only show users with reviews", value=True)

st.sidebar.markdown("---")

# Collect user data with reviews
user_data = []
for user in users:
    if user.get('id') == st.session_state.current_user.get('id'):
        continue
    
    reviews = get_user_reviews(user.get('id'))
    
    if reviews:
        avg = sum(r['rating'] for r in reviews) / len(reviews)
        user_data.append({
            'user': user,
            'reviews': reviews,
            'avg_rating': avg,
            'review_count': len(reviews)
        })
    elif not show_only_reviewed:
        user_data.append({
            'user': user,
            'reviews': [],
            'avg_rating': 0,
            'review_count': 0
        })

# Apply filters
filtered_data = [d for d in user_data if d['avg_rating'] >= min_rating or d['avg_rating'] == 0]

# Sort data
if sort_by == "Highest Rated":
    filtered_data.sort(key=lambda x: x['avg_rating'], reverse=True)
elif sort_by == "Lowest Rated":
    filtered_data.sort(key=lambda x: x['avg_rating'] if x['avg_rating'] > 0 else 6)
elif sort_by == "Most Reviews":
    filtered_data.sort(key=lambda x: x['review_count'], reverse=True)
elif sort_by == "Fewest Reviews":
    filtered_data.sort(key=lambda x: x['review_count'])
elif sort_by == "Name (A-Z)":
    filtered_data.sort(key=lambda x: x['user'].get('name', ''))
elif sort_by == "Name (Z-A)":
    filtered_data.sort(key=lambda x: x['user'].get('name', ''), reverse=True)

st.sidebar.info(f"📊 Showing {len(filtered_data)} users")

# Display filtered and sorted reviews
for data in filtered_data:
    user = data['user']
    reviews = data['reviews']
    avg_rating = data['avg_rating']
    review_count = data['review_count']
    
    if reviews:
        with st.expander(f"👤 {user.get('name')} - {review_count} review{'s' if review_count != 1 else ''} - {'⭐' * int(avg_rating)} {round(avg_rating, 1)}/5.0"):
            st.write(f"**Average Rating:** {'⭐' * int(avg_rating)} {round(avg_rating, 1)}/5.0")
            
            for review in reviews:
                rater = next((u for u in users if u.get('id') == review['rater_id']), None)
                rater_name = rater.get('name') if rater else 'Anonymous'
                
                st.markdown(f"""
                **{rater_name}** rated {'⭐' * review['rating']} ({review['rating']}/5)  
                *{review.get('timestamp', 'N/A')}*  
                {review.get('review', 'No review text')}
                """)
                st.markdown("---")
    else:
        with st.expander(f"👤 {user.get('name')} - No reviews yet"):
            st.info("💬 This user hasn't received any reviews yet.")