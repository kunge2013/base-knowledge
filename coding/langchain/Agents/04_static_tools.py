"""04_static_tools.py
Example: Static tools definition with @tool decorator.
"""

from langchain.tools import tool
from langchain.agents import create_agent
from llm_config import default_llm


@tool
def search(query: str) -> str:
    """Search for information."""
    return f"Results for: {query}"


@tool
def get_weather(location: str) -> str:
    """Get weather information for a location."""
    return f"Weather in {location}: Sunny, 72°F"


# Create agent with static tools
agent = create_agent(default_llm, tools=[search, get_weather])
