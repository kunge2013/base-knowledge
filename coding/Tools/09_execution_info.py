"""09_execution_info.py
Access execution context from tools.
"""

from langchain.tools import tool, ToolRuntime

@tool
def log_execution_context(runtime: ToolRuntime) -> str:
    """Log execution identity information."""
    info = runtime.execution_info
    print(f"Thread: {info.thread_id}, Run: {info.run_id}")
    print(f"Attempt: {info.node_attempt}")
    return "done"

print("This tool logs execution information")
print("Requires langgraph>=1.1.5 or deepagents>=0.5.0")
