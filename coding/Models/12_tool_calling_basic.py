"""12_tool_calling_basic.py
Example: Basic tool calling with bind_tools.
"""

from langchain.tools import tool
from llm_config import default_llm


@tool
def get_weather(location: str) -> str:
    """Get the weather at a location."""
    return f"It's sunny in {location}."


# Bind tools to the model
model_with_tools = default_llm.bind_tools([get_weather])

# Get response with tool calls
response = model_with_tools.invoke("What's the weather like in Boston?")
for tool_call in response.tool_calls:
    # View tool calls made by the model
    print(f"Tool: {tool_call['name']}")
    print(f"Args: {tool_call['args']}")
