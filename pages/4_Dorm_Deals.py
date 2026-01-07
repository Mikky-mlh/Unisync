# File: 4_Dorm_Deals.py
# Purpose: Marketplace for accommodation, furniture, and campus resources
# Assigned to: Siddhika & Aaradhya
# Deadline: Jan 9, 2024

# Key Features:
# - Display listings in card format with filters
# - Allow users to post new listings
# - Implement search and filtering options

import streamlit as st
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.data_manager import load_listings
import pandas as pd

# Setup page configuration
st.set_page_config(page_title="Dorm Deals", page_icon="🏢", layout="wide")

# Load CSS for styling
try:
    with open("assets/style-dorm.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except:
    pass  # CSS file optional

# Page header
st.title("🏢 Dorm Deals")
st.markdown("### Your campus marketplace for rooms, furniture, and resources")
st.caption("💡 Find great deals or post items you want to sell/give away")

# Load all listings from CSV
listings = load_listings()

# Sidebar filters
st.sidebar.title("🔍 Filters")
st.sidebar.caption("Narrow down your search")

# Filter by item type
type_options = ["All", "room", "furniture", "textbook", "electronics", "other"]
selected_type = st.sidebar.selectbox("🏷️ Item Type", type_options)

# Price range filter
if listings:
    prices = []
    for l in listings:
        price_str = str(l.get('price', '0'))
        if price_str.lower() == 'free':
            prices.append(0)
        else:
            # Extract numbers from price string
            import re
            numbers = re.findall(r'\d+', price_str)
            if numbers:
                prices.append(int(numbers[0]))
            else:
                prices.append(0)

    max_price = max(prices) if prices else 1000
    price_range = st.sidebar.slider("💰 Price Range", 0, max_price, (0, max_price))
else:
    price_range = (0, 1000)

# Location search
location_search = st.sidebar.text_input("📍 Location", placeholder="e.g., Dorm B")

# Free items only filter
free_only = st.sidebar.checkbox("✅ Free items only")

st.sidebar.markdown("---")
st.sidebar.info(f"📊 Showing {len(listings)} listings")

# Display available listings
st.subheader("📦 Available Listings")

if not listings:
    st.warning("😕 No listings available yet. Be the first to post!")
else:
    # Display listings in a 3-column grid
    st.markdown('<div class="listings-grid">', unsafe_allow_html=True)
    cols = st.columns(3)
    for idx, listing in enumerate(listings):
        with cols[idx % 3]:
            # Card container
            st.markdown(f"""
            <div class="listing-card">
                <div class="listing-header">
                    <span class="listing-type">{listing.get('type', 'other').upper()}</span>
                    <span class="listing-status">{listing.get('status', 'available').upper()}</span>
                </div>
                <h3 class="listing-title">{listing.get('title', 'Untitled')}</h3>
                <p class="listing-desc">{listing.get('description', 'No description')}</p>
                <div class="listing-details">
                    <p>📍 <strong>Location:</strong> {listing.get('location', 'Not specified')}</p>
                    <p>💰 <strong>Price:</strong> {listing.get('price', 'Contact for price')}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

            if st.button("👋 I'm Interested", key=f"interest_{listing.get('id')}", use_container_width=True):
                st.success("✅ Interest registered! Contact info would be shown here.")
    st.markdown('</div>', unsafe_allow_html=True)

# Form to post new listing
st.markdown("---")
st.subheader("📝 Post Your Own Listing")
st.caption("Have something to sell or give away? List it here!")

with st.form("post_listing_form"):
    col1, col2 = st.columns(2)

    with col1:
        title = st.text_input("🏷️ Title *", placeholder="e.g., Study Desk with Chair")
        listing_type = st.selectbox("📊 Type *", ["room", "furniture", "textbook", "electronics", "other"])
        price = st.text_input("💰 Price", placeholder="e.g., $50 or Free")

    with col2:
        location = st.text_input("📍 Location", placeholder="e.g., Dorm B, Room 301")
        contact = st.text_input("📧 Contact Email", placeholder="your.email@campus.edu")

    description = st.text_area("📝 Description", placeholder="Describe your item, its condition, etc.", height=100)

    st.caption("* Required fields")

    submit_button = st.form_submit_button("🚀 Post Listing", type="primary", use_container_width=True)

    if submit_button:
        # Validate inputs
        if not title or not listing_type:
            st.error("⚠️ Please fill in all required fields (Title and Type)")
        else:
            st.success(f"✅ Listing '{title}' posted successfully!")
            st.balloons()
            st.info("💡 In the full app, this would be saved to listings.csv and shown to all users.")

            # Show preview of what was submitted
            with st.expander("👁️ Preview Your Listing"):
                st.markdown(f"**Title:** {title}")
                st.markdown(f"**Type:** {listing_type}")
                st.markdown(f"**Price:** {price if price else 'Not specified'}")
                st.markdown(f"**Location:** {location if location else 'Not specified'}")
                st.markdown(f"**Description:** {description if description else 'No description'}")

# Campus resources section
st.markdown("---")
st.subheader("🌟 Campus Resources")
st.caption("Quick links to campus services")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown("🏫 **Housing Office**")
    st.caption("Find official housing")
with col2:
    st.markdown("📚 **Library**")
    st.caption("Borrow textbooks")
with col3:
    st.markdown("🛍️ **Campus Store**")
    st.caption("Buy supplies")
with col4:
    st.markdown("❓ **Help Desk**")
    st.caption("Get support")
