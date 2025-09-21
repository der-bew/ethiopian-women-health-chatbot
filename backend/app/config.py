import os
from dotenv import load_dotenv
import redis

load_dotenv()

def load_config():
    global SUPABASE_URL, SUPABASE_KEY, GEMINI_API_KEY, TAVILY_API_KEY, REDIS_CLIENT
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    REDIS_CLIENT = redis.from_url(REDIS_URL)
