import re
import joblib


class CustomPredictionService:
    def __init__(self):
        # Load the model and vectorizer
        self.model = joblib.load("models/sentiment_model.pkl")
        self.vectorizer = joblib.load("models/tfidf_vectorizer.pkl")

    def make_prediction(self, text: str):
        def clean_text(text: str):
            text = text.lower()  # Lowercase
            text = re.sub(r'\W+', ' ', text)  # Remove non-word characters
            return text
        
        # Apply the same preprocessing to the input text to match the model's input format (TF-IDF)
        text = clean_text(text)  # Apply the same preprocessing
        text_tfidf = self.vectorizer.transform([text])
        prediction = int(self.model.predict(text_tfidf)[0]) + 1
        
        prediction_str = ""
        if prediction == 1:
            prediction_str = "Negative"
        elif prediction == 2:
            prediction_str = "Positive"
            
        return prediction_str, prediction


custom_prediction_service = CustomPredictionService()
