"""04_delete_messages.py
Delete messages from graph state using RemoveMessage.
"""

from langchain.messages import RemoveMessage
from langchain.agents import create_agent, AgentState
from langchain.agents.middleware import after_model
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.runtime import Runtime
from llm_config import default_llm

@after_model
def delete_old_messages(state: AgentState, runtime: Runtime) -> dict | None:
    """Remove old messages to keep conversation manageable."""
    messages = state["messages"]
    if len(messages) > 2:
        # Remove earliest two messages
        return {"messages": [RemoveMessage(id=m.id) for m in messages[:2]]}
    return None

# Create agent with delete middleware
agent = create_agent(
    default_llm,
    tools=[],
    system_prompt="Please be concise and to the point.",
    middleware=[delete_old_messages],
    checkpointer=InMemorySaver(),
)

config = {"configurable": {"thread_id": "1"}}

print("Deleting old messages to manage conversation length...")
for event in agent.stream(
    {"messages": [{"role": "user", "content": "hi! I'm bob"}]},
    config,
    stream_mode="values",
):
    if "messages" in event:
        message_types = [(message.type, message.content[:50]) for message in event["messages"]]
        print(f"Messages: {message_types}")

for event in agent.stream(
    {"messages": [{"role": "user", "content": "what's my name?"]},
    config,
    stream_mode="values",
):
    if "messages" in event:
        message_types = [(message.type, message.content[:50]) for message in event["messages"]]
        print(f"Messages: {message_types}")
