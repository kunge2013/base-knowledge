"""02_custom_tool_properties.py
Customize tool name and description.
"""

from langchain.tools import tool

# Custom tool name
@tool("web_search")  # Custom name
def search(query: str) -> str:
    """Search web for information."""
    return f"Results for: {query}"

print(f"Tool name: {search.name}")
print(f"Expected name: web_search")
print()

# Custom tool description
@tool("calculator", description="Performs arithmetic calculations. Use this for any math problems.")
def calc(expression: str) -> str:
    """Evaluate mathematical expressions."""
    return str(eval(expression))

print(f"Tool name: {calc.name}")
print(f"Tool description: {calc.description}")

# Use the calculator
result = calc.invoke({"expression": "2 + 2 * 3"})
print(f"\nCalculation result: {result}")
