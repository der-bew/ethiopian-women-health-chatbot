"""
This is the main entry point for the Ethiopian Women Health Chatbot API.
version: 1.0.0
author: Derbew Felasman
"""

from fastapi import FastAPI
from app.routers import chat, auth
from app.config import load_config
import uvicorn

load_config()  # Load environment variables

app = FastAPI(title="Ethiopian Women Health Chatbot", description="A chatbot for Ethiopian women's health", version="1.0.0")
app.include_router(auth.router, prefix="/auth")
app.include_router(chat.router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
