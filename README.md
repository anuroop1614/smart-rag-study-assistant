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
- LLM-powered answers (Groq API)

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
```

---

## 🌐 How to Deploy on Streamlit Community Cloud

1. **Fork or clone this repository.**
2. **Go to [Streamlit Cloud](https://streamlit.io/cloud) and sign in with GitHub.**
3. **Click "New app" and select this repo and the `main` branch.**
4. **Set up secrets:**
   - In the Streamlit Cloud app dashboard, go to `Settings` → `Secrets` and add:
     ```
     GROQ_API_KEY = "your-groq-api-key"
     FIREBASE_CONFIG = "your-firebase-config-json-string"
     ```
   - (You may need to adapt your code to read FIREBASE_CONFIG from secrets if not already.)
5. **Click Deploy!**

---

## 💻 Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables (on Windows)
set GROQ_API_KEY=your-groq-api-key

# Run the app
streamlit run app.py
```

---

## 📝 Notes
- Never commit secrets or API keys to the repository.
- For Firebase, you may need to adapt your code to read config from Streamlit secrets.

---

Enjoy your smart study assistant!
