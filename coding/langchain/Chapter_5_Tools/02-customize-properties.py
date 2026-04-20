"""
2. Customize Tool Properties

You can customize the tool name and description instead of
using defaults from the function name and docstring.
"""

from langchain.tools import tool
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from llm_config import get_llm

print("=" * 60)
print("2. Customize Tool Properties Example")
print("Custom name, description, and parameter details")
print("=" * 60)


# Customize name and description via decorator arguments
@tool(
    name="calculator_add",
    description="Add two numbers together. Use this when you need to calculate a sum."
)
def add(a: float, b: float) -> float:
    """This docstring won't be used because we provided a custom description."""
    print(f"\n[TOOL EXECUTION] calculator_add called with a={a}, b={b}")
    result = a + b
    print(f"[TOOL RESULT]: {a} + {b} = {result}")
    return result


# Customize with argument descriptions in the docstring
@tool
def search_web(query: str, max_results: int = 5) -> str:
    """Search the web for information on a topic.

    Args:
        query: The search query to look up. Be specific for better results.
        max_results: Maximum number of results to return. Defaults to 5.

    Use this when you need up-to-date information not contained in your training data.
    """
    print(f"\n[TOOL EXECUTION] search_web called with query={query}, max_results={max_results}")
    result = f"Found {max_results} results for '{query}':\n"
    result += "1. Example result one\n"
    result += "2. Example result two\n"
    result += "3. Example result three"
    print(f"[TOOL RESULT]: {result}")
    return result


# Disable parsing of docstring for parameter descriptions
@tool(
    parse_docstring=False,
    description="Get current weather for a city"
)
def get_weather(city: str) -> str:
    # Without parse_docstring, the entire docstring is not parsed for parameters
    print(f"\n[TOOL EXECUTION] get_weather called with city={city}")
    result = f"The weather in {city} is 65°F and cloudy."
    print(f"[TOOL RESULT]: {result}")
    return result


print("\n🔧 Configuration:")
print("   - calculator_add: Custom name and description")
print("   - search_web: Docstring parsing with detailed parameter descriptions")
print("   - get_weather: parse_docstring=False, no parameter docs from docstring")

# Create agent
agent = create_agent(
    model=get_llm("gpt-4.1"),
    tools=[add, search_web, get_weather],
    middleware=[],
)

print("\n✅ Agent created successfully!")

# Invoke
print("\n🚀 Invoking agent...")
query = "Add 15.5 and 27.3, then search for information about LangChain tools with 3 results, and get the weather in Boston."
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
print("Customize properties example completed!")
print("\n💡 Customization options:")
print("   - name: Override the default function name")
print("   - description: Override the docstring-based description")
print("   - parse_docstring: Disable docstring parsing for parameters")
print("   - Docstring args become parameter descriptions in the schema")
