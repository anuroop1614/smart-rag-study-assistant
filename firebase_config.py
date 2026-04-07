import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase (run only once)
if not firebase_admin._apps:
    cred = credentials.Certificate("firebase_key.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

def load_chat(user_id):
    doc = db.collection("chats").document(user_id).get()

    if doc.exists:
        data = doc.to_dict()

        # 🔥 FIX: ensure it's always dict
        if isinstance(data.get("history"), dict):
            return data["history"]
        else:
            return {}   # fallback

    return {}

# Save chat history
def save_chat(user_id, chat_history):
    db.collection("chats").document(user_id).set({
        "history": chat_history
    })