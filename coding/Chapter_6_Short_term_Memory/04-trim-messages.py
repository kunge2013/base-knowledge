"""
4. Trim Messages (before_model middleware)

Trim messages to keep context window manageable.
This example uses the @before_model middleware decorator to trim messages before LLM call.
"""

from typing import Any
from langchain.messages import RemoveMessage
from langgraph.graph.message import REMOVE_ALL_MESSAGES
from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents import create_agent, AgentState
from langchain.agents.middleware import before_model
from langchain_core.runnables import RunnableConfig
from langchain.messages import HumanMessage
from llm_config import get_llm

print("=" * 60)
print("4. Trim Messages Example")
print("@before_model middleware trims messages to fit context window")
print("=" * 60)


@before_model
def trim_messages(state: AgentState, runtime) -> dict[str, Any] | None:
    """Keep only the last few messages to fit context window.

    Args:
        state: Current agent state with messages
        runtime: Runtime context (unused here)

    Returns:
        Updated messages dict or None if no change needed
    """
    messages = state["messages"]
    print(f"\n[TRIM] Trimming messages... Current count: {len(messages)}")

    if len(messages) <= 3:
        print("[TRIM] No trimming needed - 3 or fewer messages")
        return None  # No changes needed

    # Strategy: Keep the first message (usually system) and last N
    first_msg = messages[0]
    # Keep last 3-4 messages depending on even/odd to maintain chat turn pattern
    recent_messages = messages[-3:] if len(messages) % 2 == 0 else messages[-4:]
    new_messages = [first_msg] + recent_messages

    print(f"[TRIM] Trimmed from {len(messages)} to {len(new_messages)} messages")

    return {
        "messages": [
            RemoveMessage(id=REMOVE_ALL_MESSAGES),
            *new_messages
        ]
    }


print("\n🔧 Configuration:")
print("   - @before_model decorator runs before LLM call")
print("   - Trims messages to keep last 3-4 messages plus first")
print("   - Adjust the number based on your context window size")
print("   - Uses RemoveMessage with REMOVE_ALL_MESSAGES to clear")

checkpointer = InMemorySaver()

agent = create_agent(
    get_llm("gpt-4.1"),
    tools=[],
    middleware=[trim_messages],
    checkpointer=checkpointer,
)

config: RunnableConfig = {"configurable": {"thread_id": "1"}}

print("\n✅ Agent created with trim_messages middleware!")
print("\n🚀 Making multiple turns to demonstrate trimming...")

# Multiple interaction turns
turns = [
    "hi, my name is bob",
    "write a short poem about cats",
    "now do the same but for dogs",
    "what's my name?",
]

for i, turn in enumerate(turns):
    print(f"\n{'='*50}")
    print(f"Turn {i+1}: {turn}")
    print("-" * 50)

    try:
        result = agent.invoke({"messages": HumanMessage(content=turn)}, config)

        # Print final message
        print("\n📄 Response:")
        if isinstance(result, dict) and 'messages' in result:
            print(f"Total messages after this turn: {len(result['messages'])}")
            last_msg = result['messages'][-1]
            if hasattr(last_msg, 'content'):
                print(f"\nFinal response: {last_msg.content[:200]}...")

    except Exception as e:
        print("-" * 50)
        print(f"\n❌ Error: {type(e).__name__}: {e}")
        print("\nThis example requires a valid OpenAI API key configured in .env")
        break

print("\n" + "=" * 60)
print("Trim messages example completed!")
print("\n💡 Trimming strategy:")
print("   - Simple: keep N most recent messages")
print("   - Preserves the conversation turn pattern (alternating user/assistant)")
print("   - Runs automatically before every LLM call")
print("   - Good when you just need to fit within context window")
print("   - Loses older information - use summarization if you need to retain info")
