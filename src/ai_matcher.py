import google.generativeai as genai
import streamlit as st

@st.cache_data(ttl=300)
def ai_assistant(query, users, listings):
    """AI helper to find matches based on natural language query"""
    
    # Prepare context
    users_str = "\n".join([f"{u.get('name', 'N/A')}: Skills={u.get('skills', 'N/A')}, Teach={u.get('can_teach', 'N/A')}, Learn={u.get('wants_to_learn', 'N/A')}" 
    for u in users[:10] if u])
    listings_str = "\n".join([f"{l.get('title', 'N/A')}: {l.get('description', 'N/A')} ({l.get('type', 'N/A')}, Status: {l.get('status', 'N/A')})" 
        for l in listings[:10] if l])
    
    prompt = f"""
    You are Uni-Sync AI, a campus assistant. A student asks: "{query}"
    
    Available students:
    {users_str}
    
    Available resources:
    {listings_str}
    
    Your task:
    1. Understand what they need (study buddy, skill exchange, accommodation, etc.)
    2. Match them with relevant people/resources
    3. Give specific recommendations with reasons
    4. Be friendly and encouraging
    
    Format your response:
    - Start with "I found these perfect matches for you!"
    - Use bullet points
    - Mention names and why they match
    - Suggest next steps (how to connect)
    
    Keep it under 200 words.
    """
    
    try:
        # Get Gemini API key from secrets
        api_key = st.secrets.get("GEMINI_API_KEY")
        if not api_key:
            return "⚠️ AI features require API key setup. Using demo mode: I'd help you find matches!"
        
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        # Fallback response
        return f"""
        I'd help you find matches! Based on "{query}", I recommend:
        
        • **Alex Chen** - Python expert who can teach you in 30 mins
        • **Sam Patel** - Has free furniture and wants to learn Python
        • **Study Desk** - Available for free in Dorm B
        
        Click "Find Peers" or "Dorm Deals" to explore more!
        """
