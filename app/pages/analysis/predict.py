import streamlit as st

from services.sentiment_analysis_service import sentiment_analysis_service
from services.fasttext_prediction_service import fasttext_prediction
from utils.messages import generate_message


db = st.session_state['db']

st.title('📈 Predict Sentimental Analysis')

tab1, tab2 = st.tabs(['Single', 'Batch'])


with tab1:
    # Prediction form
    st.subheader("Enter text to predict sentiment")
    with st.form("prediction_form"):
        text = st.text_input("Text", placeholder="Enter text").strip()
        # st.markdown('<b>Air Quality Index</b>', unsafe_allow_html=True)    
        
        submit = st.form_submit_button("Make Prediction")

    # Handle form submission
    if submit:
        # Make prediction
        prediction_str, prediction = fasttext_prediction.make_prediction(text)
        
        # Save prediction to database
        sentiment_analysis_service.create(
            db,
            label_str=prediction_str,
            label=prediction,
            text=text,
        )
        
        # Display prediction
        if prediction_str == 'Positive':
            st.success(f"Predicted sentiment: {prediction_str}")
        elif prediction_str == 'Negative':
            st.error(f"Predicted sentiment: {prediction_str}")
        else:
            st.info(f"Predicted sentiment: {prediction_str}")
    

with tab2:
    # Batch analysis form
    st.subheader('Upload file to do batch sentimental analysis all at once')
    st.write('The file should contain reviews for your brand products each separated by a new line')
    with st.form('batch_analysis_form'):
        file = st.file_uploader("Upload CSV file", type=["csv", "txt", "pdf"])
        doc = None
        
        if file is not None:
            # Read CSV
            if file.type == "text/csv":
                import pandas as pd
                df = pd.read_csv(file)
                st.write("📊 Preview of CSV:")
                st.dataframe(df, height=2000, use_container_width=True)

            # Read Text File
            elif file.type == "text/plain":
                content = file.read().decode("utf-8")
                doc = st.text_area("📜 File Content", content, height=200, disabled=True)
            
            # Read PDF
            elif file.type == "application/pdf":
                import PyPDF2
                reader = PyPDF2.PdfReader(file)
                text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
                doc = st.text_area("📜 Extracted PDF Text", text, height=200, disabled=True)
            
        else:
            st.warning(generate_message("Please upload a file.", "warning"))
        
        submit_batch = st.form_submit_button("Batch Analysis")
    

