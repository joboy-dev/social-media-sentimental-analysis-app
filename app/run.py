import streamlit as st

from services.auth_service import auth_service

def load_pages():
    pages = [
        {"page": "app/pages/auth/register.py", "title": "Register", "url_path": "/register", "icon": "📝"},
        {"page": "app/pages/auth/login.py", "title": "Login", "url_path": "/login", "icon": "🔑"},
        {"page": "app/pages/analysis/dashboard.py", "title": "Dashboard", "url_path": "/", "icon": "📊"},
        {"page": "app/pages/analysis/predict.py", "title": "Make Prediction", "url_path": "/predict", "icon": "📈"},
        {"page": "app/pages/user/settings.py", "title": "Profile Settings", "url_path": "/profile-settings", "icon": "👤"},
        {"page": "app/pages/auth/logout.py", "title": "Logout", "url_path": "/logout", "icon": "🚪"},
    ]
    
     # Filter out login and register if the user is authenticated
    if auth_service.is_authenticated():
        pages = [p for p in pages if p["title"] not in ["Login", "Register"]]
    else:
        pages = [p for p in pages if p["title"] not in ["Logout", "Analysis Details", "Profile Settings", "Make Prediction", "Dashboard",]]

    # Convert to Streamlit Page objects
    st_pages = [st.Page(page=p["page"], title=p["title"], url_path=p["url_path"], icon=p['icon']) for p in pages]

    # Navigation
    pg = st.navigation(st_pages)
    pg.run()
