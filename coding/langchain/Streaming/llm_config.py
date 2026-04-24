"""LLM Configuration for LangChain Streaming examples.

Configure your LLM API settings here. All examples use this configuration.
"""

import os
from langchain_openai import ChatOpenAI
from langchain_core.language_models.chat_models import BaseChatModel
from dotenv import load_dotenv

load_dotenv()

os.environ['NO_PROXY'] = '*'
os.environ['no_proxy'] = '*'

def get_llm(model_name: str = "gpt-4.1-mini", temperature: float = 0.1) -> BaseChatModel:
    """Get configured LLM instance.

    Args:
        model_name: Name of the model to use
        temperature: Temperature for generation

    Returns:
        Configured ChatOpenAI instance
    """
    return ChatOpenAI(
        model=os.getenv("model"),
        temperature=float(os.getenv("temperature") or 0.1),
        max_tokens=1000,
        timeout=30,
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_BASE_URL") if os.getenv("OPENAI_BASE_URL") else None,
    )


# Default LLM instance used across all examples
default_llm = get_llm()
