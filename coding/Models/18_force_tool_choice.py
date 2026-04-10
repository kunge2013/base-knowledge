"""18_force_tool_choice.py
Example: Forcing the model to use any tool from a list.
"""

from langchain.tools import tool
from llm_config import default_llm


@tool
def search_web(query: str) -> str:
    """Search the web for information."""
    return f"Results for: {query}"


# Force the model to use any tool from the bound list
model_with_tools = default_llm.bind_tools([search_web], tool_choice="any")

# Model will output a tool call regardless of prompt
response = model_with_tools.invoke("Hello!")
print(response.tool_calls)
