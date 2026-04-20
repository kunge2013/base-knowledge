"""15_custom_state_schema.py
Example: Custom state definition via state_schema parameter.
"""

from langchain.agents import AgentState
from langchain.agents import create_agent
from langchain.tools import tool
from llm_config import default_llm


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


agent = create_agent(
    model=default_llm,
    tools=[tool1, tool2],
    state_schema=CustomState
)

# The agent can now track additional state beyond messages
result = agent.invoke({
    "messages": [{"role": "user", "content": "I prefer technical explanations"}],
    "user_preferences": {"style": "technical", "verbosity": "detailed"},
})
