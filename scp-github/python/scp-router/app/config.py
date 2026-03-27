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
    scp_version: str = "3.0.2"
    default_domain: str = "market"
    drift_firewall: bool = True
    compression_mode: str = "moderate"  # light|moderate|deep|adaptive

    # Token metering
    token_model: str = "cl100k_base"  # tiktoken encoding

    # Domain thresholds
    domain_config: dict = {
        "finance": {"tri": 0.85, "cqs": 0.80},
        "education": {"tri": 0.90, "cqs": 0.85},
        "governance": {"tri": 0.95, "cqs": 0.85},
        "default": {"tri": 0.90, "cqs": 0.85},
    }

    def get_thresholds(self, domain: str) -> dict:
        """Get TRI/CQS thresholds for a specific domain."""
        return self.domain_config.get(domain, self.domain_config["default"])

    model_config = {"env_file": ".env", "env_prefix": "SCP_"}

    def validate_api_key(self):
        if not self.anthropic_api_key:
            import warnings
            warnings.warn("SCP_ANTHROPIC_API_KEY is not set. /proxy/chat will fail.")


settings = Settings()
settings.validate_api_key()