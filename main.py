from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import requests
import os
import random
from funfact import GROQ_API_KEY, TOPICS
from madhurbot import retrieve_chunks, model
# from dotenv import load_dotenv

# load_dotenv()

app = FastAPI()

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

@app.post("/ask")
async def ask(request: Request):
    body = await request.json()
    message = body.get("message")
    history = body.get('history')
    print("here is the history 🫠👽")
    print(history)
    retrieved_context = retrieve_chunks(message)
    print("🔍 Retrieved Chunks:")
    for c in retrieved_context:
        print("-", c)
            
    prompt = f"""
    You are Madhur Chouhan, designed to answer questions about Madhur using information from his portfolio.

    ### Instruction:
    - If the user input is a greeting or farewell (e.g., "hi", "hello", "bye", "see you"), respond warmly and naturally — context is not needed in that case.
    - For all other queries, answer strictly using the context provided below.
    - Use markdown in the response.
    - If you cannot find the answer in the context, respond with: 
    "Sorry, I can only answer questions about Madhur based on the available portfolio information."

    ### Context:
    {chr(10).join(retrieved_context)}

    ### Chat History:
    {history}

    ### User Message:
    {message}

    ### Response:
    """

    response = model.generate_content(prompt)
    answer = response.text.strip()

    return {"answer": answer}
