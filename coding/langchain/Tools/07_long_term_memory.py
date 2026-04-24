"""07_long_term_memory.py
Use persistent store for long-term memory.
"""

from typing import Any
from langgraph.store.memory import InMemoryStore
from langchain.tools import tool, ToolRuntime

# Access memory
@tool
def get_user_info(user_id: str, runtime: ToolRuntime) -> str:
    """Look up user info."""
    store = runtime.store
    user_info = store.get(("users",), user_id)
    return str(user_info.value) if user_info else "Unknown user"

# Update memory
@tool
def save_user_info(user_id: str, user_info: dict[str, Any], runtime: ToolRuntime) -> str:
    """Save user info."""
    store = runtime.store
    store.put(("users",), user_id, user_info)
    return "Successfully saved user info."

# Example setup
store = InMemoryStore()

print("Tools for long-term memory created")
print("Use with create_agent(store=store) to enable persistent storage")
