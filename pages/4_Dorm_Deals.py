import streamlit as st
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.data_manager import load_listings, load_users, save_listing
import pandas as pd
import re

# Initialize session state if not already done
if 'current_user' not in st.session_state:
    st.session_state.current_user = None

# Setup page configuration
st.set_page_config(page_title="Dorm Deals", page_icon="🏢", layout="wide")

# Check if user is logged in
if 'current_user' not in st.session_state or st.session_state.current_user is None:
    st.warning("🔒 Please login from the Home page to access Dorm Deals")
    st.stop()

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

# Load all listings and users from CSV
listings = load_listings()
users = load_users()

# Create a mapping from user_id to user info for easy lookup
user_map = {}
for user in users:
    user_map[user['id']] = user

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

# --- LOGIC: Filter the listings based on sidebar ---
filtered_listings = []

for listing in listings:
    # 1. Filter by Type
    if selected_type != "All" and listing.get('type', '').lower() != selected_type.lower():
        continue

    # 2. Filter by Price
    price_str = str(listing.get('price', '0'))
    price_val = 0

    if 'free' in price_str.lower():
        price_val = 0
    else:
        # Extract numeric components from the price string.
        # If a range like "$5-10" is detected, use the average of the first two numbers.
        # Otherwise, fall back to the first numeric group.
        numbers = re.findall(r'\d+', price_str)
        if numbers:
            numbers = [int(n) for n in numbers]
            if '-' in price_str and len(numbers) >= 2:
                price_val = int((numbers[0] + numbers[1]) / 2)
            else:
                price_val = numbers[0]
        numbers = re.findall(r'\d+', price_str)
        if numbers:
            price_val = int(numbers[0])
    
    # Check if price is within the slider range
    if price_val < price_range[0] or price_val > price_range[1]:
        continue

    # 3. Filter by Location (if user typed something)
    if location_search:
        loc = str(listing.get('location', '')).lower()
        if location_search.lower() not in loc:
            continue

    # 4. Filter "Free Only" checkbox
    if free_only and price_val != 0:
        continue

    # If it passes all checks, add to our new list
    filtered_listings.append(listing)

# Display available listings
st.subheader("📦 Available Listings")

if not filtered_listings:
    st.warning("😕 No listings match your filters.")
else:
    st.markdown('<div class="listings-grid">', unsafe_allow_html=True)
    cols = st.columns(3)
    for idx, listing in enumerate(filtered_listings):
        with cols[idx % 3]:
            # Get the user who posted this listing
            poster_user = user_map.get(listing.get('user_id'))
            poster_name = poster_user.get('name', 'Anonymous') if poster_user else 'Unknown'

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
                    <p>👤 <strong>Posted by:</strong> {poster_name}</p>
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
            price = st.text_input("💰 Price", placeholder="e.g., ₹500 or Free")

        with col2:
            location = st.text_input("📍 Location", placeholder="e.g., Boys Hostel, Room 301")
            contact = st.text_input("📧 Contact Email", value=st.session_state.current_user.get('email', ''), placeholder="your.email@iitd.ac.in")

        description = st.text_area("📝 Description", placeholder="Describe your item, its condition, etc.", height=100)

        st.caption("* Required fields")

        submit_button = st.form_submit_button("🚀 Post Listing", type="primary", use_container_width=True)

        if submit_button:
            # Validate inputs
            if not title or not listing_type:
                st.error("⚠️ Please fill in all required fields (Title and Type)")
            else:
                # Create listing data dictionary
                listing_data = {
                    "user_id": st.session_state.current_user.get('id'),
                    "type": listing_type,
                    "title": title,
                    "description": description if description else "No description provided",
                    "location": location if location else "Location not specified",
                    "price": price if price else "Price not specified",
                    "status": "available"
                }

                # Save the listing to CSV
                listing_id = save_listing(listing_data)

                st.success(f"✅ Listing '{title}' posted successfully! (ID: {listing_id})")
                st.balloons()
                st.info("💡 Your listing has been saved to the database and is now visible to other users.")

                # Refresh the page to show the new listing
                st.rerun()

                # Show preview of what was submitted
                with st.expander("👁️ Preview Your Listing"):
                    st.markdown(f"**Title:** {title}")
                    st.markdown(f"**Type:** {listing_type}")
                    st.markdown(f"**Price:** {price if price else 'Not specified'}")
                    st.markdown(f"**Location:** {location if location else 'Not specified'}")
                    st.markdown(f"**Description:** {description if description else 'No description'}")
                    st.markdown(f"**Posted by:** {st.session_state.current_user.get('name', 'Current User')}")

# Campus resources section
st.markdown("---")
st.subheader("🌟 Campus Resources")
st.caption("Quick access to IIT Delhi services")

col1, col2, col3, col4 = st.columns(4)

with col1:
    with st.expander("🏫 Housing Office"):
        st.markdown("""
        **Contact Information:**
        - Email: housing@iitd.ac.in
        - Phone: +91-11-2659-1234
        - Office: Block IV, Ground Floor
        
        **Services:**
        - Room allocation
        - Hostel complaints
        - AC/furniture repairs
        """)

with col2:
    with st.expander("📚 Central Library"):
        st.markdown("""
        **Timings:**
        - Mon-Fri: 8:00 AM - 12:00 AM
        - Sat-Sun: 9:00 AM - 10:00 PM
        
        **Services:**
        - Book issue/return
        - Study rooms booking
        - Digital resources
        
        **Location:** Near Main Gate
        """)

with col3:
    with st.expander("🛍️ Campus Store"):
        st.markdown("""
        **Timings:** 9:00 AM - 6:00 PM (Mon-Sat)
        
        **Available Items:**
        - Stationery supplies
        - Electronics accessories
        - IIT Delhi merchandise
        
        **Location:** Student Activity Center
        """)

with col4:
    with st.expander("❓ Help Desk"):
        st.markdown("""
        **Contact:**
        - Email: helpdesk@iitd.ac.in
        - Campus Ext: 1234
        
        **For Issues:**
        - Internet/WiFi problems
        - ID card issues
        - General complaints
        """)