import streamlit as st
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base
from sqlalchemy import create_engine


DB_TYPE = st.secrets.db_credentials.db_type
DATABASE_URL = st.secrets.db_credentials.db_url


def get_db_engine():
    return create_engine(DATABASE_URL)

engine = get_db_engine()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

db_session = scoped_session(SessionLocal)

Base = declarative_base()


def create_database():
    from database.models import (
        User, 
        SentimentAnalysis
    )
    
    return Base.metadata.create_all(bind=engine)


def get_db():
    db = db_session()
    try:
        yield db
    finally:
        db.close()


@st.cache_resource
def load_db():
    '''Loads database session into streamlit session context'''
    
    if "db" not in st.session_state:
        st.session_state.db = next(get_db())

    # db = st.session_state['db']
    # # print("Loaded database session:", db)  # Uncomment to debug session state in console
    # return db
