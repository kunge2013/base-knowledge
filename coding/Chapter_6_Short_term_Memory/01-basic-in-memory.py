"""
1. Basic Short-term Memory with InMemorySaver

Basic example of adding short-term memory to an agent using InMemorySaver.
Short-term memory remembers previous interactions within a single thread/conversation.
"""

from langchain.agents import create_agent
from langchain.tools import tool
from langgraph.checkpoint.memory import InMemorySaver
from langchain.messages import HumanMessage
from llm_config import get_llm

print("=" * 60)
print("1. Basic Short-term Memory Example")
print("InMemorySaver for thread-level conversation persistence")
print("=" * 60)


@tool
def get_user_info(user_id: str) -> str:
    """Get user information by user ID.

    Args:
        user_id: The ID of the user to look up
    """
    print(f"\n[TOOL EXECUTION] get_user_info called with user_id={user_id}")
    result = f"User {user_id}: John Smith, john@example.com"
    print(f"[TOOL RESULT]: {result}")
    return result


print("\n🔧 Configuration:")
print("   - Checkpointer: InMemorySaver()")
print("   - Thread ID configurable via config")
print("   - State persisted in memory for the running process")
print("   - Good for development and testing")

# Create agent with checkpointer for short-term memory
checkpointer = InMemorySaver()

agent = create_agent(
    model=get_llm("gpt-4.1"),
    tools=[get_user_info],
    checkpointer=checkpointer,
)

print("\n✅ Agent created successfully with InMemorySaver!")

# First turn - introduce yourself
print("\n🚀 First turn: Introduce yourself")
config = {"configurable": {"thread_id": "conversation_1"}}
print(f"   Thread ID: {config['configurable']['thread_id']}")
print(f"   User: Hi! My name is Bob.")
print("-" * 60)

try:
    result = agent.invoke(
        {"messages": [HumanMessage(content="Hi! My name is Bob.")]},
        config,
    )

    print("\n📄 Agent response:")
    if isinstance(result, dict) and 'messages' in result:
        last_msg = result['messages'][-1]
        if hasattr(last_msg, 'content'):
            print(last_msg.content)
    print(f"\n[STATE] Checkpointer saved state for thread_id=conversation_1")

    # Second turn - ask to recall
    print("\n" + "=" * 40)
    print("🚀 Second turn - Ask who you are (should remember)")
    print(f"   Thread ID: {config['configurable']['thread_id']}")
    print(f"   User: What's my name?")
    print("-" * 60)

    result2 = agent.invoke(
        {"messages": [HumanMessage(content="What's my name?")]},
        config,
    )

    print("\n📄 Agent response:")
    if isinstance(result2, dict) and 'messages' in result2:
        last_msg2 = result2['messages'][-1]
        if hasattr(last_msg2, 'content'):
            print(last_msg2.content)

    # Different thread should not remember
    print("\n" + "=" * 40)
    print("🚀 New thread - different conversation")
    config2 = {"configurable": {"thread_id": "conversation_2"}}
    print(f"   New Thread ID: {config2['configurable']['thread_id']}")
    print(f"   User: What's my name?")
    print("-" * 60)

    result3 = agent.invoke(
        {"messages": [HumanMessage(content="What's my name?")]},
        config2,
    )

    print("\n📄 Agent response (new thread):")
    if isinstance(result3, dict) and 'messages' in result3:
        last_msg3 = result3['messages'][-1]
        if hasattr(last_msg3, 'content'):
            print(last_msg3.content)

except Exception as e:
    print("-" * 60)
    print(f"\n❌ Error: {type(e).__name__}: {e}")
    print("\nThis example requires a valid OpenAI API key configured in .env")

print("\n" + "=" * 60)
print("Basic in-memory short-term memory example completed!")
print("\n💡 Key points:")
print("   - checkpointer persists agent state between invocations")
print("   - thread_id separates different conversations")
print("   - InMemorySaver is in-memory only (lost on restart)")
print("   - Use database-backed checkpointer in production")
