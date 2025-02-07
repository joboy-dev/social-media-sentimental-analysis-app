import streamlit as st

from services.auth_service import auth_service


db = st.session_state['db']

st.title('🔑 Login')

# Registration form
with st.form("login_form"):
    email = st.text_input("Email", placeholder="your@email.com").strip()
    password = st.text_input("Password", type="password", placeholder="Enter a secure password").strip()
    
    submit = st.form_submit_button("Login")

# Handle form submission
if submit:
    auth_service.authenticate(db, email, password)
