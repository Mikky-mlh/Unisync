import streamlit as st
import sys
import os
import streamlit.components.v1 as components  # Import components for JS execution

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  # Add parent directory to path

from src.data_manager import load_listings, load_users, save_listing
import pandas as pd
import re
import urllib.parse

if 'current_user' not in st.session_state:
    st.session_state.current_user = None

st.set_page_config(page_title="Dorm Deals", page_icon="🏢", layout="wide")  # Configure page

if 'current_user' not in st.session_state or st.session_state.current_user is None:  # Check authentication
    st.warning("🔒 Please login from the Home page to access Dorm Deals")
    st.stop()

try:
    with open("assets/style-dorm.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
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
    background: linear-gradient(180deg, #14b8a6, #06b6d4) !important;
    border-radius: 10px !important;
    border: 3px solid #0a0a0f !important;
}
.custom-scroll::-webkit-scrollbar-thumb:hover {
    background: #14b8a6 !important;
    box-shadow: 0 0 10px rgba(20, 184, 166, 0.5) !important;
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

# Helper function to create listing card HTML
def listing_card(listing_type, listing_status, title, description, poster_name, location, price):
    return f"""<div class="listing-card">
<div class="listing-header">
<span class="listing-type">{listing_type.upper()}</span>
<span class="listing-status">{listing_status.upper()}</span></div>
<h3 class="listing-title">{title}</h3>
<p class="listing-desc">{description}</p>
<div class="listing-details">
<p>👤 <strong>Posted by:</strong> {poster_name}</p>
<p>📍 <strong>Location:</strong> {location}</p>
<p>💰 <strong>Price:</strong> {price}</p></div></div>"""

st.markdown("""
<div style="text-align: center; margin-bottom: 0.5rem;">
    <h1><span class="emoji-fix">🏢</span> Dorm Deals</h1>
</div>
""", unsafe_allow_html=True)

st.markdown("### Your campus marketplace for rooms, furniture, and resources")
st.caption("💡 Find great deals or post items you want to sell/give away")

listings = load_listings()
users = load_users()

user_map = {}
for user in users:
    user_map[user['id']] = user

st.sidebar.markdown("""
<h3><span class="emoji-fix">🔍</span> Filters</h3>
""", unsafe_allow_html=True)
st.sidebar.caption("Narrow down your search")

type_options = ["All", "room", "furniture", "textbook", "electronics", "other"]  # Available filter options
selected_type = st.sidebar.selectbox("🏷️ Item Type", type_options)

if listings:  # Calculate price range from listings
    prices = []
    for l in listings:
        price_str = str(l.get('price', '0'))
        if price_str.lower() == 'free':
            prices.append(0)
        else:
            # Extract numbers from price string
            numbers = re.findall(r'\d+', price_str)
            if numbers:
                prices.append(int(numbers[0]))
            else:
                prices.append(0)

    max_price = max(prices) if prices else 1000
    price_range = st.sidebar.slider("💰 Price Range", 0, max_price, (0, max_price))
else:
    price_range = (0, 1000)

location_search = st.sidebar.text_input("📍 Location", placeholder="e.g., Dorm B")  # Location filter

free_only = st.sidebar.checkbox("✅ Free items only")  # Free items filter

st.sidebar.markdown("---")
st.sidebar.info(f"📊 Showing {len(listings)} listings")

filtered_listings = []  # Apply all filters

for listing in listings:
    if selected_type != "All" and listing.get('type', '').lower() != selected_type.lower():
        continue

    price_str = str(listing.get('price', '0'))  # Extract price value
    price_val = 0

    if 'free' in price_str.lower():
        price_val = 0
    else:
        numbers = re.findall(r'\d+', price_str)
        if numbers:
            numbers = [int(n) for n in numbers]
            if '-' in price_str and len(numbers) >= 2:
                price_val = int((numbers[0] + numbers[1]) / 2)
            else:
                price_val = numbers[0]
        else:
             price_val = 0
    if price_val < price_range[0] or price_val > price_range[1]:
        continue

    if location_search:  # Filter by location
        loc = str(listing.get('location', '')).lower()
        if location_search.lower() not in loc:
            continue

    if free_only and price_val != 0:  # Filter free items only
        continue

    filtered_listings.append(listing)

st.subheader("📦 Available Listings")  # Display listings section

if not filtered_listings:
    st.warning("😕 No listings match your filters.")
else:
    st.markdown('<div class="listings-grid">', unsafe_allow_html=True)
    cols = st.columns(3)
    for idx, listing in enumerate(filtered_listings):
        with cols[idx % 3]:
            poster_user = user_map.get(listing.get('user_id'))
            poster_name = poster_user.get('name', 'Anonymous') if poster_user else 'Unknown'
            poster_email = poster_user.get('email', '') if poster_user else ''

            st.markdown(listing_card(
                listing.get('type', 'other'),
                listing.get('status', 'available'),
                listing.get('title', 'Untitled'),
                listing.get('description', 'No description'),
                poster_name,
                listing.get('location', 'Not specified'),
                listing.get('price', 'Contact for price')
            ), unsafe_allow_html=True)

            if st.button("👋 I'm Interested", key=f"interest_{listing.get('id')}", use_container_width=True):
                from src.data_manager import save_connection
                save_connection(
                    st.session_state.current_user.get('id'),
                    listing.get('user_id'),
                    f'dorm_interest_{listing.get("id")}'
                )
                
                if poster_email:
                    subject = f"UniSync: Interested in {listing.get('title')}"
                    body = f"Hi {poster_name},\n\nI saw your listing '{listing.get('title')}' on UniSync Dorm Deals and I'm interested!\n\nDetails:\n- Item: {listing.get('title')}\n- Price: {listing.get('price')}\n- Location: {listing.get('location')}\n\nLet's connect!\n\nBest regards,\n{st.session_state.current_user.get('name')}\nEmail: {st.session_state.current_user.get('email')}"
                    mailto_link = f"mailto:{poster_email}?subject={urllib.parse.quote(subject)}&body={urllib.parse.quote(body)}"
                    
                    st.markdown(f'<meta http-equiv="refresh" content="0; url={mailto_link}">', unsafe_allow_html=True)
                    st.success(f"✅ Interest saved! Opening email to {poster_name}...")
                else:
                    st.success("✅ Interest saved!")

    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")  # Section divider
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
        if not title or not listing_type:
            st.error("⚠️ Please fill in all required fields (Title and Type)")
        else:
            from src.data_manager import save_listing
            listing_data = {
                "user_id": st.session_state.current_user.get('id'),
                "type": listing_type,
                "title": title,
                "description": description if description else "No description provided",
                "location": location if location else "Location not specified",
                "price": price if price else "Price not specified",
                "status": "available"
            }

            listing_id = save_listing(listing_data)

            st.success(f"✅ Listing '{title}' posted successfully! (ID: {listing_id})")
            st.balloons()
            st.info("💡 Your listing has been saved to the database and is now visible to other users.")

            st.rerun()

st.markdown("---")  # Section divider
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