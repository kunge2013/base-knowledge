"""14_tool_return_command.py
Tool that returns a Command to update state.
"""

from langchain.messages import ToolMessage
from langchain.tools import ToolRuntime, tool
from langgraph.types import Command

@tool
def set_language(language: str, runtime: ToolRuntime) -> Command:
    """Set preferred response language."""
    return Command(
        update={
                "preferred_language": language,
                "messages": [
                    ToolMessage(
                        content=f"Language set to {language}.",
                        tool_call_id=runtime.tool_call_id,
                    )
                ],
            }
    )

print("Tool that returns Command to update agent state")
print("Behavior:")
print("- Command updates state using 'update'")
print("- Updated state is available to subsequent steps")
print("- Use reducers for fields that may be updated by parallel tool calls")
