"""11_basic_invocation.py
Example: Basic agent invocation.
"""

from langchain.agents import create_agent
from langchain.tools import tool
from llm_config import default_llm


@tool
def get_weather(location: str) -> str:
    """Get weather information for a location."""
    return f"Weather in {location}: Sunny, 72°F"


agent = create_agent(default_llm, tools=[get_weather])

# Invoke the agent with a user message
result = agent.invoke(
    {"messages": [{"role": "user", "content": "What's the weather in San Francisco?"}]}
)

# Print the final response
print(result)
