"""
5. Delete Messages (after_model middleware)

Delete specific old messages from the graph state to manage context window.
This example uses @after_model middleware to delete oldest messages after each turn.
"""

from langchain.messages import RemoveMessage
from langgraph.graph.message import REMOVE_ALL_MESSAGES
from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents import create_agent, AgentState
from langchain.agents.middleware import after_model
from langgraph.runtime import Runtime
from langchain_core.runnables import RunnableConfig
from langchain.messages import HumanMessage
from llm_config import get_llm

print("=" * 60)
print("5. Delete Messages Example")
print("@after_model middleware deletes old messages after LLM call")
print("=" * 60)


@after_model
def delete_old_messages(state: AgentState, runtime: Runtime) -> dict | None:
    """Remove old messages to keep conversation manageable.

    Args:
        state: Current agent state
        runtime: Runtime context

    Returns:
        Update dict with messages to delete, or None if no change
    """
    messages = state["messages"]
    print(f"\n[DELETE] Checking messages - current count: {len(messages)}")

    # Delete the earliest two messages when we have more than 2 messages
    if len(messages) > 2:
        to_delete = [RemoveMessage(id=m.id) for m in messages[:2]]
        print(f"[DELETE] Deleting {len(to_delete)} oldest messages")
        return {"messages": to_delete}

    print("[DELETE] No deletion needed - 2 or fewer messages")
    return None


print("\n🔧 Configuration:")
print("   - @after_model decorator runs after LLM call")
print("   - Deletes 2 oldest messages when > 2 messages")
print("   - Shows output after each deletion to demonstrate")

checkpointer = InMemorySaver()

agent = create_agent(
    get_llm("gpt-4.1"),
    tools=[],
    system_prompt="Please be concise and to the point.",
    middleware=[delete_old_messages],
    checkpointer=checkpointer,
)

config: RunnableConfig = {"configurable": {"thread_id": "1"}}

print("\n✅ Agent created with delete_old_messages middleware!")
print("\n🚀 Running conversation with automatic deletion...\n")

# Use stream to see message count after each step
turns = [
    "hi! I'm bob",
    "what's my name?",
]

try:
    for turn in turns:
        print(f"👤 User: {turn}")
        print("-" * 40)

        message_count_before = 0
        # Get current state before
        if checkpointer.get(config, ()):
            snapshot = checkpointer.get(config, ())
            if snapshot and 'values' in snapshot:
                message_count_before = len(snapshot['values'].get('messages', []))
                print(f"Message count before: {message_count_before}")

        for event in agent.stream(
            {"messages": [HumanMessage(content=turn)]},
            config,
            stream_mode="values",
        ):
            # After stream completes, we have the final state
            pass

        # Get final state after
        snapshot = checkpointer.get(config, ())
        if snapshot and 'values' in snapshot:
            messages = snapshot['values'].get('messages', [])
            message_count_after = len(messages)
            print(f"Message count after deletion: {message_count_after}")
            print("\nCurrent message history:")
            for i, msg in enumerate(messages):
                content_preview = msg.content[:40] + ('...' if len(msg.content) > 40 else '')
                print(f"  [{i}] {msg.type}: {content_preview}")

        print()

except Exception as e:
    print("-" * 40)
    print(f"\n❌ Error: {type(e).__name__}: {e}")
    print("\nThis example requires a valid OpenAI API key configured in .env")

print("\n" + "=" * 60)
print("Delete messages example completed!")
print("\n💡 Deletion patterns:")
print("   - @after_model runs after model response")
print("   - Delete oldest N messages to control growth")
print("   - Can delete specific messages by ID")
print("   - Use REMOVE_ALL_MESSAGES to clear entire history")
print("   - Requires add_messages reducer (default AgentState has it)")
print("\n⚠️  Important: Always keep a valid conversation sequence:")
print("   - Must start with a user message")
print("   - Tool calls must be followed by tool responses")
