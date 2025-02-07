from typing import Optional
import streamlit as st
import re


def is_valid_email(email: str):
    """Validate email using regex."""
    
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email)


def text_input_component(
    label: str, 
    placeholder: Optional[str] = "Enter text", 
    value: Optional[str] = None, 
    required: bool=True, 
    disabled: bool=False, 
    type: Optional[str] = 'default'  # default, email, password
):
    
    text = st.text_input(
        label if not required else f"{label} *", 
        placeholder=placeholder, 
        value=value, 
        type=type, 
        disabled=disabled,
    )
    
    if type == 'email' and not is_valid_email(text):
        st.error("Please enter a valid email address.")
        return
    
    if required and (not text or text == ""):
        st.error(f"The {label} field is required.")
        return
    
    return text


def password_input_component(
    label: str
):
    password = text_input_component(
        label,
        type='password',
        placeholder="Enter a secure password",
        required=True,
        disabled=False,
    )
    return password