import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # DeepSeek API
    DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
    DEEPSEEK_API_URL = os.getenv("DEEPSEEK_API_URL", "https://api.deepseek.com/v1/chat/completions")
    DEEPSEEK_MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
    
    # Claude API
    CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY", "")
    CLAUDE_MODEL = os.getenv("CLAUDE_MODEL", "claude-3-haiku")

    # DEFAULT LLM
    DEFAULT_LLM = os.getenv("DEFAULT_LLM", "claude")
    

    # Local storage
    ANCHOR_DB_PATH = os.getenv("ANCHOR_DB_PATH", "anchors.db")
    REDIS_URL = os.getenv("REDIS_URL", None)  # Optional
    
    # Compression
    DEFAULT_COMPRESSION = os.getenv("DEFAULT_COMPRESSION", "moderate")
    
    # Quality thresholds
    TRI_THRESHOLD = float(os.getenv("TRI_THRESHOLD", "0.85"))
    DRIFT_THRESHOLD = float(os.getenv("DRIFT_THRESHOLD", "0.70"))
    
    # Session
    SESSION_EXPIRE_SECONDS = int(os.getenv("SESSION_EXPIRE_SECONDS", "3600"))