import google.generativeai as genai
import streamlit as st

@st.cache_data(ttl=300)
def ai_assistant(query, users, listings):
    # Remove the [:10] truncation - use ALL users and listings
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
    
    prompt = f"""You are Uni-Sync AI, a smart campus matchmaking assistant at IIT Delhi.

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
    
    try:
        api_key = st.secrets.get("GEMINI_API_KEY")
        if not api_key:
            return "⚠️ AI features require API key. Please configure GEMINI_API_KEY in secrets."
        
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')  # Use latest model
        response = model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        return f"⚠️ AI is temporarily unavailable: {str(e)}"