"""
 Chat endpoints for the app
 version: 1.0.0
 author: Derbew Felasman
"""

from fastapi import APIRouter, Depends
from pydantic import BaseModel
import hashlib
from app.rag.graph import agent_graph
from app.db.supabase_client import supabase
from app.config import REDIS_CLIENT
from app.routers.auth import get_current_user
import uuid

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    conversation_id: str = None  # Optional; create new if none

@router.post("/chat")
def chat_endpoint(request: ChatRequest, user_id: str = Depends(get_current_user)):
    convo_id = request.conversation_id or str(uuid.uuid4())

    if not request.conversation_id:
        supabase.table('conversations').insert({
            'id': convo_id,
            'user_id': user_id,
            'title': request.message[:50]  # Simple title
        }).execute()

    cache_key = hashlib.md5((user_id + request.message).encode()).hexdigest()  # User-specific cache
    cached = REDIS_CLIENT.get(cache_key)
    if cached:
        return {"response": cached.decode(), "conversation_id": convo_id}

    state = {
        "messages": [request.message],
        "user_id": user_id,
        "conversation_id": convo_id
    }
    result = agent_graph.invoke(state, config={"configurable": {"thread_id": f"{user_id}_{convo_id}"}})
    response = result['messages'][-1]

    REDIS_CLIENT.set(cache_key, response, ex=86400)

    supabase.table('messages').insert([
        {'conversation_id': convo_id, 'role': 'user', 'content': request.message},
        {'conversation_id': convo_id, 'role': 'assistant', 'content': response}
    ]).execute()

    return {"response": response, "conversation_id": convo_id}
