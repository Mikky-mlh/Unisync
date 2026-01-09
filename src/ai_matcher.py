import google.generativeai as genai
import streamlit as st

if 'api_key_index' not in st.session_state:
    st.session_state.api_key_index = 0

def get_next_api_key():
    keys = [st.secrets.get(f"GEMINI_API_KEY_{i}") for i in range(1, 11)]
    keys = [k for k in keys if k]
    if not keys:
        return None
    key = keys[st.session_state.api_key_index % len(keys)]
    st.session_state.api_key_index += 1
    return key

@st.cache_data(ttl=300)  # Cache results for 5 minutes
def ai_assistant(query, users, listings):
    import csv
    
    users_str = "\n".join([
        f"• {u.get('name')}: Major={u.get('major')}, Year={u.get('year')}, "
        f"Skills={u.get('skills')}, Can teach={u.get('can_teach')}, "
        f"Wants to learn={u.get('wants_to_learn')}, Email={u.get('email')}"
        for u in users if u
    ])
    
    listings_str = "\n".join([
        f"• {l.get('title')}: Type={l.get('type')}, Price={l.get('price')}, "
        f"Location={l.get('location')}, Description={l.get('description')}"
        for l in listings if l
    ])
    
    try:
        with open('data/ratings.csv', 'r') as f:
            ratings = list(csv.DictReader(f))
            ratings_str = "\n".join([f"User {r['rater_id']} rated User {r['rated_id']}: {r['rating']}/5" for r in ratings[:50]])
    except:
        ratings_str = "No ratings available"
    
    prompt = f"""You are Uni-Sync AI, a smart campus matchmaking assistant at IIT Delhi.  # Build AI prompt

Student query: "{query}"

ANALYZE CAREFULLY:
1. What do they need?
   - Study buddy for a specific course?
   - Someone to teach them a skill?
   - Accommodation/room/furniture?
   - Something to buy/sell?

2. Search through ALL available students and listings below

COMPLETE STUDENT DATABASE:
{users_str}

COMPLETE MARKETPLACE LISTINGS:
{listings_str}

USER RATINGS (Trust Scores):
{ratings_str}

YOUR RESPONSE MUST:
1. Find 2-3 BEST matches with SPECIFIC reasons
2. Include full names and contact emails
3. Explain WHY each match is perfect
4. Give actionable next steps

Format:
🎯 Perfect Matches Found!

👤 [Name] ([Major]) - [Specific reason they match]
   📧 Contact: [email]
   💡 Why: [Explain skill overlap or interest alignment]

👤 [Next match...]

📍 Next Steps: [What the student should do]

Keep it under 300 words but be SPECIFIC with names and reasons.
"""
    
    max_retries = 10
    for attempt in range(max_retries):
        try:
            api_key = get_next_api_key()
            if not api_key:
                return "⚠️ AI features require API key. Please configure GEMINI_API_KEY in secrets."
            
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-flash-latest')
            response = model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            if "quota" in str(e).lower() or "rate" in str(e).lower():
                if attempt < max_retries - 1:
                    continue
            return f"⚠️ AI is temporarily unavailable: {str(e)}"