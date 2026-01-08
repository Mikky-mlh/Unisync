import streamlit as st
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.data_manager import load_users, get_user_reviews

st.set_page_config(page_title="Reviews", page_icon="⭐", layout="wide")

if 'current_user' not in st.session_state or st.session_state.current_user is None:
    st.warning("🔒 Please login to see reviews")
    st.stop()

st.title("⭐ User Reviews")

users = load_users()

for user in users:
    if user.get('id') == st.session_state.current_user.get('id'):
        continue  # Skip yourself
    
    reviews = get_user_reviews(user.get('id'))
    
    if reviews:
        with st.expander(f"👤 {user.get('name')} - {len(reviews)} reviews"):
            avg = sum(r['rating'] for r in reviews) / len(reviews)
            st.write(f"**Average Rating:** {'⭐' * int(avg)} {round(avg, 1)}/5.0")
            
            for review in reviews:
                rater = next((u for u in users if u.get('id') == review['rater_id']), None)
                rater_name = rater.get('name') if rater else 'Anonymous'
                
                st.markdown(f"""
                **{rater_name}** rated {'⭐' * review['rating']} ({review['rating']}/5)  
                *{review.get('timestamp', 'N/A')}*  
                {review.get('review', 'No review text')}
                """)
                st.markdown("---")