import streamlit as st
from sqlalchemy.orm import Session

from database.models.sentiment_analysis import SentimentAnalysis
from utils.messages import generate_message


class SentimentalAnalysisService:
    
    def create(self, db: Session, label_str: str, label: int, text: str):
        SentimentAnalysis.create(
            db,
            label_str=label_str,
            label=label,
            text=text,
            user_id=st.session_state.current_user.id
        )
        st.success(generate_message("Prediction saved successfully"))
    
    def get_all(self, db: Session):
        query = db.query(SentimentAnalysis).order_by(SentimentAnalysis.created_at.desc())
        sentiments = query.all()
        return sentiments

    def get_by_id(self, db: Session, id: str):
        sentiment = db.get(SentimentAnalysis, id)
        return sentiment


sentiment_analysis_service = SentimentalAnalysisService()
