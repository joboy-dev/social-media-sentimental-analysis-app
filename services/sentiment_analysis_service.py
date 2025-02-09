from typing import List
import streamlit as st
from sqlalchemy.orm import Session

from database.models.sentiment_analysis import BatchSentimentAnalysis, SentimentAnalysis
from utils.messages import generate_message
from services.fasttext_prediction_service import fasttext_prediction


class SentimentalAnalysisService:
    
    def create(self, db: Session, label_str: str, label: int, text: str, user_id: str):
        try:
            sentiment = SentimentAnalysis.create(
                db,
                label_str=label_str,
                label=label,
                text=text,
                user_id=user_id
            )
            st.success(generate_message("Prediction saved successfully"))
            return sentiment
        except Exception as e:
            print(e)
            db.rollback()
            st.error(generate_message('An unexpected error occured. Try again later', 'error'))
        
    def create_batch(self, db: Session, data, user_id: str):
        try:    
            BatchSentimentAnalysis.create(
                db,
                data=data,
                user_id=user_id
            )
            st.success(generate_message("Prediction saved successfully"))
        
        except Exception as e:
            print(e)
            db.rollback()
            st.error(generate_message('An unexpected error occured. Try again later', 'error'))
    
    def get_all(self, db: Session):
        query = db.query(SentimentAnalysis).order_by(SentimentAnalysis.created_at.desc())
        sentiments = query.all()
        return sentiments
    
    def get_all_batch(self, db: Session):
        query = db.query(BatchSentimentAnalysis).order_by(BatchSentimentAnalysis.created_at.desc())
        batch_sentiments = query.all()
        return batch_sentiments

    def get_by_id(self, db: Session, id: str):
        sentiment = db.get(SentimentAnalysis, id)
        return sentiment
    
    def get_batch_by_id(self, db: Session, id: str):
        batch_sentiment = db.get(BatchSentimentAnalysis, id)
        return batch_sentiment
    
    # def batch_analysis(self, db: Session, document: str | List[str], user_id: str):
    def batch_analysis(self, db: Session, document: str | List[str], user_id: str, predict_func):
        if document is None:
            st.error(generate_message("No document provided.", "error"))
            return
        
        if 'fasttext_model' not in st.session_state:
            import fasttext
            print('Loading model')
            model = fasttext.load_model('models/fasttext-sentiment-model-quantized.ftz')
            print('Model loaded successfully!')
            
            # Once loaded, update the session state
            st.session_state['fasttext_model'] = model
        
        data = []
        doc_list = document.split('\n') if isinstance(document, str) else document
        
        for text in doc_list:
            if text.strip()!= '':
                # prediction_str, prediction = fasttext_prediction.make_prediction(text)
                prediction_str, prediction = predict_func(text)
                # Save prediction to database
                sentiment_analysis = self.create(
                    db,
                    label_str=prediction_str,
                    label=prediction,
                    text=text,
                    user_id=user_id
                )
                
                data.append({
                    'id': sentiment_analysis.id,
                    'text': text,
                    'label': prediction_str,
                    'label_id': prediction
                })
                
        
        # Save batch prediction
        self.create_batch(db, data, user_id)
        
        st.success(generate_message("Batch analysis complete. Please check the dashboard for results."))
        

sentiment_analysis_service = SentimentalAnalysisService()
