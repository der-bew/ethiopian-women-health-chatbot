import uvicorn
from fastapi import FastAPI

app = FastAPI(title="Ethiopian Women Health Chatbot", description="A chatbot for Ethiopian women's health", version="1.0.0")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
