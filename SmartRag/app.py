import os
import streamlit as st
import tempfile

from rag_pipeline import process_document, clear_database, run_query

# Configure the Streamlit page
st.set_page_config(page_title="Simple RAG Assistant", layout="wide")
st.title("📚 Simple RAG Research Assistant")
st.caption("Upload documents to the left, and ask questions about them here.")

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# ==========================================
# SIDEBAR: File Uploads & Database Management
# ==========================================
with st.sidebar:
    st.header("Upload Documents")
    
    uploaded_files = st.file_uploader("Upload PDFs or TXT files", type=["pdf", "txt"], accept_multiple_files=True)
    
    if st.button("Process Documents"):
        if not uploaded_files:
            st.warning("Please upload a file first.")
        else:
            with st.spinner("Processing files..."):
                total_chunks = 0
                for file in uploaded_files:
                    # Save the uploaded file temporarily to disk so we can process it
                    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file.name.split('.')[-1]}") as tmp_file:
                        tmp_file.write(file.getvalue())
                        temp_path = tmp_file.name
                        
                    # Process it using our pipeline
                    chunks = process_document(temp_path)
                    total_chunks += chunks
                    
                    # Clean up temp file
                    os.remove(temp_path)
                    
                st.success(f"Success! Processed {len(uploaded_files)} files into {total_chunks} chunks.")
                
    st.markdown("---")
    if st.button("Clear Database"):
        if clear_database():
            st.session_state.messages = []  # clear chat too
            st.success("Database cleared!")
        else:
            st.info("Database is already empty.")

# ==========================================
# MAIN CHAT INTERFACE
# ==========================================
# Display all past chat messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Wait for the user to type a new question
if user_question := st.chat_input("Ask a question based on your uploaded documents..."):
    # 1. Add user question to the screen
    st.session_state.messages.append({"role": "user", "content": user_question})
    with st.chat_message("user"):
        st.markdown(user_question)
        
    # 2. Get the answer from our pipeline
    with st.chat_message("assistant"):
        with st.spinner("Searching documents..."):
            try:
                result = run_query(user_question)
                answer = result["answer"]
                sources = result["source_documents"]
                
                # Display the answer
                st.markdown(answer)
                
                # Display the sources used
                with st.expander("View Source Documents"):
                    for idx, doc_text in enumerate(sources, 1):
                        st.markdown(f"**Source {idx}:**")
                        st.info(doc_text)
                        
                # Save assistant response to history
                st.session_state.messages.append({"role": "assistant", "content": answer})
                
            except Exception as e:
                st.error(f"Error answering question. Did you upload documents first? Details: {e}")
