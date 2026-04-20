"""05_dynamic_tools_state_based.py
Example: Dynamic tool filtering based on conversation state.
"""

from langchain.agents import create_agent
from langchain.agents.middleware import wrap_model_call, ModelRequest, ModelResponse
from langchain.tools import tool
from llm_config import default_llm
from typing import Callable, List


# Define different tools
@tool
def public_search(query: str) -> str:
    """Public search - available to all users."""
    return f"Public search results: {query}"


@tool
def private_search(query: str) -> str:
    """Private search - requires authentication."""
    return f"Private search results: {query}"


@tool
def advanced_search(query: str) -> str:
    """Advanced search - only available after conversation context."""
    return f"Advanced search results: {query}"


@wrap_model_call
def state_based_tools(
    request: ModelRequest,
    handler: Callable[[ModelRequest], ModelResponse]
) -> ModelResponse:
    """Filter tools based on conversation State."""
    # Read from State: check if user has authenticated
    state = request.state
    is_authenticated = state.get("authenticated", False)
    message_count = len(state["messages"])

    # Only enable sensitive tools after authentication
    if not is_authenticated:
        tools = [t for t in request.tools if t.name.startswith("public_")]
        request = request.override(tools=tools)
    elif message_count < 5:
        # Limit tools early in conversation
        tools = [t for t in request.tools if t.name != "advanced_search"]
        request = request.override(tools=tools)

    return handler(request)


agent = create_agent(
    model=default_llm,
    tools=[public_search, private_search, advanced_search],
    middleware=[state_based_tools]
)
