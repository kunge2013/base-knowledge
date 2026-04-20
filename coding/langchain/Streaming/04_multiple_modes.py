"""04_multiple_modes.py
Stream multiple modes simultaneously.
"""

from langchain.agents import create_agent
from langchain.config import get_stream_writer
from langchain.tools import tool
from llm_config import default_llm

@tool
def get_weather(city: str) -> str:
    """Get weather for a given city."""
    writer = get_stream_writer()
    writer(f"Looking up data for city: {city}")
    writer(f"Acquired data for city: {city}")
    return f"It's always sunny in {city}!"

agent = create_agent(
    default_llm,
    tools=[get_weather],
)

print("Streaming multiple modes:")
for chunk in agent.stream(
    {"messages": [{"role": "user", "content": "What is the weather in SF?"}]},
    stream_mode=["updates", "custom"],
    version="v2",
):
    print(f"Stream mode: {chunk['type']}")
    print(f"Content: {chunk['data']}")
    print()
