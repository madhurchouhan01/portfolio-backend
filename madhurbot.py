import faiss
import json
import cohere
import os
import numpy as np
import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
co = cohere.Client(COHERE_API_KEY)

# Initialize Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

# Load FAISS and context chunks
index = faiss.read_index("madhur_index.faiss")
with open("chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

def get_cohere_embedding(text):
    response = co.embed(
        texts=[text],
        model="embed-english-v3.0",
        input_type="search_query"
    )
    return np.array(response.embeddings[0], dtype="float32")

def retrieve_chunks(query, top_k=5):
    query_vec = get_cohere_embedding(query).reshape(1, -1)
    distances, indices = index.search(query_vec, top_k)
    return [chunks[i] for i in indices[0]]