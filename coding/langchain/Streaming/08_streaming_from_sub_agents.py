"""08_streaming_from_sub_agents.py
Stream from sub-agents with agent identification.
"""

from typing import Any
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain.messages import AIMessage, AnyMessage
from langchain.tools import tool
from llm_config import default_llm

@tool
def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

# Create weather agent
weather_model = init_chat_model(os.getenv("model"))
weather_agent = create_agent(
    weather_model,
    tools=[get_weather],
    name="weather_agent",
)

def call_weather_agent(query: str) -> str:
    """Query weather agent."""
    result = weather_agent.invoke({
        "messages": [{"role": "user", "content": query}]
    })
    return result["messages"][-1].text

# Create supervisor agent
supervisor_model = init_chat_model(os.getenv("model"))
agent = create_agent(
    supervisor_model,
    tools=[call_weather_agent],
    name="supervisor",
)

def _render_message_chunk(token: Any) -> None:
    """Render message chunks."""
    if hasattr(token, 'text'):
        print(token.text, end="")
    if hasattr(token, 'tool_call_chunks'):
        print(token.tool_call_chunks)

print("Streaming from sub-agents:")
input_message = {"role": "user", "content": "What is weather in Boston?"}
current_agent = None

for chunk in agent.stream(
    {"messages": [input_message]},
    stream_mode=["messages", "updates"],
    subgraphs=True,
    version="v2",
):
    if chunk["type"] == "messages":
"        token, metadata = chunk["data"]
        agent_name = metadata.get("lc_agent_name")
        if agent_name and agent_name != current_agent:
            print(f"\n🤖 {agent_name}: ")
            current_agent = agent_name
        if hasattr(token, 'content_blocks'):
            _render_message_chunk(token)
