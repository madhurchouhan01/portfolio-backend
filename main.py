from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
import os
from dotenv import load_dotenv
load_dotenv()
app = FastAPI()

# Allow frontend from GitHub Pages
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production: use specific domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
print(GROQ_API_KEY)
@app.get("/")
def read_root():
    return {"message": "Groq FastAPI Proxy is live"}

@app.post("/funfact")
def get_fun_fact():
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GROQ_API_KEY}"
    }

    payload = {
        "model": "meta-llama/llama-4-scout-17b-16e-instruct",
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant who shares short, fun, and surprising facts about programming or technology."
            },
            {
                "role": "user",
                "content": "Give me one fun fact about programming or technology. Keep it under 50 words."
            }
        ],
        "temperature": 0.8,
        "max_tokens": 100
    }

    response = requests.post("https://api.groq.com/openai/v1/chat/completions", json=payload, headers=headers)
    return response.json()
