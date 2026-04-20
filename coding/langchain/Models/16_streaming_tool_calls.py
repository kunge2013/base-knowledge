"""16_streaming_tool_calls.py
Example: Streaming tool call chunks progressively.
"""

from langchain.tools import tool
from llm_config import default_llm


@tool
def get_weather(location: str) -> str:
    """Get the weather at a location."""
    return f"It's sunny in {location}."


model_with_tools = default_llm.bind_tools([get_weather])

# Stream tool call chunks incrementally
for chunk in model_with_tools.stream(
    "What's the weather in Boston and Tokyo?"
):
    # Tool call chunks arrive progressively
    for tool_chunk in chunk.tool_call_chunks:
        if name := tool_chunk.get("name"):
            print(f"Tool: {name}")
        if id_ := tool_chunk.get("id"):
            print(f"ID: {id_}")
        if args := tool_chunk.get("args"):
            print(f"Args: {args}")

# Output:
# Tool: get_weather
# ID: call_SvMlU1TVIZugrFLckFE2ceRE
# Args: {"lo
# Args: catio
# Args: n": "B
# Args: osto
# Args: n"}
# Tool: get_weather
# ID: call_QMZdy6qInx13oWKE7KhuhOLR
# Args: {"lo
# Args: catio
# Args: n": "T
# Args: oky
# Args: o"}
