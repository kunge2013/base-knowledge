"""14_custom_state_middleware.py
Example: Custom state definition via middleware (preferred approach).
"""

from langchain.agents import AgentState
from langchain.agents.middleware import AgentMiddleware
from langchain.agents import create_agent
from langchain.tools import tool
from llm_config import default_llm
from typing import Any


class CustomState(AgentState):
    user_preferences: dict


@tool
def tool1(query: str) -> str:
    """First example tool."""
    return f"Result for: {query}"


@tool
def tool2(query: str) -> str:
    """Second example tool."""
    return f"Result for: {query}"


class CustomMiddleware(AgentMiddleware):
    state_schema = CustomState
    tools = [tool1, tool2]

    def before_model(self, state: CustomState, runtime) -> dict[str, Any] | None:
        """Hook called before model invocation."""
        # Access and potentially modify the state
        preferences = state.get("user_preferences", {})
        # Return None to leave state unchanged
        # Return modified state if changes are needed
        return None


agent = create_agent(
    model=default_llm,
    tools=[tool1, tool2],
    middleware=[CustomMiddleware()]
)

# The agent can now track additional state beyond messages
result = agent.invoke({
    "messages": [{"role": "user", "content": "I prefer technical explanations"}],
    "user_preferences": {"style": "technical", "verbosity": "detailed"},
})
