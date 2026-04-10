"""17_accumulate_tool_calls.py
Example: Accumulating tool call chunks from streaming.
"""

from langchain.tools import tool
from llm_config import default_llm


@tool
def get_weather(location: str) -> str:
    """Get the weather at a location."""
    return f"It's sunny in {location}."


model_with_tools = default_llm.bind_tools([get_weather])

# Accumulate chunks to build complete tool calls
gathered = None
for chunk in model_with_tools.stream("What's the weather in Boston?"):
    gathered = chunk if gathered is None else gathered + chunk
    print(gathered.tool_calls)
