import os
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

TOPICS = [
    "programming", "AI", "machine learning", "deep learning", "quantum computing",
    "blockchain", "cybersecurity", "robotics", "computer vision", "natural language processing",
    "data science", "programming languages", "history of computing", "futuristic tech"
]