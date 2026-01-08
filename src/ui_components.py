import streamlit as st

def user_card(user_data):  # 🎴 Display user card
    st.markdown(f"""
    <div style="
        border: 2px solid #e0e0e0;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        background: white;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    ">
        <h3 style="margin-top: 0;">{user_data.get('name', 'Anonymous')}</h3>
        <p><strong>🎓 {user_data.get('major', 'Undeclared')}</strong></p>
        <p><strong>🛠️ Skills:</strong> {user_data.get('skills', 'None listed')}</p>
        <p><strong>❤️ Interests:</strong> {user_data.get('interests', 'None listed')}</p>
        <div style="
            background: #fff3cd;
            padding: 0.5rem;
            border-radius: 8px;
            margin: 0.5rem 0;
        ">
            <strong>✨ X-Factor:</strong> {user_data.get('x_factor', 'No special skill')}
        </div>
    </div>
    """, unsafe_allow_html=True)

def skill_card(skill_data, type="teach"):  # 🎯 Display skill card
    if type == "teach":
        st.markdown(f"""
        <div style="
            border-left: 4px solid #28a745;
            padding: 1rem;
            margin: 0.5rem 0;
            background: #f8fff9;
        ">
            <strong>📚 {skill_data['skill']}</strong>
            <p>Taught by: {skill_data['teacher']} ({skill_data.get('teacher_major', '')})</p>
            <small>Special: {skill_data.get('x_factor', '')}</small>
            <br>
            <small>Contact: {skill_data['teacher_email']}</small>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="
            border-left: 4px solid #007bff;
            padding: 1rem;
            margin: 0.5rem 0;
            background: #f0f8ff;
        ">
            <strong>🎯 Wants to learn: {skill_data['skill']}</strong>
            <p>Learner: {skill_data['learner']} ({skill_data.get('learner_major', '')})</p>
            <br>
            <small>Contact: {skill_data['learner_email']}</small>
        </div>
        """, unsafe_allow_html=True)