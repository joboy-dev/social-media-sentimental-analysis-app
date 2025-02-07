import re
import time
from typing import Optional
import streamlit as st
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from database.models.user import User
from utils.messages import generate_message


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    
    def is_authenticated(self):
        return st.session_state.get("current_user", None)
    
    def hash_password(self, password: str):
        return pwd_context.hash(password)
    
    def verify_password(self, password: str, hash: str):
        return pwd_context.verify(password, hash)
    
    def is_valid_email(self, email):
        """Validate email using regex."""
        
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        return re.match(pattern, email)

    def authenticate(self, db: Session, email: str, password: str):
        st.session_state['current_user'] = None
        
        if not self.is_valid_email(email):
            st.error(generate_message("Invalid email format!", "error"))
            return
        
        # user = User.fetch_one_by_field(db, email=email)
        user = db.query(User).filter(User.email == email).first()
        
        if not user:
            print('User not found')
            st.error(generate_message("Invalid credentials!", "error"))
            return
        
        if not self.verify_password(password, user.password):
            print('Password validation failed')
            st.error(generate_message("Invalid credentials", "error"))
            return
        
        st.session_state['current_user'] = user
        time.sleep(0.5)
        st.switch_page(st.Page('app/pages/analysis/dashboard.py'))
    
    def register(self, db: Session, name: Optional[str], email: str, password: str, confirm_password: str):
        st.session_state['current_user'] = None
        
        if not email or not password:
            st.error(generate_message("Both email and password are required!", "error"))
            return

        if not self.is_valid_email(email):
            st.error(generate_message("Invalid email format!", "error"))
            return
        
        if password != confirm_password:
            st.error(generate_message("Passwords do not match!", "error"))
            return
        
        if User.fetch_one_by_field(db, email=email):
            st.error(generate_message("User with email already exists!", 'error'))
            return
        
        hashed_password = self.hash_password(password)
        
        user = User(name=name, email=email, password=hashed_password)
        db.add(user)
        db.commit()
        db.refresh(user)
        
        st.session_state['current_user'] = user
        st.success(generate_message(f"Successfully registered with {email}!"))
        time.sleep(0.5)
        st.switch_page(st.Page('app/pages/analysis/dashboard.py'))
    
    def logout(self):
        st.session_state.pop('current_user', None)
        st.success(generate_message("Logged out successfully!"))
        
        time.sleep(0.5)
        st.rerun()


# Instantiate the AuthService
auth_service = AuthService()
