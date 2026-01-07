import pandas as pd
import os

def init_data():
    """Create sample data files if they don't exist"""
    
    # Create data directory if it doesn't exist
    os.makedirs("data", exist_ok=True)
    
    # Users CSV
    if not os.path.exists("data/users.csv") or os.path.getsize("data/users.csv") == 0:
        sample_users = [
            {
                "id": 1,
                "name": "Alex Chen",
                "email": "alex@campus.edu",
                "year": "Junior",
                "major": "Computer Science",
                "skills": "Python, Machine Learning, Guitar",
                "interests": "AI Research, Music, Hiking",
                "x_factor": "🔥 Can teach Python in 30 mins",
                "can_teach": "Python basics, Guitar chords",
                "wants_to_learn": "Data Visualization, Spanish",
                "accommodation_need": "Looking for room near campus"
            },
            {
                "id": 2,
                "name": "Sam Patel",
                "email": "sam@campus.edu",
                "year": "Sophomore",
                "major": "Business + Design",
                "skills": "UI/UX Design, Public Speaking, Cooking",
                "interests": "Startups, Photography, Basketball",
                "x_factor": "🎤 Won campus debate championship",
                "can_teach": "Figma design, Presentation skills",
                "wants_to_learn": "Data Analysis, Python",
                "accommodation_need": "Has extra furniture to give"
            }
        ]
        pd.DataFrame(sample_users).to_csv("data/users.csv", index=False)
    
    # Listings CSV
    if not os.path.exists("data/listings.csv") or os.path.getsize("data/listings.csv") == 0:
        sample_listings = [
            {
                "id": 1,
                "user_id": 2,
                "type": "furniture",
                "title": "Study Desk with Chair",
                "description": "Good condition, moving out",
                "location": "Dorm B, Block 3",
                "price": "Free",
                "status": "available"
            },
            {
                "id": 2,
                "user_id": 1,
                "type": "room",
                "title": "Room available for sharing",
                "description": "Private room in 3BHK, near campus",
                "location": "10 min from college",
                "price": "$300/month",
                "status": "available"
            }
        ]
        pd.DataFrame(sample_listings).to_csv("data/listings.csv", index=False)

def load_users():
    """Load users from CSV"""
    try:
        if os.path.exists("data/users.csv"):
            return pd.read_csv("data/users.csv").to_dict('records')
    except:
        pass
    return []

def load_listings():
    """Load listings from CSV"""
    try:
        if os.path.exists("data/listings.csv"):
            return pd.read_csv("data/listings.csv").to_dict('records')
    except:
        pass
    return []

def save_user(user_data):
    """Add new user to CSV"""
    df = pd.read_csv("data/users.csv")
    new_id = len(df) + 1
    user_data['id'] = new_id
    df = pd.concat([df, pd.DataFrame([user_data])], ignore_index=True)
    df.to_csv("data/users.csv", index=False)
    return new_id
