"""
9. After Model: Response Validation

Use @after_model middleware to validate or modify the model's response
after it completes but before returning to the user. This example
demonstrates filtering sensitive content from responses.
"""

from langchain.messages import RemoveMessage
from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents import create_agent, AgentState
from langchain.agents.middleware import after_model
from langgraph.runtime import Runtime
from llm_config import get_llm

print("=" * 60)
print("9. After Model: Response Validation Example")
print("@after_model middleware validates/filters response after generation")
print("=" * 60)


@after_model
def validate_response(state: AgentState, runtime: Runtime) -> dict | None:
    """Remove messages containing sensitive words before they leave the server.

    Args:
        state: Current agent state after model response
        runtime: Runtime context

    Returns:
        Update dict to remove bad message, or None if no change
    """
    STOP_WORDS = ["password", "secret", "token", "api_key", "credentials"]
    last_message = state["messages"][-1]

    print(f"\n[VALIDATION] Checking last message for sensitive words...")
    print(f"[VALIDATION] Prohibited words: {STOP_WORDS}")

    content = last_message.content.lower() if hasattr(last_message, 'content') else ""

    for word in STOP_WORDS:
        if word in content:
            print(f"[VALIDATION] Found prohibited word: '{word}' - removing message")
            return {"messages": [RemoveMessage(id=last_message.id)]}

    print(f"[VALIDATION] OK - no prohibited words found")
    return None


print("\n🔧 Configuration:")
print("   - @after_model runs after model generates response")
print("   - Checks last message for sensitive words")
print("   - Removes message if prohibited word found")
print("   - This happens before the response is returned")

checkpointer = InMemorySaver()

agent = create_agent(
    model=get_llm("gpt-4.1"),
    tools=[],
    middleware=[validate_response],
    checkpointer=checkpointer,
)

print("\n✅ Agent created with after_model validation middleware!")

# Test with safe query
print("\n🚀 Test 1: Safe query - no sensitive content")
print(f"   User: Tell me a joke about programming")
print("-" * 60)

try:
    result = agent.invoke(
        {"messages": [{"role": "user", "content": "Tell me a joke about programming"}]},
        {"configurable": {"thread_id": "1"}},
    )

    print("-" * 60)
    print("\n📄 Final Response:")
    if isinstance(result, dict) and 'messages' in result:
        last_msg = result['messages'][-1]
        if hasattr(last_msg, 'content'):
            print(last_msg.content)

    # The validation would already have run and accepted this

except Exception as e:
    print("-" * 60)
    print(f"\n❌ Error: {type(e).__name__}: {e}")
    print("\nThis example requires a valid OpenAI API key configured in .env")

print("\n" + "=" * 60)
print("After model validation example completed!")
print("\n💡 Use cases for @after_model:")
print("   - Content filtering (sensitive words, PII, harmful content)")
print("   - Response validation against schema")
print("   - Logging and auditing of all responses")
print("   - Post-processing (formatting, cleanup)")
print("   - Metrics collection (response length, latency, etc.)")
print("   - Runs after model, before returning to client")
