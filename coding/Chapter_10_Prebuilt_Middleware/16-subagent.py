"""
16. Subagent Middleware Example

Handing off tasks to subagents isolates context, keeping the main (supervisor)
agent's context window clean while still going deep on a task.
"""

from langchain.tools import tool
from langchain.agents import create_agent
from deepagents.middleware.subagents import SubAgentMiddleware
from langchain.messages import HumanMessage
from llm_config import get_llm

print("=" * 60)
print("Subagent Middleware Example")
print("Delegate to subagents for context isolation, keep main context clean")
print("=" * 60)


@tool
def get_weather(city: str) -> str:
    """Get the weather in a city."""
    print(f"\n[SUBAGENT TOOL EXECUTION] get_weather called for city: {city}")
    result = f"The weather in {city} is currently 72°F and sunny."
    print(f"[TOOL RESULT]: {result}")
    return result


@tool
def search_web(query: str) -> str:
    """Search the web for general information."""
    print(f"\n[MAIN TOOL EXECUTION] search_web called with query: {query}")
    result = f"Search results for '{query}': Found general information about weather reporting."
    print(f"[TOOL RESULT]: {result}")
    return result


print("\n🔧 Configuration:")
print("   Defined subagent: 'weather' - specialized for getting weather")
print("   The weather subagent has its own tools: [get_weather]")
print("   Main agent has search_web for general queries")
print("   general-purpose subagent always available for complex delegation")

# Basic usage with defined subagents
agent = create_agent(
    model=get_llm("claude-sonnet-4-6"),
    tools=[search_web],
    middleware=[
        SubAgentMiddleware(
            default_model="claude-sonnet-4-6",
            default_tools=[],
            subagents=[
                {
                    "name": "weather",
                    "description": "This subagent specializes in getting weather information for cities.",
                    "system_prompt": "You are a weather specialist. Use the get_weather tool to get the weather and answer the question concisely.",
                    "tools": [get_weather],
                    "model": get_llm("gpt-4.1"),
                    "middleware": [],
                }
            ],
        )
    ],
)

print("\n✅ Agent created successfully!")
print("\nSubagents defined: weather")
print("A general-purpose subagent is also always available for context isolation.")

# Invoke with a query that should delegate to the weather subagent
print("\n🚀 Invoking agent...")
query = "What's the current weather in San Francisco? Also tell me briefly why weather forecasting is useful."
print(f"\n👤 User: {query}")
print("\n🤖 Main agent should delegate the weather question to the weather subagent.")
print("   This keeps intermediate tool calls out of the main agent context.")
print("-" * 60)

result = agent.invoke({
    "messages": [HumanMessage(content=query)]
})

print("-" * 60)
print("\n📄 Final Response from main agent:")
if isinstance(result, dict) and 'messages' in result:
    last_msg = result['messages'][-1]
    if hasattr(last_msg, 'content'):
        print(last_msg.content)
    else:
        print(last_msg)
else:
    print(result)

print("\n" + "=" * 60)
print("Subagent middleware example completed!")
print("\n💡 Benefits:")
print("   - Context isolation: subagent tool calls don't bloat main context")
print("   - Specialization: different subagents can have different tools/models")
print("   - Cleaner context window for main agent")
print("   - General-purpose subagent always available for complex task delegation")
print("\n   The main agent gets a concise answer back without the intermediate noise.")

