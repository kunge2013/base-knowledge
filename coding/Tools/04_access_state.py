"""04_access_state.py
Access conversation state from tools.
"""

from langchain.tools import tool, ToolRuntime
from langchain.messages import HumanMessage

@tool
def get_last_user_message(runtime: ToolRuntime) -> str:
    """Get most recent message from user."""
    messages = runtime.state["messages"]

    # Find last human message
    for message in reversed(messages):
        if isinstance(message, HumanMessage):
            return message.content

    return "No user messages found"

# Access custom state fields
@tool
def get_user_preference(
    pref_name: str,
    runtime: ToolRuntime
) -> str:
    """Get a user preference value."""
    preferences = runtime.state.get("user_preferences", {})
    return preferences.get(pref_name, "Not set")

# Example usage (requires LangGraph context)
print("These tools require runtime context and should be used within a LangGraph agent.")
print("See the ToolNode examples for complete agent setup.")
