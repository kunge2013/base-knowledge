"""07_system_prompt_string.py
Example: System prompt configuration with string.
"""

from langchain.agents import create_agent
from llm_config import default_llm
from langchain.tools import tool


@tool
def search(query: str) -> str:
    """Search for information."""
    return f"Search results: {query}"


agent = create_agent(
    default_llm,
    [search],
    system_prompt="You are a helpful assistant. Be concise and accurate."
)
