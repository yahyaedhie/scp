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
    CLAUDE_MODEL = os.getenv("CLAUDE_MODEL", "claude-3-5-sonnet-20240620")

    # DEFAULT LLM
    DEFAULT_LLM = os.getenv("DEFAULT_LLM", "claude")
    
    # Local storage
    ANCHOR_DB_PATH = os.getenv("ANCHOR_DB_PATH", "anchors.db")
    REDIS_URL = os.getenv("REDIS_URL", None)
    
    # Compression
    DEFAULT_COMPRESSION = os.getenv("DEFAULT_COMPRESSION", "moderate")
    
    # Domain-specific Quality Thresholds
    # Rules: TRI (0-1), Drift (0-1, higher is stricter)
    DOMAIN_CONFIG = {
        "finance": {"tri": 0.85, "drift": 0.70},
        "governance": {"tri": 0.90, "drift": 0.80},
        "education": {"tri": 0.75, "drift": 0.60},
        "cosmology": {"tri": 0.80, "drift": 0.65},
        "default": {"tri": 0.85, "drift": 0.70}
    }
    
    # Session
    SESSION_EXPIRE_SECONDS = int(os.getenv("SESSION_EXPIRE_SECONDS", "3600"))