"""15_disable_parallel_tool_calls.py
Example: Disable parallel tool calls when single tool call is desired.
"""

from langchain.tools import tool
from llm_config import default_llm


@tool
def get_weather(location: str) -> str:
    """Get the weather at a location."""
    return f"It's sunny in {location}."

# Disable parallel tool calls
model_with_tools = default_llm.bind_tools([get_weather], parallel_tool_calls=False)
