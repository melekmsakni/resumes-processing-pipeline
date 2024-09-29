from pymongo import MongoClient
import streamlit as st

# Singleton pattern for MongoDB client
def get_mongo_client():
    if 'mongo_client' not in st.session_state:
        client = MongoClient("mongodb://root:root@localhost:27017",serverSelectionTimeoutMS=5000)  
        st.session_state.mongo_client = client
    return st.session_state.mongo_client

def get_db():
    client = get_mongo_client()
    return client['Project']  
