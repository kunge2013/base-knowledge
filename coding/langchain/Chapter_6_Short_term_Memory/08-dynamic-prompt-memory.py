"""
8. Dynamic Prompt from Memory

Use dynamic_prompt middleware to create dynamic system prompts based on
short-term memory (custom state fields). This example demonstrates
how to personalize prompts using stored user information.
"""

from typing import TypedDict
from langchain.agents import create_agent
from langchain.agents.middleware import dynamic_prompt, ModelRequest
from langchain.tools import tool
from llm_config import get_llm

print("=" * 60)
print("8. Dynamic Prompt from Memory Example")
print("dynamic_prompt middleware creates personalized prompts from state")
print("=" * 60)


# Define custom context type
class CustomContext(TypedDict):
    user_name: str


# Example tool
@tool
def get_weather(city: str) -> str:
    """Get the weather in a city.

    Args:
        city: The city to get weather for
    """
    print(f"\n[TOOL EXECUTION] get_weather called for city: {city}")
    result = f"The weather in {city} is 68°F and partly cloudy."
    print(f"[TOOL RESULT]: {result}")
    return result


@dynamic_prompt
def dynamic_system_prompt(request: ModelRequest) -> str:
    """Dynamic system prompt that uses user name from context."""
    # Access context from request.runtime
    user_name = request.runtime.context["user_name"]

    print(f"\n[DYNAMIC PROMPT] Building system prompt for user: {user_name}")

    # Get current message count
    messages = request.state["messages"]
    message_count = len(messages)
    print(f"[DYNAMIC PROMPT] Current message count: {message_count}")

    # Build dynamic prompt that includes user name and conversation context
    system_prompt = f"""You are a helpful assistant.

The current user is: {user_name}
Address the user by name throughout the conversation.

This is turn #{message_count} in this conversation. Be conversational but concise.
"""
    print(f"[DYNAMIC PROMPT] Generated prompt length: {len(system_prompt)} characters")

    return system_prompt


print("\n🔧 Configuration:")
print("   - @dynamic_prompt middleware decorator")
print("   - Accesses context from request.runtime.context")
print("   - Accesses state from request.state")
print("   - Returns dynamic system prompt string")
print("   - Personalization based on stored user information")

# Create agent with dynamic prompt middleware
agent = create_agent(
    model=get_llm("gpt-4.1"),
    tools=[get_weather],
    middleware=[dynamic_system_prompt],
    context_schema=CustomContext,
)

print("\n✅ Agent created with dynamic_prompt middleware!")

# Invoke
print("\n🚀 Invoking agent...")
print(f"   User query: What is the weather in San Francisco?")
print(f"   context: {{'user_name': 'John Smith'}}")
print("-" * 60)

try:
    result = agent.invoke(
        {"messages": [{"role": "user", "content": "What is the weather in San Francisco?"}]},
        context=CustomContext(user_name="John Smith"),
    )

    print("-" * 60)
    print("\n📄 Complete conversation:")
    if isinstance(result, dict) and 'messages' in result:
        for msg in result['messages']:
            msg.pretty_print()

except Exception as e:
    print("-" * 60)
    print(f"\n❌ Error: {type(e).__name__}: {e}")
    print("\nThis example requires a valid OpenAI API key configured in .env")

print("\n" + "=" * 60)
print("Dynamic prompt from memory example completed!")
print("\n💡 Use cases for dynamic prompts:")
print("   - Personalization: address user by name, use preferences")
print("   - Conversation awareness: include turn count, summary")
print("   - Dynamic instructions based on current state")
print("   - Context-aware system prompts")
print("   - Runs before every model invocation")
