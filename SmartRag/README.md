# 🧩 SmartRag — Simple AI Research Assistant

A straightforward, beginner-friendly Retrieval-Augmented Generation (RAG) application built with Python, Streamlit, LangChain, ChromaDB, and OpenAI.

This project allows users to upload PDF and TXT files, process them into a local vector database, and ask questions about them. Answers are strictly grounded in the provided documents to prevent AI hallucinations.

---

## 📂 Project Structure

We intentionally keep this project as simple as possible. All logic lives in just two files:

- `app.py`: The frontend UI built with Streamlit. Handles file uploads and the chat interface.
- `rag_pipeline.py`: The backend logic. Handles document chunking, embeddings, ChromaDB storage, and OpenAI LLM generation.
- `requirements.txt`: The Python dependencies needed to run the app.
- `.env`: Where you store your API keys.

---

## 🛠️ Installation

### 1. Prerequisites
Ensure you have **Python 3.10+** installed.

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Setup Environment Variables
Create a `.env` file in the root directory (or use the existing `.env.example` as a template) and add your OpenAI API key:
```ini
OPENAI_API_KEY=your_openai_api_key_here
```

---

## 🚀 Running the App

Launch the Streamlit application locally:
```bash
streamlit run app.py
```
The application will open automatically in your default web browser at `http://localhost:8501`.

---

## 🧠 How it Works (RAG Pipeline)

1. **Ingestion**: When you upload a document, `rag_pipeline.py` splits it into chunks of 800 characters.
2. **Embedding**: We use a local HuggingFace model (`sentence-transformers/all-MiniLM-L6-v2`) to turn these chunks into math vectors.
3. **Storage**: The vectors are saved persistently on your hard drive using **ChromaDB**.
4. **Retrieval**: When you ask a question, we find the 4 most mathematically similar chunks to your question.
5. **Generation**: We send those 4 chunks to **OpenAI (gpt-4o-mini)** with a strict instruction to *only* answer using the provided text.
