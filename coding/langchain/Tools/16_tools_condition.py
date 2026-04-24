"""16_tools_condition.py
Use tools_condition for conditional routing in LangGraph.
"""

from langgraph.prebuilt import ToolNode, tools_condition
from langchain.tools import tool
from langgraph.graph import StateGraph, MessagesState, START, END

@tool
def search(query: str) -> str:
    """Search for information."""
    return f"Results for: {query}"

@tool
def calculator(expression: str) -> str:
    """Evaluate a math expression."""
    try:
        return str(eval(expression))
    except:
        return "Invalid expression"

# Define a function to call the LLM
def call_llm(state: MessagesState):
    """Call the LLM with current messages."""
    from llm_config import default_llm
    model_with_tools = default_llm.bind_tools([search, calculator])
    return {"messages": [model_with_tools.invoke(state["messages"]))}

[...]

# Create graph with conditional routing
builder = StateGraph(MessagesState)
builder.add_node("llm", call_llm)
builder.add_node("tools", ToolNode([search, calculator]))

builder.add_edge(START, "llm")
builder.add_conditional_edges("llm", tools_condition)  # Routes to "tools" or END
builder.add_edge("tools", "llm")

graph = builder.compile()

print("Graph created with tools_condition for routing")
print("Routes to 'tools' when LLM makes tool calls, otherwise to END")
