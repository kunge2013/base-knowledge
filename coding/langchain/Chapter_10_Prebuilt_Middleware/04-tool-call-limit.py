"""
4. Tool Call Limit Middleware Example

Control agent execution by limiting the number of tool calls, either globally
across all tools or for specific tools.
"""

from langchain.agents import create_agent
from langchain.agents.middleware import ToolCallLimitMiddleware
from langchain.tools import tool
from langchain.messages import HumanMessage
from llm_config import get_llm
from langgraph.checkpoint.memory import InMemorySaver

print("=" * 60)
print("Tool Call Limit Middleware Example")
print("Control tool execution by limiting call counts globally or per tool")
print("=" * 60)


@tool
def web_search(query: str) -> str:
    """Search the web for information about a query."""
    print(f"\n[TOOL EXECUTION] web_search called with query: {query}")
    result = f"Search results for '{query}': This is mock search result data from the web search API."
    print(f"[TOOL RESULT]: {result}")
    return result


@tool
def query_database(sql: str) -> str:
    """Query the database with a SQL statement."""
    print(f"\n[TOOL EXECUTION] query_database called with sql: {sql[:50]}...")
    result = "Found 3 rows matching your query: [{'id': 1, 'name': 'example'}, {'id': 2, 'name': 'test'}, {'id': 3, 'name': 'sample'}]"
    print(f"[TOOL RESULT]: {result}")
    return result


@tool
def scrape_webpage(url: str) -> str:
    """Scrape content from a webpage."""
    print(f"\n[TOOL EXECUTION] scrape_webpage called with url: {url}")
    result = f"Scraped content from {url}: HTML content with 2500 words extracted."
    print(f"[TOOL RESULT]: {result}")
    return result


print("\n🔧 Configuration with multiple limiters:")
print("   1. Global: thread_limit=20, run_limit=10 (all tools)")
print("   2. search: thread_limit=5, run_limit=3 (web_search specific)")
print("   3. query_database: thread_limit=10")
print("   4. scrape_webpage: run_limit=2, exit_behavior=error (strict)")
print("   checkpointer: InMemorySaver (required for thread-level limiting)")

# Multiple limiters example
global_limiter = ToolCallLimitMiddleware(thread_limit=20, run_limit=10)
search_limiter = ToolCallLimitMiddleware(tool_name="web_search", thread_limit=5, run_limit=3)
database_limiter = ToolCallLimitMiddleware(tool_name="query_database", thread_limit=10)
strict_limiter = ToolCallLimitMiddleware(tool_name="scrape_webpage", run_limit=2, exit_behavior="error")

checkpointer = InMemorySaver()

agent = create_agent(
    model=get_llm("gpt-4.1"),
    tools=[web_search, query_database, scrape_webpage],
    checkpointer=checkpointer,
    middleware=[global_limiter, search_limiter, database_limiter, strict_limiter],
)

print("\n✅ Agent created successfully with multiple middleware!")

# Invoke with a query
print("\n🚀 Invoking agent with a query to LLM...")
query = "Search for recent information about LangChain middleware and summarize what you find."
print(f"\n👤 User: {query}")
print("\n🤖 LLM is generating response...")
print("-" * 60)

# Configure thread ID
config = {"configurable": {"thread_id": "thread-1"}}

result = agent.invoke(
    {"messages": [HumanMessage(content=query)]},
    config=config
)

print("-" * 60)
print("\n📄 Final agent response:")
if isinstance(result, dict) and 'messages' in result:
    last_msg = result['messages'][-1]
    if hasattr(last_msg, 'content'):
        print(last_msg.content)
    else:
        print(last_msg)
else:
    print(result)

print("\n" + "=" * 60)
print("Tool Call Limit middleware example completed!")
print("\n💡 Exit behaviors when limit reached:")
print("   - continue: Block exceeded calls, let agent decide what to do")
print("   - error: Raise exception immediately stopping execution")
print("   - end: Stop execution immediately (single-tool only)")

