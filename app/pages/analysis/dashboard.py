import streamlit as st
import pandas as pd
import plotly.express as px

from services.sentiment_analysis_service import sentiment_analysis_service


db = st.session_state['db']

st.title('📊 Dashboard')

# Display sentiment history
sentiments = sentiment_analysis_service.get_all(db)

data = [
    {"Text": sentiment.text, "Label": sentiment.label_str, "Label ID": sentiment.label}
    for sentiment in sentiments if sentiment.user_id == st.session_state.current_user.id
]


if data:
    tab1, tab2 = st.tabs(['Charts', 'History'])
    
    with tab1:        
        # Group by sentiment and count occurrences
        df = pd.DataFrame(data)
        sentiment_counts = df["Label"].value_counts().reset_index()
        
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Bar Chart")
            bar_chart = px.bar(sentiment_counts, x="Label", y="count", color="Label", title="Sentiment Count")
            st.plotly_chart(bar_chart, use_container_width=True)

        # Pie Chart
        with col2:
            st.subheader("Pie Chart")
            pie_chart = px.pie(sentiment_counts, names="Label", values="count", title="Sentiment Distribution")
            st.plotly_chart(pie_chart, use_container_width=True)
    
    with tab2:    
        st.subheader("Prediction History")
        st.dataframe(data, use_container_width=True)
else:
    st.info("No prediction history found.")