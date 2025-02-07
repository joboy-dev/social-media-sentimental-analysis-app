import time
import fasttext, streamlit as st
from database.conn import create_database, load_db
from app.run import load_pages
from services.fasttext_prediction_service import fasttext_prediction
from utils.messages import generate_message


@st.cache_resource
def load_fasttext_model():
    message = st.empty()
    
    print('Loading fasttext model')
    message.info(generate_message("⚡Loading FastText model in the background... Please wait.", "info"))
    
    model = fasttext.load_model('models/fasttext-sentiment-model-quantized.ftz')
    
    print('Model loaded')
    message.success(generate_message("Model loaded successfully!"))
    
    # Wait for 3 seconds
    time.sleep(0.5)

    # Clear the message
    message.empty()
    
    return model


if __name__ == "__main__":
    # Create database tables
    create_database()
    
    # Load database in streamlit cache
    load_db()
    
    # Load all pages and run the app
    load_pages()
    
    # Load model
    model= load_fasttext_model()
    st.session_state['fasttext_model'] = model
