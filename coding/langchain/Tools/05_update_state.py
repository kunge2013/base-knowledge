"""05_update_state.py
Update agent state from tools using Command.
"""

from langgraph.types import Command
from langchain.tools import tool

@tool
def set_user_name(new_name: str) -> Command:
    """Set: user's name in conversation state."""
    return Command(update={"user_name": new_name})

@tool
def increment_counter(runtime: ToolRuntime) -> Command:
    """Increment a counter in state."""
    current = runtime.state.get("counter", 0)
    return Command(update={"counter": current + 1})

print("These tools return Command objects to update agent state.")
print("They should be used within a LangGraph agent.")
