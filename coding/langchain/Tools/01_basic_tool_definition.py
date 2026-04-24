"""01_basic_tool_definition.py
Basic tool definition using @tool decorator.
"""

from langchain.tools import tool

@tool
def search_database(query: str, limit: int = 10) -> str:
    """Search customer database for records matching the query.

    Args:
        query: Search terms to look for
        limit: Maximum number of results to return
    """
    return f"Found {limit} results for '{query}'"

print(f"Tool name: {search_database.name}")
print(f"Tool description: {search_database.description}")

# Use the tool
result = search_database.invoke({"query": "premium", "limit": 5})
print(f"Tool result: {result}")
