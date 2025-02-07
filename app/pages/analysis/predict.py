import streamlit as st
import threading

from database.conn import load_db
from services.sentiment_analysis_service import sentiment_analysis_service
from services.fasttext_prediction_service import fasttext_prediction
from utils.messages import generate_message
from services.auth_service import auth_service


auth_service.protect_page()
db = load_db()
user = st.session_state['current_user']

st.title('📈 Predict Sentimental Analysis')

tab1, tab2 = st.tabs(['Single', 'Batch'])

with tab1:
    # Prediction form
    st.subheader("Enter text to predict sentiment")
    with st.form("prediction_form"):
        text = st.text_input("Text", placeholder="Enter text").strip()        
        submit = st.form_submit_button("Make Prediction", type='primary')

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
            user_id=user.id
        )
        
        # Display prediction
        if prediction_str == 'Positive':
            st.success(f"Predicted sentiment: {prediction_str}")
        elif prediction_str == 'Negative':
            st.error(f"Predicted sentiment: {prediction_str}")
        else:
            st.info(f"Predicted sentiment: {prediction_str}")
    

with tab2:
    # def add_text_to_doc_list(doc: List, test: str):
    #     doc.append(test)

    st.subheader('Conduct batch analysis')
    st.write('All reviews should be put on a separate line')
    
    with st.form('batch_analysis_form'):
        
        doc = st.text_area('Text (separated by a new line)', height=200)
        
        submit_batch_button = st.form_submit_button("Batch Analysis", type='primary')
        
        if submit_batch_button:
            # Start processing in the background
            # thread = threading.Thread(target=batch_analysis, args=(doc,))
            # thread.start()
            
            # st.success(generate_message("Batch analysis started"))
            threading.Thread(target=lambda: sentiment_analysis_service.batch_analysis(db, doc, user.id)).start()
            st.success(generate_message("Batch analysis started"))
            
        
    st.divider()
    
    # Batch analysis form
    st.subheader('Upload file to do batch sentimental analysis all at once')
    st.write('The file should contain reviews for your brand products each separated by a new line')
    
    with st.form('file_batch_analysis_form'):
        file = st.file_uploader("Upload CSV file", type=["txt", "pdf"])
        doc = None
        
        if file is not None:
            # Read CSV
            # if file.type == "text/csv":
            #     import pandas as pd
            #     df = pd.read_csv(file)
            #     st.write("📊 Preview of CSV:")
            #     st.dataframe(df, height=2000, use_container_width=True)

            # Read Text File
            if file.type == "text/plain":
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
        
        submit_batch_button = st.form_submit_button("Batch Analysis", type='primary')
        
        if submit_batch_button:
            # Start processing in the background
            threading.Thread(target=lambda: sentiment_analysis_service.batch_analysis(db, doc, user.id)).start()
            st.success(generate_message("Batch analysis started"))
