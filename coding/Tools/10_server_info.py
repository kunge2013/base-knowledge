"""10_server_info.py
Access LangGraph Server information from tools.
"""

from langchain.tools import tool, ToolRuntime

@tool
def get_assistant_scoped_data(runtime: ToolRuntime) -> str:
    """Fetch data scoped to current assistant."""
    server = runtime.server_info
    if server is not None:
        print(f"Assistant: {server.assistant_id}, Graph: {server.graph_id}")
        if server.user is not None:
            print(f"User: {server.user.identity}")
    return "done"

print("This tool accesses LangGraph Server metadata")
print("Server info is None when not running on LangGraph Server")
print("Requires langgraph>=1.1.5 or deepagents>=0.5.0")
