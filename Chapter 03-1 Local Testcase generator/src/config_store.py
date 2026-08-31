"""Configuration layer - reads settings from the local .env file.

This module lives at <chapter root>/src/. The .env file sits one level
up at the chapter root. Credentials are never hardcoded here.
"""

from pathlib import Path

from dotenv import load_dotenv, set_key

# <chapter root>/src/config_store.py -> chapter root is parent.parent
CHAPTER_DIR = Path(__file__).resolve().parent.parent

ENV_PATH = CHAPTER_DIR / ".env"

# Keys read from .env
JIRA_URL = "JIRA_URL"
JIRA_EMAIL = "JIRA_EMAIL"
JIRA_TOKEN = "JIRA_TOKEN"
GROQ_API_KEY = "GROQ_API_KEY"
GROQ_MODEL = "GROQ_MODEL"
OLLAMA_URL = "OLLAMA_URL"
OLLAMA_MODEL = "OLLAMA_MODEL"
LLM_PROVIDER = "LLM_PROVIDER"

DEFAULTS = {
    OLLAMA_URL: "http://localhost:11434",
    OLLAMA_MODEL: "gemma3:1b",
    GROQ_MODEL: "llama-3.3-70b-versatile",
    LLM_PROVIDER: "auto",
}

VALID_PROVIDERS = ("auto", "ollama", "groq")

_ENV_KEYS = (
    JIRA_URL,
    JIRA_EMAIL,
    JIRA_TOKEN,
    GROQ_API_KEY,
    GROQ_MODEL,
    OLLAMA_URL,
    OLLAMA_MODEL,
    LLM_PROVIDER,
)


def env_exists() -> bool:
    """True if a .env file is present at the chapter root."""
    return ENV_PATH.exists()


def load_settings() -> dict:
    """Load all settings from .env, applying defaults for optional keys."""
    import os

    load_dotenv(ENV_PATH)

    settings = {}
    for key in _ENV_KEYS:
        value = os.getenv(key)
        if value is None:
            value = DEFAULTS.get(key, "")
        settings[key] = value.strip().strip("'\"")

    return settings


def save_provider(provider: str) -> None:
    """Persist the LLM provider choice to .env (auto | ollama | groq).

    Only the LLM_PROVIDER line is touched; other lines and comments are
    preserved. Creates .env if it does not exist.
    """
    if provider not in VALID_PROVIDERS:
        raise ValueError(
            f"Invalid provider '{provider}'. "
            f"Choose one of {', '.join(VALID_PROVIDERS)}."
        )

    set_key(str(ENV_PATH), LLM_PROVIDER, provider)
