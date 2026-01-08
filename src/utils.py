def get_user_by_id(user_id, users):  # 🔍 Find user by ID
    for user in users:
        if user.get('id') == user_id:
            return user
    return None

def calculate_compatibility(user1, user2):  # 📊 Compatibility score
    score = 0
    if user1.get('major') == user2.get('major'):
        score += 30
    
    interests1 = user1.get('interests', '').lower().split(',')
    interests2 = user2.get('interests', '').lower().split(',')
    common = set(interests1) & set(interests2)
    score += len(common) * 10
    
    if user1.get('can_teach') and user2.get('wants_to_learn'):
        teach1 = [s.strip().lower() for s in user1['can_teach'].split(',')]
        learn2 = [s.strip().lower() for s in user2['wants_to_learn'].split(',')]
        if any(t in learn2 for t in teach1):
            score += 40
    
    return min(score, 100)

def format_email_link(email):  # 📧 Create mailto link
    return f'<a href="mailto:{email}">{email}</a>'