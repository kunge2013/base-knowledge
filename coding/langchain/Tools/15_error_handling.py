"""15_error_handling.py
Configure error handling in ToolNode.
"""

from langgraph.prebuilt import ToolNode
from langchain.tools import tool

@tool
def risky_tool(input_str: str) -> str:
    """A tool that might fail."""
    if "error" in input_str.lower():
        raise ValueError("Simulated error")
    return f"Processed: {input_str}"

# Default: catch invocation errors, re-raise execution errors
tool_node_default = ToolNode([risky_tool])

# Catch all errors and return error message to LLM
tool_node_catch_all = ToolNode([risky_tool], handle_tool_errors=True)

# Custom error message
tool_node_custom_msg = ToolNode(
    [risky_tool],
    handle_tool_errors="Something went wrong, please try again."
)

# Custom error handler
def handle_error(e: ValueError) -> str:
    return f"Invalid input: {e}"

tool_node_custom_handler = ToolNode([risky_tool], handle_tool_errors=handle_error)

# Only catch specific exception types
tool_node_specific = ToolNode([risky_tool], handle_tool_errors=(ValueError, TypeError))

print("ToolNode with different error handling strategies created")
