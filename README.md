# 📚 Smart RAG Study Assistant

An AI-powered document assistant that allows users to upload PDFs and ask questions.  
Built using Retrieval-Augmented Generation (RAG) with real-time chat, multi-session support, and Firebase-based persistent memory.

---

## 🚀 Features

- 📄 Upload multiple PDFs
- 🤖 Ask questions from documents
- 💬 Multi-chat system (like ChatGPT)
- ⚡ Streaming responses
- 🧠 Context-aware answers using RAG
- ☁️ Firebase cloud storage for chat history
- 🔄 Persistent chat across sessions
- 🎯 Clean UI using Streamlit

---

## 🧠 How It Works

1. PDF is uploaded
2. Text is extracted and split into chunks
3. Embeddings are created using Sentence Transformers
4. Stored in FAISS vector database
5. Relevant chunks retrieved based on query
6. Context + question sent to LLM (Groq)
7. Answer generated and streamed

---

## 🛠️ Tech Stack

- Python
- Streamlit
- FAISS
- Sentence Transformers
- Groq API (LLM)
- Firebase Firestore

---

## 📦 Installation

```bash
git clone https://github.com/your-username/smart-rag-study-assistant.git
cd smart-rag-study-assistant

pip install -r requirements.txt
