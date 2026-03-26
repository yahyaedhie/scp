"""SCP Router v3.2 — Configuration"""

from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    # App
    app_name: str = "SCP Router"
    app_version: str = "3.2.0"
    debug: bool = False

    # Database
    db_path: str = "scp_router.db"

    # Anthropic
    anthropic_api_key: str = Field(default="", description="Anthropic API key")
    anthropic_model: str = "claude-sonnet-4-6"
    anthropic_max_tokens: int = 4096

    # SCP Protocol
    scp_version: str = "3.0"
    default_domain: str = "market"
    drift_firewall: bool = True
    compression_mode: str = "adaptive"  # light|moderate|deep|adaptive

    # Token metering
    token_model: str = "cl100k_base"  # tiktoken encoding

    model_config = {"env_file": ".env", "env_prefix": "SCP_"}


settings = Settings()