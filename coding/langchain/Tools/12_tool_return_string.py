"""12_tool_return_string.py
Tool that returns a string for human-readable results.
"""

from langchain.tools import tool

@tool
def get_weather(city: str) -> str:
    """Get weather for a city."""
    return f"It is currently sunny in {city}."

# Use the tool
result = get_weather.invoke({"city": "Beijing"})
print(f"Tool result: {result}")
print(f"Result type: {type(result)}")
print("\nBehavior:")
print("- Return value is converted to a ToolMessage")
print("- Model sees the text and decides next action")
print("- No agent state fields are changed directly")
