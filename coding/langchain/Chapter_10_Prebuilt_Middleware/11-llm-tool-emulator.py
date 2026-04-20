"""
11. LLM Tool Emulator Middleware Example

Emulate tool execution using an LLM for testing purposes, replacing actual
tool calls with AI-generated responses.
"""

from langchain.agents import create_agent
from langchain.agents.middleware import LLMToolEmulator
from langchain.tools import tool
from langchain.messages import HumanMessage
from llm_config import get_llm

print("=" * 60)
print("LLM Tool Emulator Middleware Example")
print("Emulate tool calls with LLM-generated responses for testing")
print("=" * 60)


@tool
def get_weather(location: str) -> str:
    """Get the current weather for a location."""
    # This would actually call a weather API in production
    print(f"\n[ACTUAL TOOL would be called here] get_weather({location})")
    return f"Weather in {location}"


@tool
def send_email(to: str, subject: str, body: str) -> str:
    """Send an email to a recipient."""
    # This would actually connect to an email server in production
    print(f"\n[ACTUAL TOOL would be called here] send_email(to={to}, subject={subject})")
    return "Email sent"


print("\n🔧 Configuration - Emulate all tools:")
print("   All tools: get_weather, send_email")
print("   Emulation model: same as agent model (gpt-4.1)")

# Emulate all tools (default behavior)
agent = create_agent(
    model=get_llm("gpt-4.1"),
    tools=[get_weather, send_email],
    middleware=[LLMToolEmulator()],
)

print("\n✅ Agent created with full tool emulation!")
print("   All tool calls will be emulated by LLM - no actual API calls made")

# Emulate specific tools only
print("\n📋 Also defined: agent that only emulates get_weather")
print("   send_email still makes actual calls if used")

agent2 = create_agent(
    model=get_llm("gpt-4.1"),
    tools=[get_weather, send_email],
    middleware=[LLMToolEmulator(tools=["get_weather"])],
)

# Invoke the full-emulation agent with a query
print("\n🚀 Invoking agent with full emulation...")
query = "What's the weather like in New York today?"
print(f"\n👤 User: {query}")
print("\n🤖 LLM will emulate the get_weather tool call...")
print("   No actual weather API will be called!")
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
print("LLM Tool Emulator middleware example completed!")
print("\n💡 Use cases:")
print("   - Testing agent behavior without executing real tools")
print("   - Developing when external tools are unavailable")
print("   - Prototyping workflows before implementing actual tools")
print("\n📐 Configuration options:")
print("   - tools: List specific tools to emulate (None = all tools)")
print("   - model: Use different model for emulation (default = agent model)")

