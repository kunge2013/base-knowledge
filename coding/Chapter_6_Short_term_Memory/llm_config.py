"""LLM Configuration for LangChain Short-term Memory examples.

Configure your LLM API settings here. All examples use this configuration.
"""

import os
from typing import Optional
from langchain_openai import ChatOpenAI
from langchain_core.language_models.chat_models import BaseChatModel
from dotenv import load_dotenv

load_dotenv()


def get_llm(model_name: str = "gpt-4.1-mini", temperature: float = 0.1) -> BaseChatModel:
    """Get configured LLM instance.

    Args:
        model_name: Name of the model to use
        temperature: Temperature for generation

    Returns:
        Configured ChatOpenAI instance

    Raises:
        ValueError: If OPENAI_API_KEY is not set
        RuntimeError: If LLM initialization fails
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY environment variable is not set. "
            "Please set it in your .env file."
        )

    try:
        return ChatOpenAI(
            model=os.getenv("model", model_name),
            temperature=float(os.getenv("temperature") or temperature),
            max_tokens=1000,
            timeout=30,
            api_key=api_key,
            base_url=os.getenv("OPENAI_BASE_URL") if os.getenv("OPENAI_BASE_URL") else None,
        )
    except Exception as e:
        raise RuntimeError(f"Failed to initialize LLM: {e}") from e


# Default LLM instance - lazy initialized to avoid import-time failure
_default_llm: Optional[BaseChatModel] = None


def get_default_llm() -> BaseChatModel:
    """Get the default LLM instance (lazy initialization)."""
    global _default_llm
    if _default_llm is None:
        _default_llm = get_llm()
    return _default_llm
