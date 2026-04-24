"""02_llm_tokens.py
Stream LLM tokens using stream_mode="messages".
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

print("Streaming LLM tokens:")
for chunk in agent.stream(
    {"messages": [{"role": "user", "content": "What is the weather in SF?"}]},
    stream_mode="messages",
    version="v2",
):
    if chunk["type"] == "messages":
        token, metadata = chunk["data"]
        print(f"Node: {metadata['langgraph_node']}")
        print(f"Content: {token.content_blocks}")
        print()
