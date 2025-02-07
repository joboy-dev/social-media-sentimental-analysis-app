from typing import List
import streamlit as st

from services.user_service import user_service
from utils.messages import generate_message


def file_upload_component(db, label:str, allowed_types: str | List[str], required: bool=False):
    uploaded_file = st.file_uploader(label, type=allowed_types)

    if required and not uploaded_file:
        st.error(generate_message("File is required", "error"))
        return
    
    st.success(generate_message("File uploaded successfully"))

    # Display Image
    if uploaded_file.type.startswith("image/"):
        st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)

    # Read CSV
    elif uploaded_file.type == "text/csv":
        import pandas as pd
        df = pd.read_csv(uploaded_file)
        st.write("📊 Preview of CSV:")
        st.dataframe(df)

    # Read Text File
    elif uploaded_file.type == "text/plain":
        content = uploaded_file.read().decode("utf-8")
        st.text_area("📜 File Content", content, height=200)
    
    # edit_profile_submit = st.form_submit_button("Save Changes")

    # if edit_profile_submit:
    #     user_service.update_profile(db, name=None, email=None, profile_picture_file=uploaded_file)
    
    return uploaded_file

    # Read PDF
    # elif uploaded_file.type == "application/pdf":
    #     import PyPDF2
    #     reader = PyPDF2.PdfReader(uploaded_file)
    #     text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
    #     st.text_area("📜 Extracted PDF Text", text, height=200)
