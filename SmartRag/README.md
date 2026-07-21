# 🧩 SmartRag — Simple AI Research Assistant

A beginner-friendly **Retrieval-Augmented Generation (RAG)** application built with Python, Streamlit, LangChain, ChromaDB, and OpenRouter.

Upload PDF or TXT files, ask questions about them, and get answers that are strictly grounded in your documents — no hallucinations.

---

## 📂 Project Structure

The project is intentionally kept simple — all logic lives in just **two files**:

```
SmartRag/
├── app.py              # Streamlit UI — file uploads + chat interface
├── rag_pipeline.py     # All RAG logic — load, chunk, embed, store, query
├── requirements.txt    # Python dependencies
├── .env                # Your API keys (never committed to Git)
└── .streamlit/
    └── config.toml     # Streamlit server configuration
```

---

## 🛠️ Setup & Installation

### 1. Prerequisites
Python **3.10+** required (tested on 3.14).

### 2. Create a Virtual Environment
```bash
python -m venv venv
.\venv\Scripts\activate   # Windows
source venv/bin/activate  # Mac/Linux
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure API Keys
Create a `.env` file in the `SmartRag/` directory:
```ini
OPENROUTER_API_KEY=your_openrouter_api_key_here
```
> Get a free key at [openrouter.ai](https://openrouter.ai). No billing required for free-tier models.

---

## 🚀 Running the App

```bash
streamlit run app.py
```

The app opens at `http://localhost:8501`.

---

## 🧠 How the RAG Pipeline Works

This is the core concept of the project — **Retrieval-Augmented Generation**:

| Step | What Happens | Code Location |
|------|-------------|---------------|
| **1. Load** | PDF/TXT file is read from disk | `PyPDFLoader` / `TextLoader` |
| **2. Chunk** | Document split into 800-character overlapping pieces | `RecursiveCharacterTextSplitter` |
| **3. Embed** | Each chunk converted to a math vector (list of numbers) | `HuggingFaceEmbeddings` (local, no API needed) |
| **4. Store** | Vectors saved to disk in ChromaDB | `chromadb.PersistentClient` |
| **5. Retrieve** | User's question embedded → 4 most similar chunks found | Cosine similarity search |
| **6. Generate** | Chunks + question sent to LLM → answer produced | OpenRouter `gpt-oss-20b:free` |

### Why RAG?
Instead of asking a generic AI that might guess or hallucinate, RAG makes the AI read *your* specific documents first and only answer based on what's in them.

---

## 🔑 Key Technologies

| Library | Purpose |
|---------|---------|
| `streamlit` | Web UI framework |
| `langchain` | Document loading, chunking, prompt building |
| `sentence-transformers` | Local embedding model (runs on your CPU, free) |
| `chromadb` | Local vector database for storing embeddings |
| `langchain-openai` | LLM client (used to connect to OpenRouter) |

---

## 👨‍💻 Author
**Rachith Anumalla** — CEI Data Science Internship Capstone Project
