"""
3. Custom State Schema

Extend AgentState to add custom fields for additional short-term memory.
This lets you store more than just conversation history in your agent state.
"""

from langchain.agents import create_agent, AgentState
from langchain.tools import tool
from langgraph.checkpoint.memory import InMemorySaver
from langchain.messages import HumanMessage
from llm_config import get_llm

print("=" * 60)
print("3. Custom State Schema Example")
print("Extend AgentState to add custom fields to agent state")
print("=" * 60)


@tool
def get_user_preferences(user_id: str) -> str:
    """Get user preferences from database.

    Args:
        user_id: User ID to get preferences for
    """
    print(f"\n[TOOL EXECUTION] get_user_preferences called for user_id={user_id}")
    result = '{"theme": "dark", "notifications": "enabled", "language": "en"}'
    print(f"[TOOL RESULT]: {result}")
    return result


# Extend AgentState to add custom fields
class CustomAgentState(AgentState):
    """Custom agent state with additional fields for short-term memory."""
    user_id: str          # Store current user ID
    preferences: dict     # Store user preferences in memory


print("\n🔧 Configuration:")
print("   - CustomAgentState extends base AgentState")
print("   - Adds: user_id: str, preferences: dict")
print("   - Pass via state_schema parameter to create_agent")
print("   - Custom fields persisted with checkpointer")

# Create checkpointer
checkpointer = InMemorySaver()

# Create agent with custom state schema
agent = create_agent(
    model=get_llm("gpt-4.1"),
    tools=[get_user_preferences],
    state_schema=CustomAgentState,
    checkpointer=checkpointer,
)

print("\n✅ Agent created with custom state schema!")

# Invoke with custom state fields
print("\n🚀 Invoking agent with custom state...")
config = {"configurable": {"thread_id": "thread_123"}}
query = {
    "messages": [HumanMessage(content="Hello, I need help with my account settings.")],
    "user_id": "user_123",
    "preferences": {},
}
print(f"\n👤 User: {query['messages'][0].content}")
print(f"   user_id: {query['user_id']}")
print(f"   initial preferences: {query['preferences']}")
print("-" * 60)

try:
    result = agent.invoke(query, config)

    print("-" * 60)
    print("\n📄 Final Response:")
    if isinstance(result, dict) and 'messages' in result:
        print(f"\nState contains custom fields:")
        print(f"   user_id: {result.get('user_id', 'NOT FOUND')}")
        print(f"   preferences: {result.get('preferences', 'NOT FOUND')}")
        print(f"\nNumber of messages in state: {len(result['messages'])}")
        print(f"\nFinal message from agent:")
        last_msg = result['messages'][-1]
        if hasattr(last_msg, 'content'):
            print(last_msg.content)

except Exception as e:
    print("-" * 60)
    print(f"\n❌ Error: {type(e).__name__}: {e}")
    print("\nThis example requires a valid OpenAI API key configured in .env")

print("\n" + "=" * 60)
print("Custom state schema example completed!")
print("\n💡 Benefits of custom state:")
print("   - Store domain-specific data in short-term memory")
print("   - Everything still persisted via checkpointer")
print("   - Type checked by Pydantic")
print("   - AgentState already provides messages with add_messages reducer")
print("   - Just add your extra fields and you're done")
