"""
10. Model Retry Middleware Example

Automatically retry failed model calls with configurable exponential backoff.
"""

from langchain.agents import create_agent
from langchain.agents.middleware import ModelRetryMiddleware
from langchain.tools import tool
from langchain.messages import HumanMessage
from llm_config import get_llm

print("=" * 60)
print("Model Retry Middleware Example")
print("Auto-retry failed model calls with exponential backoff")
print("=" * 60)


@tool
def web_search(query: str) -> str:
    """Search the web for information about a query."""
    print(f"\n[TOOL EXECUTION] web_search called with query: {query}")
    result = f"Search results for '{query}': LangChain model retry middleware automatically handles transient failures."
    print(f"[TOOL RESULT]: {result}")
    return result


print("\n🔧 Configuration for default agent:")
print("   max_retries: 2 (default)")
print("   backoff_factor: 2.0 (default)")
print("   initial_delay: 1.0 (default)")
print("   on_failure: continue (default) - return error in AIMessage")

# Basic usage with default settings (2 retries, exponential backoff)
agent = create_agent(
    model=get_llm("gpt-4.1"),
    tools=[web_search],
    middleware=[ModelRetryMiddleware()],
)

print("\n✅ Default agent created successfully!")

# Show different configuration options
print("\n📐 Other configuration examples defined in code:")
print("   1. Retry only specific exceptions (TimeoutError, ConnectionError)")
print("   2. Custom filter function to decide what to retry")
print("   3. Custom error formatting function")
print("   4. Constant backoff (no exponential growth)")
print("   5. Strict mode - raise exception on failure")

# Custom exception filtering (defined but not used in this invocation)
class TimeoutError(Exception):
    """Custom exception for timeout errors."""
    pass

class ConnectionError(Exception):
    """Custom exception for connection errors."""
    pass

# Retry specific exceptions only
retry = ModelRetryMiddleware(
    max_retries=4,
    retry_on=(TimeoutError, ConnectionError),
    backoff_factor=1.5,
)

def should_retry(error: Exception) -> bool:
    # Only retry on rate limit errors
    if isinstance(error, TimeoutError):
        return True
    # Or check for specific HTTP status codes
    if hasattr(error, "status_code"):
        return error.status_code in (429, 503)
    return False

retry_with_filter = ModelRetryMiddleware(
    max_retries=3,
    retry_on=should_retry,
)

# Invoke with a query
print("\n🚀 Invoking agent with default configuration...")
query = "Explain how exponential backoff works for retrying failed API calls."
print(f"\n👤 User: {query}")
print("\n🤖 LLM is generating response... Any failures will be retried automatically.")
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
print("Model Retry middleware example completed!")
print("\n💡 Configuration options summary:")
print("   - max_retries: Number of retry attempts after initial call")
print("   - retry_on: Tuple of exception types or filter function")
print("   - backoff_factor: 0.0 for constant delay, >1.0 for exponential growth")
print("   - on_failure: 'continue'|'error'|custom function to handle exhausted retries")
print("   - jitter: Add ±25% randomness to avoid thundering herd")

