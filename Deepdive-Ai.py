import os
import streamlit as st
import PyPDF2
import faiss
import requests
import torch
from sentence_transformers import SentenceTransformer

# Load the Gemini API key from the environment variable
gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    st.error("Gemini API key is NOT set in the environment variables!")
    st.stop()

# Load embedding model
embed_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# Function to extract text from PDF
def extract_text_from_pdf(uploaded_file):
    text = ""
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    return text

# Function to split text into chunks
def split_text(text, chunk_size=500):
    words = text.split()
    chunks = [' '.join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]
    return chunks

# Function to create FAISS index
def create_faiss_index(embeddings):
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    return index

# Function to retrieve relevant text
def retrieve_text(query, index, embeddings, texts, top_k=3):
    query_embedding = embed_model.encode([query])
    distances, indices = index.search(query_embedding, top_k)
    return [texts[i] for i in indices[0]]

# Function to get response from Gemini API
def get_gemini_response(context, query):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={gemini_api_key}"
    headers = {
        "Content-Type": "application/json"
    }
    
    # Adjusting the payload according to Gemini API's format
    data = {
        "contents": [
            {
                "parts": [
                    {"text": f"Context: {context}\n\nQuery: {query}"}
                ]
            }
        ]
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        response_json = response.json()
        
        # Extracting only the text answer
        try:
            answer = response_json["candidates"][0]["content"]["parts"][0]["text"]
            return answer  # Returning only the clean text response
        except KeyError:
            return "No valid response found."
    
    else:
        return f"Error: {response.status_code}, Message: {response.text}"


    
# Streamlit UI
st.title("AI Research Paper Insight Extractor")

# File Upload
uploaded_file = st.file_uploader("Upload AI Research Paper (PDF)", type="pdf")

if uploaded_file is not None:
    # Extract text
    raw_text = extract_text_from_pdf(uploaded_file)
    text_chunks = split_text(raw_text)

    # Create embeddings
    embeddings = torch.tensor(embed_model.encode(text_chunks)).numpy()

    # Create FAISS index
    faiss_index = create_faiss_index(embeddings)

    # Query Input
    query = st.text_input("Ask a question about the paper")

    if query:
        # Retrieve relevant chunks
        retrieved_texts = retrieve_text(query, faiss_index, embeddings, text_chunks)
        context = " ".join(retrieved_texts)
        
        # Get response from Gemini API
        answer = get_gemini_response(context, query)
        
        # Display the answer
        st.subheader("Answer:")
        st.write(answer)