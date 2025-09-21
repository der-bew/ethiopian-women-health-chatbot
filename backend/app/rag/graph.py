"""
Backend for the Ethiopian Women Health Chatbot
version: 1.0.0
Author: Derbew Felasman
"""

from langgraph.graph import StateGraph, END
from langgraph.checkpoint import MemorySaver
from langchain_core.tools import tool
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import TypedDict, List
from app.db.supabase_client import supabase
from app.config.load_config import GOOGLE_API_KEY, TAVILY_API_KEY

# Initialize the LLM with the API key
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest", temperature=0.7, api_key=GOOGLE_API_KEY)

# Agent State
class AgentState(TypedDict):
    messages: List[str]
    context: str
    user_id: str
    conversation_id: str

# Tools
@tool(name="WebSearch", description="Search the web for information")
def web_search(query: str) -> str:
    """Search the web using Tavily."""
    tavily = TavilySearchResults(api_key=TAVILY_API_KEY)
    results = tavily.invoke({"query": query})
    return str(results)

@tool(name="Databaseretriever", description="Search the database for information")
def db_retriever(conversation_id: str) -> str:
    """Retrieve chat history from Supabase."""
    result = supabase.table('messages').select('role, content').eq('conversation_id', conversation_id).order('timestamp').execute()
    history = "\n".join([f"{msg['role']}: {msg['content']}" for msg in result.data])
    return history

@tool(name="Vectorretriever", description="Search the vector database for information")
def vector_retriever(query: str) -> str:
    """Retrieve from FAISS vector DB."""
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.load_local("../knowledge_base/index.faiss", embeddings, allow_dangerous_deserialization=True)
    docs = vectorstore.similarity_search(query, k=5)
    return "\n".join([doc.page_content for doc in docs])

tools = [web_search, db_retriever, vector_retriever]

# Nodes
def retrieve(state: AgentState):
    last_msg = state['messages'][-1]
    # Conditional tool calls (simplified; in prod, use agentic decision)
    web_results = web_search.invoke(last_msg) if "search" in last_msg.lower() else ""
    db_history = db_retriever.invoke(state['conversation_id'])
    vector_context = vector_retriever.invoke(last_msg)
    state['context'] = f"Web: {web_results}\nHistory: {db_history}\nKnowledge: {vector_context}"
    return state

def generate(state: AgentState):
    prompt = (
        "You are a helpful health chatbot for Ethiopian women. Provide empathetic, accurate info on maternal health, fistula, cancers.\n"
        f"Context: {state['context']}\n"
        f"User: {state['messages'][-1]}\n"
        "Response:"
    )
    response = llm.generate_content(prompt).text
    state['messages'].append(response)
    return state

# Workflow
workflow = StateGraph(state_schema=AgentState)
workflow.add_node("retrieve", retrieve)
workflow.add_node("generate", generate)
workflow.add_edge("retrieve", "generate")
workflow.add_edge("generate", END)

memory = MemorySaver()
agent_graph = workflow.compile(checkpointer=memory)
