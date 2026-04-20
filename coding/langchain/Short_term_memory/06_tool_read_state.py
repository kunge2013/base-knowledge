"""06_tool_read_state.py
Read short-term memory from tools.
"""

from langchain.agents import create_agent, AgentState
from langchain.tools import tool, ToolRuntime
from llm_config import default_llm

class CustomState(AgentState):
    user_id: str

@tool
def get_user_info(
    runtime: ToolRuntime
) -> str:
    """Look up user info."""
    user_id = runtime.state["user_id"]
    return "User is John Smith" if user_id == "user_123" else "Unknown user"

agent = create_agent(
    default_llm,
    tools=[get_user_info],
    state_schema=CustomState,
)

result = agent.invoke({
    "messages": "look up user information",
    "user_id": "user_123"
})

print(f"Response: {result['messages'][-1].content}")
