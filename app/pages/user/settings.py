import streamlit as st
from database.conn import load_db
from services.user_service import user_service
from utils.messages import generate_message
from services.auth_service import auth_service


auth_service.protect_page()
db = load_db()
current_user = st.session_state.current_user

st.title('👤⚙️ Profile Settings')

tab1, tab2, tab3, tab4 = st.tabs(['Profile', 'Edit Profile', 'Update Profile Picture', 'Update Password'])

with tab1:
    
    user_data = {
        "name": st.session_state.current_user.name,
        "email": st.session_state.current_user.email,
        "profile_pic": st.session_state.current_user.profile_picture  # Placeholder profile picture
    }

    # UI Styling
    st.markdown(
        """
        <style>
            .profile-container {
                text-align: center;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
                max-width: 400px;
                margin: auto;
            }
            .profile-pic {
                border-radius: 50%;
                width: 120px;
                height: 120px;
                object-fit: cover;
                border: 4px solid #4CAF50;
            }
            .profile-name {
                font-size: 24px;
                font-weight: bold;
                margin-top: 15px;
            }
            .profile-email {
                font-size: 16px;
                color: gray;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Profile Section
    st.markdown('<div class="profile-container">', unsafe_allow_html=True)

    st.image(user_data["profile_pic"], caption="", width=120)

    st.markdown(f'<p class="profile-name">{user_data["name"]}</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="profile-email">{user_data["email"]}</p>', unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
    
with tab2:
    st.subheader("Edit Profile")
    with st.form("edit_profile"):
        name = st.text_input("Full Name", value=current_user.name).strip()
        email = st.text_input("Email", value=current_user.email).strip()
        
        edit_profile_submit = st.form_submit_button("Save Changes", type='primary')

    if edit_profile_submit:
        user_service.update_profile(db, name=name, email=email, profile_picture_file=None)


with tab3:
    st.subheader("Change Profile Picture")
    with st.form('change_profile_picture'):
        st.image(st.session_state.current_user.profile_picture, width=150)
        # uploaded_file = file_upload_component(db, label="Upload Picture", allowed_types=["png", "jpg", "jpeg"])
        uploaded_file = st.file_uploader("Upload Picture", type=["png", "jpg", "jpeg"])
        
        if uploaded_file is not None:
            st.success(generate_message("File uploaded successfully"))

            # Display Image
            if uploaded_file.type.startswith("image/"):
                st.image(uploaded_file, caption="Uploaded Image", width=150)
            
        else:
            st.warning(generate_message("Please upload a file.", "warning"))

        edit_profile_submit = st.form_submit_button("Save Changes", type='primary')

        if edit_profile_submit:
            user_service.update_profile(db, name=None, email=None, profile_picture_file=uploaded_file)
        
        
with tab4:
    st.subheader("Update Password")
    with st.form("update_password"):
        email = st.text_input("Email", value=current_user.email, disabled=True)
        old_password = st.text_input("Old Password", type='password', placeholder="Enter a secure password").strip()
        new_password = st.text_input("New Password", type='password', placeholder="Enter a secure password").strip()
        confirm_password = st.text_input("Confirm Password", type='password', placeholder="Enter a secure password").strip()
        
        update_password_submit = st.form_submit_button("Save Changes", type='primary')

    if update_password_submit:
        user_service.change_password(db, email=email, old=old_password, new=new_password, confirm=confirm_password)
        