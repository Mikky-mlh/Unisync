import pandas as pd
import os

def init_data():  # Initialize data files if they don't exist
    
    os.makedirs("data", exist_ok=True)  # Create data directory
    
    if not os.path.exists("data/users.csv") or os.path.getsize("data/users.csv") == 0:  # Create users CSV with sample data
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
    
    if not os.path.exists("data/listings.csv") or os.path.getsize("data/listings.csv") == 0:  # Create listings CSV with sample data
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

def load_users():  # Load users from CSV
    try:
        if os.path.exists("data/users.csv"):
            return pd.read_csv("data/users.csv").to_dict('records')
    except:
        pass
    return []

def load_listings():  # Load listings from CSV
    try:
        if os.path.exists("data/listings.csv"):
            return pd.read_csv("data/listings.csv").to_dict('records')
    except:
        pass
    return []

def save_user(user_data):  # Save new user to CSV
    df = pd.read_csv("data/users.csv")
    new_id = len(df) + 1
    user_data['id'] = new_id
    df = pd.concat([df, pd.DataFrame([user_data])], ignore_index=True)
    df.to_csv("data/users.csv", index=False)
    return new_id

def load_passwords():  # Load passwords from CSV
    try:
        if os.path.exists("data/passwords.csv"):
            return pd.read_csv("data/passwords.csv").to_dict('records')
    except:
        pass
    return []

def save_password(email, password):  # Save password to CSV
    if os.path.exists("data/passwords.csv"):
        df = pd.read_csv("data/passwords.csv")
    else:
        df = pd.DataFrame(columns=['email', 'password'])
    
    new_entry = pd.DataFrame([{'email': email, 'password': password}])
    df = pd.concat([df, new_entry], ignore_index=True)
    df.to_csv("data/passwords.csv", index=False)

def verify_password(email, password):  # Verify login credentials
    passwords = load_passwords()
    for entry in passwords:
        if entry.get('email', '').lower() == email.lower() and entry.get('password') == password:
            return True
    return False

def save_connection(user1_id, user2_id, connection_type):  # Save connection to CSV
    import pandas as pd
    from datetime import datetime
    
    if not os.path.exists("data/connections.csv"):
        df = pd.DataFrame(columns=['user1_id', 'user2_id', 'connection_type', 'timestamp'])
    else:
        df = pd.read_csv("data/connections.csv")
    
    new_connection = {
        'user1_id': user1_id,
        'user2_id': user2_id,
        'connection_type': connection_type,
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    df = pd.concat([df, pd.DataFrame([new_connection])], ignore_index=True)
    df.to_csv("data/connections.csv", index=False)

def save_listing(listing_data):  # Save listing to CSV
    if os.path.exists("data/listings.csv"):
        df = pd.read_csv("data/listings.csv")
        new_id = len(df) + 1
    else:
        df = pd.DataFrame(columns=["id", "user_id", "type", "title", "description", "location", "price", "status"])
        new_id = 1

    listing_data['id'] = new_id
    df = pd.concat([df, pd.DataFrame([listing_data])], ignore_index=True)
    df.to_csv("data/listings.csv", index=False)
    return new_id

def get_user_connections(user_id):  # Get all connections for a user
    if not os.path.exists("data/connections.csv"):
        return []

    df = pd.read_csv("data/connections.csv")
    connections = df[(df['user1_id'] == user_id) | (df['user2_id'] == user_id)]
    return connections.to_dict('records')

def save_rating(rater_id, rated_id, rating, review=""):  # Save rating to CSV
    from datetime import datetime
    
    if not os.path.exists("data/ratings.csv"):
        df = pd.DataFrame(columns=['rater_id', 'rated_id', 'rating', 'review', 'timestamp'])
    else:
        df = pd.read_csv("data/ratings.csv")
    
    existing = df[(df['rater_id'] == rater_id) & (df['rated_id'] == rated_id)]
    if not existing.empty:
        df.loc[(df['rater_id'] == rater_id) & (df['rated_id'] == rated_id), 'rating'] = rating
        df.loc[(df['rater_id'] == rater_id) & (df['rated_id'] == rated_id), 'review'] = review
        df.loc[(df['rater_id'] == rater_id) & (df['rated_id'] == rated_id), 'timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    else:
        new_rating = {
            'rater_id': rater_id,
            'rated_id': rated_id,
            'rating': rating,
            'review': review,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        df = pd.concat([df, pd.DataFrame([new_rating])], ignore_index=True)
    
    df.to_csv("data/ratings.csv", index=False)

def get_user_rating(user_id):  # Get average rating for a user
    if not os.path.exists("data/ratings.csv"):
        return 0, 0
    
    df = pd.read_csv("data/ratings.csv")
    user_ratings = df[df['rated_id'] == user_id]
    
    if user_ratings.empty:
        return 0, 0
    
    avg_rating = user_ratings['rating'].mean()
    num_ratings = len(user_ratings)
    
    return round(avg_rating, 1), num_ratings

def get_user_reviews(user_id):  # Get all reviews for a user
    if not os.path.exists("data/ratings.csv"):
        return []
    
    df = pd.read_csv("data/ratings.csv")
    reviews = df[df['rated_id'] == user_id]
    return reviews.to_dict('records')