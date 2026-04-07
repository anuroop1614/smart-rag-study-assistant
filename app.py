import streamlit as st
import time
from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from groq import Groq
import os
from firebase_config import load_chat, save_chat

"""
🔑 Secure API Key
Set your Groq API key as an environment variable named 'GROQ_API_KEY'.
Do NOT hardcode secrets in source code.
"""
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL_NAME = "llama-3.1-8b-instant"

embed_model = SentenceTransformer("all-MiniLM-L6-v2")

# ---------------- SESSION ----------------
if "chats" not in st.session_state:
    st.session_state.chats = load_chat("user1")

if "chat_docs" not in st.session_state:
    st.session_state.chat_docs = {}

if "current_chat" not in st.session_state:
    st.session_state.current_chat = None

# ---------------- SIDEBAR ----------------
st.sidebar.title("💬 Chats")

chat_name_input = st.sidebar.text_input("Enter Chat Name")

# ➕ New Chat
if st.sidebar.button("➕ New Chat"):
    if chat_name_input.strip() == "":
        st.sidebar.error("Please enter a chat name!")
    else:
        new_chat = chat_name_input.strip()

        if new_chat in st.session_state.chats:
            st.sidebar.error("Chat name already exists!")
        else:
            st.session_state.chats[new_chat] = []
            st.session_state.chat_docs[new_chat] = {"vector_db": None, "chunks": None}
            st.session_state.current_chat = new_chat
            save_chat("user1", st.session_state.chats)

st.sidebar.divider()

# Chat list + delete
for chat_name in list(st.session_state.chats.keys()):
    col1, col2 = st.sidebar.columns([3, 1])

    if col1.button(chat_name, key=f"select_{chat_name}"):
        st.session_state.current_chat = chat_name

    if col2.button("🗑", key=f"delete_{chat_name}"):
        st.session_state["delete_target"] = chat_name

# Delete confirmation
if "delete_target" in st.session_state:
    chat_to_delete = st.session_state["delete_target"]

    st.sidebar.warning(f"Delete '{chat_to_delete}'?")

    col1, col2 = st.sidebar.columns(2)

    if col1.button("Yes Delete"):
        del st.session_state.chats[chat_to_delete]
        del st.session_state.chat_docs[chat_to_delete]

        if st.session_state.chats:
            st.session_state.current_chat = list(st.session_state.chats.keys())[0]
        else:
            st.session_state.current_chat = None

        save_chat("user1", st.session_state.chats)

        del st.session_state["delete_target"]
        st.rerun()

    if col2.button("Cancel"):
        del st.session_state["delete_target"]

# ---------------- MAIN ----------------
st.title("📚 Smart Interview Preparation Assistant")

if st.session_state.current_chat is None:
    st.info("👈 Create a new chat from sidebar to start")
    st.stop()

current = st.session_state.current_chat

# Upload PDFs
file_key = f"uploader_{current}"
uploaded_files = st.file_uploader(
    "Upload PDF(s)",
    type="pdf",
    accept_multiple_files=True,
    key=file_key
)

# ---------------- FUNCTIONS ----------------

def extract_text(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text


def split_text(text, chunk_size=500, overlap=100):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks[:200]


def create_vector_db(chunks):
    embeddings = embed_model.encode(chunks, batch_size=32)
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(np.array(embeddings))
    return index


def retrieve(query):
    data = st.session_state.chat_docs[current]

    if not data["vector_db"]:
        return "No document uploaded."

    query_vec = embed_model.encode([query])
    D, I = data["vector_db"].search(np.array(query_vec), k=2)

    return " ".join([data["chunks"][i] for i in I[0]])


def ask_llm(context, history, query):
    prompt = f"""
Context:
{context}

Conversation:
{history}

Question:
{query}
"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content


# ---------------- PROCESS PDFs ----------------
if uploaded_files:
    all_chunks = []

    for file in uploaded_files:
        text = extract_text(file)
        chunks = split_text(text)
        all_chunks.extend(chunks)

    index = create_vector_db(all_chunks)

    st.session_state.chat_docs[current] = {
        "vector_db": index,
        "chunks": all_chunks
    }

    st.success(f"✅ {len(uploaded_files)} PDF(s) processed")

# Status
if st.session_state.chat_docs[current]["vector_db"]:
    st.success("📄 Documents ready")
else:
    st.warning("⚠️ Upload PDF(s) to start")

# ---------------- CHAT ----------------
chat = st.session_state.chats[current]

for msg in chat:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if prompt := st.chat_input("Ask from your documents..."):

    chat.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.write(prompt)

    history = ""
    for m in chat:
        history += f"{m['role']}: {m['content']}\n"

    context = retrieve(prompt)
    answer = ask_llm(context, history, prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_text = ""

        for word in answer.split():
            full_text += word + " "
            placeholder.markdown(full_text)
            time.sleep(0.02)

    chat.append({"role": "assistant", "content": answer})

    # 🔥 SAVE TO FIREBASE
    save_chat("user1", st.session_state.chats)