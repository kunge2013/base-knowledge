"""07_tool_write_state.py
Write short-term memory from tools using Command.
"""

from langchain.tools import tool, ToolRuntime
from langchain.messages import ToolMessage
from langchain.agents import create_agent, AgentState
from langgraph.types import Command
from pydantic import BaseModel
from llm_config import default_llm

class CustomState(AgentState):
    user_name: str

class CustomContext(BaseModel):
    user_id: str

@tool
def update_user_info(
    runtime: ToolRuntime[CustomContext, CustomState],
) -> Command:
    """Look up and update user info."""
    user_id = runtime.context.user_id
    name = "John Smith" if user_id == "user_123" else "Unknown"
    return Command(update={
        "user_name": name,
        # Update message history
        "messages": [
            ToolMessage(
                "Successfully looked up user information",
                tool_call_id=runtime.tool_call_id
            )
        ]
    })

@tool
def greet(
    runtime: ToolRuntime[CustomContext, CustomState]
) -> str | Command:
    """Greet user once you found their info."""
    user_name = runtime.state.get("user_name", None)
    if user_name is None:
        return Command(update={
            "messages": [
                ToolMessage(
                        "Please call 'update_user_info' tool first.",
                        tool_call_id=runtime.tool_call_id
                    )
            ]
        })
    return f"Hello {user_name}!"

agent = create_agent(
    default_llm,
    tools=[update_user_info, greet],
    state_schema=CustomState,
    context_schema=CustomContext,
)

print("Tools that update state:")
result = agent.invoke(
    {"messages": [{"role": "user", "content": "greet me"}]},
    context=CustomContext(user_id="user_123"),
)
print(f"Response: {result['messages'][-1].content}")
