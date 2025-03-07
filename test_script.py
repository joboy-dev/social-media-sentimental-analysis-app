# Run the following commands
# pip install emoji fasttext joblib numpy==1.26.4
# python3 test_script.py

import re
import emoji
import joblib
import fasttext
import numpy as np


class FasttextPrediction:
    
    def __init__(self, model_name: str):
        self.model_path = f'{model_name}.ftz'
    
    def load_model(self):
        return fasttext.load_model(self.model_path)
        
    def make_prediction(self, text: str):
        model = self.load_model()
        
        labels, probabilities = model.predict(text)
        
        prediction = int(labels[0].split('__')[-1])  # 2 for positive and 1 for negative and 0 for neutral in case
        prediction_str = ""
        
        if prediction == 2:
            prediction_str = "Positive"
        elif prediction == 1:
            prediction_str = "Negative"
            
        return prediction_str, prediction

class CustomPredictionService:
    def __init__(self):
        # Load the model and vectorizer
        self.model = joblib.load("sentiment_model.pkl")
        self.vectorizer = joblib.load("tfidf_vectorizer.pkl")

    def make_prediction(self, text: str):
        def clean_text(text: str):
            text = text.lower()  # Convert to lowercase
            text = re.sub(r'\W+', ' ', text)  # Remove non-word characters
            text = re.sub(r'\d+', '', text)  # Remove numbers
            text = re.sub(r'\s+', ' ', text).strip()  # Remove extra spaces
            text = re.sub(r"http\S+|www\S+", "", text)  # Remove URLs
            text = re.sub(r"#\w+", "", text)  # Remove hashtags
            text = re.sub(r"@\w+", "", text)  # Remove mentions
            text = re.sub(r"[^\w\s]", "", text)  # Remove special characters
            text = emoji.replace_emoji(text, replace="")  # Remove emojis
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


if __name__ == '__main__':
    fasttext_prediction = FasttextPrediction(model_name='fasttext-sentiment-model-quantized')
    custom_prediction_service = CustomPredictionService()

    text = input("Enter text to predict sentiment: ")
    
    print('Fasttext prediction')
    prediction_str, prediction = fasttext_prediction.make_prediction(text)
    print(f'Sentimental analysis prediction: {prediction_str}\n')

    print("Custom prediction")
    prediction_str, prediction = custom_prediction_service.make_prediction(text)
    print(f'Sentimental analysis prediction: {prediction_str}\n')
