"""
8. LLM Tool Selector Middleware Example

Use an LLM to intelligently select relevant tools before calling the main model.
Reduces token usage by filtering irrelevant tools and improves model focus.
"""

from langchain.agents import create_agent
from langchain.agents.middleware import LLMToolSelectorMiddleware
from langchain.tools import tool
from langchain.messages import HumanMessage
from llm_config import get_llm

print("=" * 60)
print("LLM Tool Selector Middleware Example")
print("Intelligently select relevant tools before main model call")
print("=" * 60)


@tool
def calculator(expression: str) -> str:
    """Calculate a mathematical expression."""
    print(f"\n[TOOL EXECUTION] calculator called with expression: {expression}")
    try:
        result = eval(expression)
        print(f"[TOOL RESULT]: {result}")
        return str(result)
    except Exception as e:
        error = f"Error calculating {expression}: {str(e)}"
        print(f"[TOOL ERROR]: {error}")
        return error


@tool
def weather_search(city: str) -> str:
    """Get the current weather for a city."""
    print(f"\n[TOOL EXECUTION] weather_search called for city: {city}")
    result = f"The weather in {city} is currently 72°F and sunny."
    print(f"[TOOL RESULT]: {result}")
    return result


@tool
def web_search(query: str) -> str:
    """Search the web for information."""
    print(f"\n[TOOL EXECUTION] web_search called with query: {query}")
    result = f"Search results for '{query}': Found relevant documentation and recent articles."
    print(f"[TOOL RESULT]: {result}")
    return result


@tool
def translate_text(text: str, target_language: str) -> str:
    """Translate text to a target language."""
    print(f"\n[TOOL EXECUTION] translate_text called: text='{text[:30]}...', target={target_language}")
    result = f"[Translated to {target_language}] This is the translated text."
    print(f"[TOOL RESULT]: {result}")
    return result


@tool
def get_stock_price(symbol: str) -> str:
    """Get the current stock price for a symbol."""
    print(f"\n[TOOL EXECUTION] get_stock_price called for symbol: {symbol}")
    result = f"The current price of {symbol} is $150.25."
    print(f"[TOOL RESULT]: {result}")
    return result


# We have 5 tools available
all_tools = [calculator, weather_search, web_search, translate_text, get_stock_price]
tool_names = [t.name for t in all_tools]

print(f"\n📋 Available tools: {', '.join(tool_names)}")
print("\n🔧 Configuration:")
print("   selection_model: gpt-4.1-mini")
print("   max_tools: 3 (select at most 3 relevant tools)")
print("   always_include: ['web_search'] (always include this regardless of selection)")

agent = create_agent(
    model=get_llm("gpt-4.1"),
    tools=all_tools,
    middleware=[
        LLMToolSelectorMiddleware(
            model=get_llm("gpt-4.1-mini"),
            max_tools=3,
            always_include=["web_search"],
        ),
    ],
)

print("\n✅ Agent created successfully!")

# Invoke with a query
print("\n🚀 Invoking agent with a query...")
print("   The selector will filter down to at most 3 relevant tools + web_search")
query = "What's the current weather in San Francisco?"
print(f"\n👤 User: {query}")
print("\n🤖 Selection LLM selects relevant tools first, then main model responds...")
print("-" * 60)

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

print("\n" + "=" * 60)
print("LLM Tool Selector middleware example completed!")
print("\n💡 Benefits:")
print("   - Reduces token usage by filtering irrelevant tools")
print("   - Improves model focus when you have 10+ tools available")
print("   - Only the selected tools are passed to the main model")

