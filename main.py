from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
import os
import random
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

TOPICS = [
    "programming", "AI", "machine learning", "deep learning", "quantum computing",
    "blockchain", "cybersecurity", "robotics", "computer vision", "natural language processing",
    "data science", "programming languages", "history of computing", "futuristic tech"
]

@app.get("/")
def read_root():
    return {"message": "Groq FastAPI Proxy is live"}

@app.post("/funfact")
def get_fun_fact():
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GROQ_API_KEY}"
    }

    topic = random.choice(TOPICS)
    dynamic_prompt = (
        f"Give me a unique and lesser-known fun fact related to {topic}. "
        "Make sure it's surprising, educational, and under 50 words. "
        "Avoid repeating common trivia. Be specific if possible."
    )

    payload = {
        "model": "meta-llama/llama-4-scout-17b-16e-instruct",
        "messages": [
            {
                "role": "system",
                "content": "You are a creative and fun assistant who shares surprising, unique, and specific short tech facts."
            },
            {
                "role": "user",
                "content": dynamic_prompt
            }
        ],
        "temperature": 0.9,
        "max_tokens": 100
    }

    response = requests.post("https://api.groq.com/openai/v1/chat/completions", json=payload, headers=headers)
    return response.json()
