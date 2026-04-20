"""
7. Server-Side Tool Use

When running tools on the server, there are special considerations:
- Authentication and authorization
- Rate limiting
- Timeout handling
- Error reporting
- Input validation
"""

from functools import wraps
from typing import Callable, Any, Dict, List, Optional
import time
import os
from pydantic import BaseModel, Field, ValidationError
from langchain.tools import tool
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from langchain_core.exceptions import ToolException
from llm_config import get_llm

print("=" * 60)
print("7. Server-Side Tool Use Example")
print("Best practices for server-side tool deployment")
print("=" * 60)


# Rate limiting decorator for server-side tools
class RateLimiter:
    """Simple rate limiter for server-side tools."""

    def __init__(self, max_calls: int, window_seconds: int) -> None:
        self.max_calls = max_calls
        self.window_seconds = window_seconds
        self.calls: Dict[str, List[float]] = {}

    def check_rate_limit(self, user_id: str) -> bool:
        """Check if user is within rate limit."""
        now = time.time()
        if user_id not in self.calls:
            self.calls[user_id] = []

        # Clean up old entries
        self.calls[user_id] = [
            t for t in self.calls[user_id]
            if now - t < self.window_seconds
        ]

        if len(self.calls[user_id]) >= self.max_calls:
            return False

        self.calls[user_id].append(now)
        return True


rate_limiter = RateLimiter(max_calls=10, window_seconds=60)


def with_rate_limit(user_id: str = "default") -> Callable:
    """Decorator to add rate limiting to a tool."""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            if not rate_limiter.check_rate_limit(user_id):
                error_msg = f"Rate limit exceeded. Max {rate_limiter.max_calls} calls per {rate_limiter.window_seconds} seconds."
                print(f"[RATE LIMIT] {error_msg}")
                raise ToolException(error_msg)
            return func(*args, **kwargs)
        return wrapper
    return decorator


# Input validation with Pydantic
class QueryRequest(BaseModel):
    """Validated input for server-side query tool."""
    query: str = Field(..., min_length=1, max_length=1000)
    max_results: int = Field(5, ge=1, le=50)
    include_docs: bool = True


@tool
@with_rate_limit()
def server_search(query: str, max_results: int = 5) -> str:
    """Server-side search with rate limiting and input validation.

    Args:
        query: Search query (1-1000 characters)
        max_results: Maximum results to return (1-50)
    """
    print(f"\n[TOOL EXECUTION] server_search called with query={query}, max_results={max_results}")

    # Server-side input validation beyond Pydantic
    try:
        # Validate using Pydantic
        request = QueryRequest(query=query, max_results=max_results)
    except ValidationError as e:
        error_msg = f"Input validation failed: {str(e)}"
        print(f"[VALIDATION ERROR] {error_msg}")
        raise ToolException(error_msg)

    # Simulate server-side processing with timeout handling
    start_time = time.time()
    try:
        # Simulate API call with timeout
        time.sleep(0.1)  # Simulate network latency

        result = (
            f"Search completed for query: '{request.query}'\n"
            f"Found {request.max_results} results:\n"
        )
        for i in range(request.max_results):
            result += f"{i+1}. Result {i+1} for {request.query}\n"

        elapsed = time.time() - start_time
        print(f"[TOOL SUCCESS] Completed in {elapsed:.3f}s")
        return result

    except TimeoutError:
        error_msg = f"Search timed out after 30 seconds"
        print(f"[TIMEOUT] {error_msg}")
        raise ToolException(error_msg)


# Tool with authentication check
class DatabaseQuery(BaseModel):
    """Database query request."""
    table: str = Field(..., pattern=r'^[a-z_]+$')
    limit: int = Field(100, ge=1, le=1000)


def check_authentication(api_key: str) -> bool:
    """Check if API key is valid."""
    expected_key = os.getenv("TOOL_API_KEY")
    if not expected_key:
        # If no env var set, accept any non-empty key for demo
        return len(api_key) > 10
    return api_key == expected_key


@tool
def query_database(sql_query: str, api_key: str, config: Optional[dict] = None) -> str:
    """Query the database with authentication.

    Args:
        sql_query: The SQL SELECT query to execute
        api_key: API key for authentication
        config: Injected configuration for additional context
    """
    print(f"\n[TOOL EXECUTION] query_database called")
    print(f"   Authenticating with API key: {'*' * len(api_key) if api_key else 'None'}")

    # Authentication check
    if not check_authentication(api_key):
        error_msg = "Authentication failed: Invalid API key"
        print(f"[AUTH ERROR] {error_msg}")
        raise ToolException(error_msg)

    # Add user ID from config for audit logging
    user_id = config.get("user_id", "unknown") if config else "unknown"
    print(f"[AUDIT] User {user_id} executing query: {sql_query[:100]}...")

    # Validate query (basic safety check)
    sql_lower = sql_query.lower().strip()
    if not sql_lower.startswith("select"):
        error_msg = "Only SELECT queries are allowed for security"
        print(f"[SECURITY] {error_msg}")
        raise ToolException(error_msg)

    if "drop" in sql_lower or "delete" in sql_lower or "update" in sql_lower:
        error_msg = "Modifying queries (DROP, DELETE, UPDATE) are not allowed"
        print(f"[SECURITY] {error_msg}")
        raise ToolException(error_msg)

    result = f"Executed SELECT query successfully. Returned 42 rows."
    print(f"[TOOL RESULT]: {result}")
    return result


print("\n🔧 Server-side configuration:")
print("   - server_search: With rate limiting and Pydantic validation")
print("   - query_database: With authentication and SQL safety checks")
print("   - Error handling with ToolException for proper error propagation")
print("   - Audit logging for all tool invocations")

# Create agent
agent = create_agent(
    model=get_llm("gpt-4.1"),
    tools=[server_search, query_database],
    middleware=[],
)

print("\n✅ Agent created successfully!")

# Invoke
print("\n🚀 Invoking agent...")
query = "Search for 'machine learning' with 5 results. The rate limiting should allow this."
print(f"\n👤 User: {query}")
print("🤖 LLM is processing... Server-side checks will execute.")
print("-" * 60)

try:
    result = agent.invoke({
        "messages": [HumanMessage(content=query)]
    }, config={"user_id": "user_789", "api_key": os.getenv("TOOL_API_KEY", "demo_key_12345")})

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
print("Server-side tool example completed!")
print("\n💡 Server-side best practices:")
print("   - Always authenticate requests before executing tools")
print("   - Enforce rate limiting per user to prevent abuse")
print("   - Validate all inputs on the server (never trust client)")
print("   - Audit log all tool invocations for compliance")
print("   - Use proper error handling with clear error messages")
print("   - Add timeouts to prevent hanging on external calls")
print("   - Sanitize inputs for security (e.g., SQL safety)")
