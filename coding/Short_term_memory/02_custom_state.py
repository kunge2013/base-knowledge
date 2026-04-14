"""02_custom_state.py
Customize agent memory with custom state schema.
"""

from langchain.agents import create_agent, AgentState
from langgraph.checkpoint.memory import InMemorySaver
from llm_config import default_llm
from langchain.tools import tool
from pydantic import BaseModel

class CustomAgentState(AgentState):
    user_id: str
    preferences: dict

@tool
def get_user_info(query: str) -> str:
    """Get user information."""
    return f"User info for: {query}"

# Create agent with custom state
agent = create_agent(
    default_llm,
    tools=[get_user_info],
    state_schema=CustomAgentState,
    checkpointer=InMemorySaver(),
)

# Use custom state in invoke
result = agent.invoke(
    {
        "messages": [{"role": "user", "content": "Hello"}],
        "user_id": "user_123",
        "preferences": {"theme": "dark"}
    },
    {"configurable": {"thread_id": "1"}}
)

print(f"Response: {result['messages'][-1].content}")
print(f"User ID: {result['user_id']}")
print(f"Preferences: {result['preferences']}")
