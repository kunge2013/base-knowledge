"""
9. Tool Retry Middleware Example

Automatically retry failed tool calls with configurable exponential backoff.
"""

from langchain.agents import create_agent
from langchain.agents.middleware import ToolRetryMiddleware
from langchain.tools import tool
from langchain.messages import HumanMessage
from llm_config import get_llm
import random

print("=" * 60)
print("Tool Retry Middleware Example")
print("Auto-retry failed tool calls with exponential backoff")
print("=" * 60)


# Simulate an unreliable API tool that sometimes fails
call_count = 0

@tool
def unreliable_api_call(endpoint: str) -> str:
    """Call an unreliable external API endpoint that sometimes fails."""
    global call_count
    call_count += 1
    print(f"\n[TOOL EXECUTION] unreliable_api_call called (attempt #{call_count}): endpoint={endpoint}")

    # Simulate random failures - 50% chance to fail on first two attempts
    if call_count <= 2 and random.random() < 0.5:
        error_msg = f"Connection timeout connecting to {endpoint} - attempt #{call_count} failed"
        print(f"[TOOL FAILED]: {error_msg}")
        raise TimeoutError(error_msg)

    result = f"Success! API response from {endpoint}: {{'status': 'ok', 'data': 'example response data'}}"
    print(f"[TOOL SUCCESS]: {result}")
    return result


@tool
def stable_search(query: str) -> str:
    """Stable search tool that doesn't need retries."""
    print(f"\n[TOOL EXECUTION] stable_search called with query: {query}")
    result = f"Search results for '{query}': Found 5 relevant results."
    print(f"[TOOL RESULT]: {result}")
    return result


print("\n🔧 Configuration:")
print("   max_retries: 3")
print("   backoff_factor: 2.0 (exponential growth)")
print("   initial_delay: 1.0 seconds")
print("   max_delay: 60.0 seconds")
print("   jitter: True (add random variation)")
print("   retry_on: (ConnectionError, TimeoutError)")
print("   Only applies to: ['unreliable_api_call']")

agent = create_agent(
    model=get_llm("gpt-4.1"),
    tools=[stable_search, unreliable_api_call],
    middleware=[
        ToolRetryMiddleware(
            max_retries=3,
            backoff_factor=2.0,
            initial_delay=1.0,
            max_delay=60.0,
            jitter=True,
            tools=["unreliable_api_call"],
            retry_on=(ConnectionError, TimeoutError),
            on_failure="return_message",
        ),
    ],
)

print("\n✅ Agent created successfully!")

# Invoke with a query
print("\n🚀 Invoking agent...")
query = "Call the unreliable API at http://192.168.2.163:15000/portal/#/enterpriseCustBill and tell me the result."
print(f"\n👤 User: {query}")
print("\n🤖 LLM is processing... If tool fails, automatic retry will happen.")
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
print("Tool Retry middleware example completed!")
print("\n💡 Retry logic:")
print("   - First retry waits: initial_delay * (backoff_factor ^ 0) = 1.0s")
print("   - Second retry waits: initial_delay * (backoff_factor ^ 1) = 2.0s")
print("   - Third retry waits: initial_delay * (backoff_factor ^ 2) = 4.0s")
print("   - Jitter adds ±25% randomness to avoid thundering herd")

