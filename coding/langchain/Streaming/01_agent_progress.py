"""01_agent_progress.py
Stream agent progress using stream_mode="updates".
"""

from langchain.agents import create_agent
from langchain.tools import tool
from llm_config import default_llm

@tool
def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

agent = create_agent(
    default_llm,
    tools=[get_weather],
)

print("Streaming agent progress:")
for chunk in agent.stream(
    {"messages": [{"role": "user", "content": "What is the weather in SF?"}]},
    stream_mode="updates",
    version="v2",
):
    if chunk["type"] == "updates":
        for step, data in chunk["data"].items():
            print(f"Step: {step}")
            print(f"Content: {data['messages'][-1].content[:100]}")
            print()
