import os
import uuid
import shutil
from dotenv import load_dotenv

# Load environment variables (API keys) from the .env file
load_dotenv()

# LangChain components for loading and splitting documents
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings

# ChromaDB - using the NEW PersistentClient API directly (avoids the RustBindingsAPI bug)
import chromadb

# LangChain components for the LLM and prompting
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Hardcoded configurations for simplicity
PERSIST_DIRECTORY = "./vector_store/chroma_db"
COLLECTION_NAME = "documents"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
CHUNK_SIZE = 800
CHUNK_OVERLAP = 150


def get_embeddings_model():
    """Initializes the local embedding model used to turn text into numbers (vectors)."""
    return HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)


def get_chroma_collection():
    """
    Returns the ChromaDB collection using the new PersistentClient API.
    This bypasses LangChain's outdated Chroma wrapper which had a RustBindingsAPI bug.
    """
    client = chromadb.PersistentClient(path=PERSIST_DIRECTORY)
    collection = client.get_or_create_collection(name=COLLECTION_NAME)
    return collection


def process_document(file_path: str):
    """
    Loads a document, splits it into chunks, embeds each chunk,
    and stores everything in ChromaDB.

    Steps:
    1. Load the file (PDF or TXT)
    2. Split it into small, overlapping chunks
    3. Embed each chunk using a local HuggingFace model
    4. Store the chunks + embeddings into ChromaDB
    """
    # Step 1: Load the file based on its extension
    if file_path.endswith(".pdf"):
        loader = PyPDFLoader(file_path)
    elif file_path.endswith(".txt"):
        loader = TextLoader(file_path, encoding="utf-8")
    else:
        raise ValueError("Unsupported file format. Please upload PDF or TXT.")

    documents = loader.load()

    # Step 2: Split the document into smaller chunks (800 characters each, 150 overlap)
    # Overlap ensures context isn't lost at chunk boundaries
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )
    chunks = text_splitter.split_documents(documents)

    # If no text was extracted (e.g., scanned image PDF), return 0
    if not chunks:
        return 0

    # Step 3: Embed each chunk into a vector (list of numbers representing meaning)
    embeddings_model = get_embeddings_model()
    texts = [chunk.page_content for chunk in chunks]
    embeddings = embeddings_model.embed_documents(texts)

    # Step 4: Store chunks + embeddings in ChromaDB with unique IDs
    collection = get_chroma_collection()
    ids = [str(uuid.uuid4()) for _ in chunks]
    collection.add(
        documents=texts,
        embeddings=embeddings,
        ids=ids
    )

    return len(chunks)


def clear_database():
    """Deletes the vector database folder entirely to start fresh."""
    if os.path.exists(PERSIST_DIRECTORY):
        shutil.rmtree(PERSIST_DIRECTORY)
        return True
    return False


def run_query(question: str):
    """
    Answers a question using Retrieval-Augmented Generation (RAG):

    1. Embed the question into a vector
    2. Search ChromaDB for the 4 most similar document chunks
    3. Build a prompt with those chunks as context
    4. Send the prompt to Gemini to generate an answer
    """
    # Step 1: Embed the question
    embeddings_model = get_embeddings_model()
    query_embedding = embeddings_model.embed_query(question)

    # Step 2: Search ChromaDB for the 4 most similar chunks
    collection = get_chroma_collection()
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=4
    )

    # Extract the text documents from the results
    retrieved_texts = results["documents"][0]  # list of strings
    context_text = "\n\n".join(retrieved_texts)

    # Step 3: Build a prompt that instructs the LLM to use only the retrieved context
    template = """
    You are an AI research assistant. Answer the user's question ONLY using the provided context.
    If the context does not contain the answer, say "I could not find this information in the uploaded documents."
    Do not make up facts.

    Context:
    {context}

    Question:
    {question}

    Answer:
    """
    prompt = ChatPromptTemplate.from_template(template)

    # Step 4: Initialize LLM via OpenRouter (free model, no billing needed)
    llm = ChatOpenAI(
        model="openai/gpt-oss-20b:free",
        temperature=0.0,
        api_key=os.getenv("OPENROUTER_API_KEY"),
        base_url="https://openrouter.ai/api/v1"
    )
    chain = prompt | llm | StrOutputParser()
    answer = chain.invoke({
        "context": context_text,
        "question": question
    })

    # Return the answer plus the raw source text for display
    return {
        "answer": answer,
        "source_documents": retrieved_texts
    }
