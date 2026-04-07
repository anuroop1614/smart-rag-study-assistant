import firebase_admin
from firebase_admin import credentials, firestore

import json
import streamlit as st

# Load Firebase key from Streamlit secrets
key_dict = json.loads(st.secrets["FIREBASE_KEY"])

# Initialize Firebase (only once)
if not firebase_admin._apps:
    cred = credentials.Certificate(key_dict)
    firebase_admin.initialize_app(cred)

db = firestore.client()

def load_chat(user_id):
    doc = db.collection("chats").document(user_id).get()
    if doc.exists:
        data = doc.to_dict()
        return data.get("history", {})
    return {}

def save_chat(user_id, chat_data):
    db.collection("chats").document(user_id).set({
        "history": chat_data
    })