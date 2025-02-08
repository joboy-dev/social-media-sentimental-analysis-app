import threading
import fasttext
import streamlit as st
import numpy as np

from utils.messages import generate_message


class FasttextPrediction:
    
    def __init__(self, model_name: str):
        self.model_path = f'models/{model_name}.ftz'
    
    def load_model(self):
        # Function to load the model (cached so it loads once)
        @st.cache_resource
        def load_fasttext_model():
            return fasttext.load_model(self.model_path)

        # Background thread function
        def load_model_thread():
            if "fasttext_model" not in st.session_state:
                print('Loading model')
                model = load_fasttext_model()
                print('Model loaded')
                
                st.success(generate_message("Model loaded successfully!"))
                
                # Once loaded, update the session state
                st.session_state["fasttext_model"] = model

        # Start background loading if the model isn't already in session state
        if "fasttext_model" not in st.session_state:
            thread = threading.Thread(target=load_model_thread, daemon=True)
            thread.start()
            st.info(generate_message("⚡Loading FastText model in the background... Please wait.", "info"))

        
    def make_prediction(self, text: str):
        model = st.session_state["fasttext_model"]
        
        labels, probabilities = model.predict(text)
        # ✅ Fix: Ensure proper NumPy array creation
        # probabilities = np.asarray(probabilities)  # Convert without `copy=False`
        
        prediction = int(labels[0].split('__')[-1])  # 2 for positive and 1 for negative and 0 for neutral in case
        prediction_str = ""
        
        if prediction == 2:
            prediction_str = "Positive"
        elif prediction == 1:
            prediction_str = "Negative"
            
        return prediction_str, prediction


fasttext_prediction = FasttextPrediction(model_name='fasttext-sentiment-model-quantized')
