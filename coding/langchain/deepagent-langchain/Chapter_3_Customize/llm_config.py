"""LLM Configuration for Deep Agents Customize examples.

Configure your LLM API settings here. All examples use this configuration.
"""

import os
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
    """
    return ChatOpenAI(
        model=model_name,
        temperature=temperature,
        max_tokens=1000,
        timeout=30,
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_BASE_URL") if os.getenv("OPENAI_BASE_URL") else None,
    )


# Default LLM instance used across all examples
default_llm = get_llm()
