from pprint import pprint
import streamlit as st
import pandas as pd
import plotly.express as px

from database.conn import load_db
from services.sentiment_analysis_service import sentiment_analysis_service
from services.auth_service import auth_service


auth_service.protect_page()
db = load_db()

st.title('📊 Dashboard')

# Display sentiment history
sentiments = sentiment_analysis_service.get_all(db)

if sentiments:
    data = [
        {"text": sentiment.text, "label": sentiment.label_str, "label_id": sentiment.label}
        for sentiment in sentiments if sentiment.user_id == st.session_state.current_user.id
    ]
    
    batch_sentiments = sentiment_analysis_service.get_all_batch(db)
    
    batch_data = [
        batch_sentiment
        for batch_sentiment in batch_sentiments if batch_sentiment.user_id == st.session_state.current_user.id
    ]
    
    # Set up tab screens
    tab1, tab2, tab3 = st.tabs(['Overall Analysis', 'Batch Analysis', 'History'])
    
    with tab1:        
        # Group by sentiment and count occurrences
        df = pd.DataFrame(data)
        sentiment_counts = df["label"].value_counts().reset_index()
        
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Bar Chart")
            bar_chart = px.bar(sentiment_counts, x="label", y="count", color="label", title="Sentiment Count")
            st.plotly_chart(bar_chart, use_container_width=True)

        # Pie Chart
        with col2:
            st.subheader("Pie Chart")
            pie_chart = px.pie(sentiment_counts, names="label", values="count", title="Sentiment Distribution")
            st.plotly_chart(pie_chart, use_container_width=True)


    with tab2:
        # Initialize session state if not set
        if "show_details" not in st.session_state:
            st.session_state.show_details = {}
            
        st.subheader("Batch Analysis History")

        for batch in batch_data:
            batch_id = batch.id
            clean_data = [
                {
                    "text": d["text"],
                    "label": d["label"],
                    "label_id": d["label_id"]
                } for d in batch.data
            ]
            df = pd.DataFrame(clean_data)

            with st.expander(f"Analysis of {len(batch.data)} reviews conducted on {batch.created_at}"):
                subtab1, subtab2 = st.tabs(['Chart', 'Table'])
                with subtab1:
                    st.write(f"**Visual Analysis**")
                    
                    # Group by sentiment and count occurrences
                    sentiment_counts = df["label"].value_counts().reset_index()
                    
                    col1, col2 = st.columns(2)

                    with col1:
                        st.subheader("Bar Chart")
                        bar_chart = px.bar(sentiment_counts, x="label", y="count", color="label", title="Sentiment Count")
                        st.plotly_chart(bar_chart, use_container_width=True)

                    # Pie Chart
                    with col2:
                        st.subheader("Pie Chart")
                        pie_chart = px.pie(sentiment_counts, names="label", values="count", title="Sentiment Distribution")
                        st.plotly_chart(pie_chart, use_container_width=True)
                
                with subtab2:
                    st.write(f"**Detailed Analysis**")
                    st.dataframe(df, use_container_width=True)

    with tab3:    
        st.subheader("Prediction History")
        st.dataframe(data, use_container_width=True)
else:
    st.info("No prediction history found.")