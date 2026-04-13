"""
1. Basic Tool Definition

The simplest way to create a tool is using the `@tool` decorator.
Type hints and docstrings are automatically converted to tool schema.
"""

from langchain.tools import tool
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from llm_config import get_llm

print("=" * 60)
print("1. Basic Tool Definition Example")
print("Using @tool decorator with type hints and docstrings")
print("=" * 60)


@tool
def multiply(a: int, b: int) -> int:
    """Multiply two integers together.

    Args:
        a: First integer to multiply
        b: Second integer to multiply

    Returns:
        Product of the two integers
    """
    print(f"\n[TOOL EXECUTION] multiply called with a={a}, b={b}")
    result = a * b
    print(f"[TOOL RESULT]: {a} * {b} = {result}")
    return result


@tool
def greet(name: str) -> str:
    """Greet a person by name.

    Args:
        name: Name of the person to greet

    Returns:
        A greeting message
    """
    print(f"\n[TOOL EXECUTION] greet called with name={name}")
    result = f"Hello, {name}! Nice to meet you!"
    print(f"[TOOL RESULT]: {result}")
    return result


print("\n🔧 Configuration:")
print("   Two tools defined with @tool decorator:")
print("   - multiply: Multiplies two integers")
print("   - greet: Greets a person by name")
print("   Type hints → automatic parameter schema")
print("   Docstring → automatic tool description")

# Create agent with the tools
agent = create_agent(
    model=get_llm("gpt-4.1"),
    tools=[multiply, greet],
    middleware=[],
)

print("\n✅ Agent created successfully!")

# Invoke with a query
print("\n🚀 Invoking agent...")
query = "What is 17 times 23? Also greet the user named Alice."
print(f"\n👤 User: {query}")
print("🤖 LLM is processing...")
print("-" * 60)

try:
    result = agent.invoke({
        "messages": [HumanMessage(content=query)]
    })

    print("-" * 60)
    print("\n📄 Final Response:")
    if isinstance(result, dict) and 'messages' in result:
        last_msg = result['messages'][-1]
        if hasattr(last_msg, 'content'):
            print(last_msg.content)
        else:
            print(last_msg)
    else:
        print(result)
except Exception as e:
    print("-" * 60)
    print(f"\n❌ Error invoking LLM: {type(e).__name__}: {e}")
    print("\nThis example requires a valid OpenAI API key configured in .env")

print("\n" + "=" * 60)
print("Basic tool definition example completed!")
print("\n💡 Key points:")
print("   - @tool decorator converts function to LangChain Tool")
print("   - Type hints automatically generate JSON schema")
print("   - Docstring becomes the tool description for the LLM")
print("   - Simple, clean, minimal code")
