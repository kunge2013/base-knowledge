"""01_basic_usage.py
Basic usage of short-term memory with checkpointer.
"""

from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from llm_config import default_llm
from langchain.tools import tool

@tool
def get_user_info(query: str) -> str:
    """Get user information."""
    return f"User info for: {query}"

# Create agent with checkpointer for short-term memory
agent = create_agent(
    default_llm,
    tools=[get_user_info],
    checkpointer=InMemorySaver(),
)

# Use thread_id to maintain conversation history
config = {"configurable": {"thread_id": "1"}}

# First interaction
result1 = agent.invoke(
    {"messages": [{"role": "user", "content": "Hi! My name is Bob."}]},
    config
)
print(f"First response: {result1['messages'][-1].content}")

# Second interaction - agent remembers the name
result2 = agent.invoke(
    {"messages": [{"role": "user", "content": "What's my name?"}]},
    config
)
print(f"Second response: {result2['messages'][-1].content}")
