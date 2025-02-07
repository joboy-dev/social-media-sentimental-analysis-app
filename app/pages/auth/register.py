import streamlit as st

from services.auth_service import auth_service


db = st.session_state['db']

st.title("🔐 Register")

# Registration form
with st.form("register_form"):
    name = st.text_input("Full Name (Optional)", placeholder="John Doe").strip()
    email = st.text_input("Email", placeholder="your@email.com").strip()
    password = st.text_input("Password", type="password", placeholder="Enter a secure password").strip()
    confirm_password = st.text_input("Confirm Password", type="password", placeholder="Enter a secure password").strip()
    
    submit = st.form_submit_button("Register")

# Handle form submission
if submit:
    auth_service.register(db, name, email, password, confirm_password)
    
