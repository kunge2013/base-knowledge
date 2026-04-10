"""16_streaming_example.py
Example: Streaming agent responses step-by-step.
"""

from langchain.agents import create_agent
from langchain.tools import tool
from llm_config import default_llm
from langchain_core.messages import AIMessage, HumanMessage


@tool
def search_web(query: str) -> str:
    """Search web for AI news and information."""
    return f"Search results for '{query}': Latest AI developments..."


agent = create_agent(default_llm, tools=[search_web])

# Stream responses to see intermediate progress
for chunk in agent.stream({
    "messages": [{"role": "user", "content": "Search for AI news and summarize the findings"}]
}, stream_mode="values"):
    # Each chunk contains the full state at that point
    latest_message = chunk["messages"][-1]
    if latest_message.content:
        if isinstance(latest_message, HumanMessage):
            print(f"User: {latest_message.content}")
        elif isinstance(latest_message, AIMessage):
            print(f"Agent: {latest_message.content}")
    elif hasattr(latest_message, 'tool_calls') and latest_message.tool_calls:
        print(f"Calling tools: {[tc['name'] for tc in latest_message.tool_calls]}")
