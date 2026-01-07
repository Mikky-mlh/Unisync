def get_user_by_id(user_id, users):
    """Find user by ID"""
    for user in users:
        if user.get('id') == user_id:
            return user
    return None

def calculate_compatibility(user1, user2):
    """Simple compatibility score (0-100)"""
    score = 0
    # Match by major
    if user1.get('major') == user2.get('major'):
        score += 30
    
    # Match by interests (simple word match)
    interests1 = user1.get('interests', '').lower().split(',')
    interests2 = user2.get('interests', '').lower().split(',')
    common = set(interests1) & set(interests2)
    score += len(common) * 10
    
    # Skill exchange match
    if user1.get('can_teach') and user2.get('wants_to_learn'):
        # Check if user1 can teach something user2 wants to learn
        teach1 = [s.strip().lower() for s in user1['can_teach'].split(',')]
        learn2 = [s.strip().lower() for s in user2['wants_to_learn'].split(',')]
        if any(t in learn2 for t in teach1):
            score += 40
    
    return min(score, 100)

def format_email_link(email):
    """Create mailto link"""
    return f'<a href="mailto:{email}">{email}</a>'