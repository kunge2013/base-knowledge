"""10_agent_naming.py
Example: Setting agent name for subgraph identification.
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
    name="research_assistant"
)
