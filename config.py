# config.py
import os
from dotenv import load_dotenv

load_dotenv()

def _get_required_env(key: str) -> str:
    """Load a required environment variable.
    
    Args:
        key: Environment variable name
        
    Returns:
        The environment variable value
        
    Raises:
        ValueError: If the variable is not set
    """
    value = os.getenv(key)
    if not value:
        raise ValueError(
            f"{key} is missing. Please set it in your .env file."
        )
    return value


def _get_optional_env(key: str, default: str) -> str:
    """Load an optional environment variable with a default fallback."""
    return os.getenv(key, default)


# Required configuration
OPENAI_API_KEY: str = _get_required_env("OPENAI_API_KEY")
SUPABASE_URL: str = _get_required_env("SUPABASE_URL")
SUPABASE_KEY: str = _get_required_env("SUPABASE_KEY")

SIMILARITY_THRESHOLD = 0.8
TOP_K = 5

# Optional configuration with defaults
MODEL: str = _get_optional_env("MODEL", "gpt-5-mini")
TEMPERATURE: float = float(_get_optional_env("TEMPERATURE", "0.7"))
MAX_TOKENS: int = int(_get_optional_env("MAX_TOKENS", "1000"))