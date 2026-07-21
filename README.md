# 📚 CEI Assignments & Projects

Welcome to the **CEI Assignments** repository! This chronicles an 8-week journey through Machine Learning and Data Science concepts, culminating in a full-stack AI capstone project.

## 🗂️ Repository Structure

The repository contains week-by-week Jupyter notebooks and the final capstone project.

### 📅 Week-Wise Progress

- **[Week 1](./week1_Anumalla_Rachith.ipynb)**
  - Introduction and fundamental concepts.
  - Foundational exercises in data manipulation and basic modeling.

- **[Week 2](./Week2/)**
  - **Topics:** Exploratory Data Analysis (EDA) and Visualization.
  - **Dataset:** Tesla Deliveries (2015-2025).
  - **Notebook:** `rachith-week-2-cie.ipynb`

- **[Week 3](./Week3/)**
  - **Topics:** Unsupervised Learning (Clustering) & Socio-economic Data Analysis.
  - **Dataset:** Global Country Data.
  - **Notebook:** `rachith-week-3-cie.ipynb`

- **[Week 4](./Week4/)**
  - **Topics:** Supervised Learning and Model Evaluation.
  - **Notebook:** `Week_4_CIE_Rachith.ipynb`

- **[Week 5](./Week5/)**
  - **Topics:** Advanced Classification and Regression techniques.
  - **Notebook:** `Week_5-CIE_Rachith.ipynb`

- **[Week 6](./Week6/)**
  - **Topics:** Deep Learning Basics and Neural Networks.
  - **Notebook:** `Week_6_CIE_Rachith.ipynb`

- **[Week 7](./Week7/)**
  - **Topics:** Advanced Model Tuning, Ensembles, and Optimization.
  - **Notebook:** `Week7_CIE_Rachith.ipynb`

- **[Week 8](./Week-8/)**
  - **Topics:** Final week coursework and Capstone preparation.
  - **Notebook:** `Week-8_Rachith_CIE.ipynb`

---

## 🧩 Capstone Project: SmartRag

**[SmartRag](./SmartRag/)** — *AI Research Assistant using RAG*

A simple, beginner-friendly **Retrieval-Augmented Generation (RAG)** application built with Python, Streamlit, LangChain, ChromaDB, and OpenRouter.

### 🌟 What it does
- Upload **PDF or TXT** documents into a local vector database
- Ask questions about your documents in a chat interface
- Receive answers that are **strictly grounded** in the uploaded content — no hallucinations
- View the exact source passages the AI used to form its answer

### 🔧 Tech Stack
| Component | Technology |
|-----------|-----------|
| UI | Streamlit |
| Document Loading & Chunking | LangChain |
| Embeddings | HuggingFace `all-MiniLM-L6-v2` (local, free) |
| Vector Database | ChromaDB (persistent, on-disk) |
| LLM | OpenRouter (free-tier models) |

### 🗂️ Architecture
The entire backend is consolidated into a single, readable file — `rag_pipeline.py` — making it easy to understand every step of the RAG process.

For detailed setup instructions, see the [SmartRag README](./SmartRag/README.md).

---

## 👨‍💻 Author
**Rachith Anumalla**

*Coursework and projects completed as part of the CEI Data Science Internship Program.*
