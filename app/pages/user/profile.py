import streamlit as st


st.title('👤 Profile')

# Profile Picture
st.image(st.session_state.current_user.profile_picture, width=150)

# Display user info
st.subheader(st.session_state.current_user.name)

st.write("Email")
st.write(st.session_state.current_user.email)
