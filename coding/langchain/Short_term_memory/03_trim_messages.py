"""03_trim_messages.py
Trim messages to fit context window using middleware.
"""

from langchain.messages import RemoveMessage
from langgraph.graph.message import REMOVE_ALL_MESSAGES
from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents import create_agent, AgentState
from langchain.agents.middleware import before_model
from langgraph.runtime import Runtime
from typing import Any
from llm_config import default_llm

@before_model
def trim_messages(state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
    """Keep only the last few messages to fit context window."""
    messages = state["messages"]

    if len(messages) <= 3:
        return None  # No changes needed

    # Keep first message (system) and last few messages
    first_msg = messages[0]
    recent_messages = messages[-3:] if len(messages) % 2 == 0 else messages[-4:]
    new_messages = [first_msg] + recent_messages

    return {
        "messages": [
                RemoveMessage(id=REMOVE_ALL_MESSAGES),
                *new_messages
            ]
    }

# Create agent with trimming middleware
agent = create_agent(
    default_llm,
    tools=[],
    middleware=[trim_messages],
    checkpointer=InMemorySaver(),
)

config = {"configurable": {"thread_id": "1"}}

# Simulate multiple interactions
print("Trimming messages to keep conversation manageable...")
result = agent.invoke({"messages": "hi, my name is bob"}, config)
result = agent.invoke({"messages": "write a short poem about cats"}, config)
result = agent.invoke({"messages": "now do same but for dogs"}, config)
final_response = agent.invoke({"messages": "what's my name?"}, config)

print(f"Final response: {final_response['messages'][-1].content}")
