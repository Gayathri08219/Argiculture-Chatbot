from fastapi import FastAPI
from pydantic import BaseModel
import requests
from tavily import TavilyClient
import os
from dotenv import load_dotenv

# ✅ Load environment variables
load_dotenv()

app = FastAPI()

# 🔑 Get API keys from .env
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")

# Initialize Tavily
tavily = TavilyClient(api_key=TAVILY_API_KEY)

class Query(BaseModel):
    question: str

# 🔍 Detect if latest info needed
def needs_latest_info(q):
    keywords = ["latest", "today", "current", "price", "news", "2025", "2026"]
    return any(k in q.lower() for k in keywords)

# 🧠 Call Ollama
def ask_ollama(prompt):
    res = requests.post(
        f"{OLLAMA_URL}/api/generate",
        json={
            "model": "llama3.2",
            "prompt": prompt,
            "stream": False
        }
    )
    return res.json()["response"]

# 🌐 Tavily search
def search_tavily(q):
    result = tavily.search(query=q, max_results=3)
    return " ".join([r["content"] for r in result["results"]])

# 🚀 API
@app.post("/ask")
def ask(query: Query):
    try:
        question = query.question

        if needs_latest_info(question):
            web_data = search_tavily(question)

            prompt = f"""
Use the information below to answer clearly.

{web_data}

Question: {question}
"""

            answer = ask_ollama(prompt)
        else:
            answer = ask_ollama(question)

        return {"answer": answer}

    except Exception as e:
        return {"error": str(e)}