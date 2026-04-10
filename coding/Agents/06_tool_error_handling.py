"""06_tool_error_handling.py
Example: Custom tool error handling with middleware.
"""

from langchain.agents import create_agent
from langchain.agents.middleware import wrap_tool_call
from langchain_core.messages import ToolMessage
from langchain.tools import tool
from llm_config import default_llm


@tool
def divide(a: float, b: float) -> float:
    """Divide two numbers."""
    return a / b


@wrap_tool_call
def handle_tool_errors(request, handler):
    """Handle tool execution errors with custom messages."""
    try:
        return handler(request)
    except Exception as e:
        # Return a custom error message to the model
        return ToolMessage(
            content=f"Tool error: Please check your input and try again. ({str(e)})",
            tool_call_id=request.tool_call["id"]
        )


agent = create_agent(
    model=default_llm,
    tools=[divide],
    middleware=[handle_tool_errors]
)
