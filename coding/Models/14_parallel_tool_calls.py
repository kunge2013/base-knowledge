"""14_parallel_tool_calls.py
Example: Multiple parallel tool calls in one response.
"""

from langchain.tools import tool
from llm_config import default_llm


@tool
def get_weather(location: str) -> str:
    """Get the weather at a location."""
    return f"It's sunny in {location}."


model_with_tools = default_llm.bind_tools([get_weather])

# The model may generate multiple tool calls in parallel
response = model_with_tools.invoke(
    "What's the weather in Boston and Tokyo?"
)

# Print the multiple tool calls
print(response.tool_calls)
# [
#   {'name': 'get_weather', 'args': {'location': 'Boston'}, 'id': 'call_1'},
#   {'name': 'get_weather', 'args': {'location': 'Tokyo'}, 'id': 'call_2'},
# ]

# Execute all tools (can be done in parallel with async)
results = []
for tool_call in response.tool_calls:
    if tool_call['name'] == 'get_weather':
        result = get_weather.invoke(tool_call)
    results.append(result)
