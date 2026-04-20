"""
5. ToolNode for LangGraph

ToolNode is a prebuilt LangGraph node that handles tool invocation.
It supports parallel execution, error handling, routing, and state injection.
"""

from typing import Literal
from langchain.tools import tool
from langgraph.prebuilt import ToolNode
from langgraph.graph import StateGraph, MessagesState, END
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from llm_config import get_llm

print("=" * 60)
print("5. ToolNode Example for LangGraph")
print("Prebuilt node with parallel execution and error handling")
print("=" * 60)


# Define some tools
@tool
def get_weather(city: str) -> str:
    """Get the current weather for a city."""
    print(f"\n[TOOL EXECUTION] get_weather called for city: {city}")
    result = f"The weather in {city} is 72°F and sunny."
    print(f"[TOOL RESULT]: {result}")
    return result


@tool
def calculate_distance(city1: str, city2: str) -> str:
    """Calculate the distance between two cities in miles."""
    print(f"\n[TOOL EXECUTION] calculate_distance called: {city1} to {city2}")
    # Simulate calculation
    result = f"The distance between {city1} and {city2} is approximately 347 miles."
    print(f"[TOOL RESULT]: {result}")
    return result


# Tool that might fail
@tool
def unreliable_api(query: str) -> str:
    """An API that sometimes fails to demonstrate error handling."""
    print(f"\n[TOOL EXECUTION] unreliable_api called with query: {query}")
    import random
    if random.random() < 0.3:
        error_msg = f"API request failed for query: {query}"
        print(f"[TOOL FAILED]: {error_msg}")
        raise ConnectionError(error_msg)
    result = f"Success! Got response for {query}"
    print(f"[TOOL SUCCESS]: {result}")
    return result


print("\n🔧 Configuration:")
print("   Three tools: get_weather, calculate_distance, unreliable_api")
print("   ToolNode handles parallel tool execution automatically")
print("   Error handling configured to wrap errors as ToolMessages")

# Create ToolNode with error handling
tools = [get_weather, calculate_distance, unreliable_api]
tool_node = ToolNode(
    tools,
    handle_tool_errors=True,  # Wrap errors instead of raising exception
)

# Create the model
llm = get_llm("gpt-4.1")
llm = llm.bind_tools(tools)


# Define the graph
def should_continue(state: MessagesState) -> Literal["tools", END]:
    messages = state['messages']
    last_message = messages[-1]
    # If the LLM made tool calls, continue to ToolNode
    if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
        return "tools"
    # Otherwise we're done
    return END


def call_model(state: MessagesState):
    messages = state['messages']
    response = llm.invoke(messages)
    return {"messages": [response]}


# Build the graph
workflow = StateGraph(MessagesState)
workflow.add_node("agent", call_model)
workflow.add_node("tools", tool_node)
workflow.set_entry_point("agent")
workflow.add_conditional_edges(
    "agent",
    should_continue,
    {
        "tools": "tools",
        END: END,
    }
)
workflow.add_edge("tools", "agent")

# Compile the graph
app = workflow.compile()

print("\n✅ LangGraph with ToolNode compiled successfully!")

# Invoke with a query that needs multiple tools
print("\n🚀 Invoking graph...")
query = "What's the weather in New York and what's the distance from New York to Boston?"
print(f"\n👤 User: {query}")
print("🤖 Graph will call both tools in parallel...")
print("-" * 60)

try:
    # Stream and collect the output
    final_messages = []
    for chunk in app.stream(
        {"messages": [HumanMessage(content=query)]},
        stream_mode="updates"
    ):
        for node, updates in chunk.items():
            if "messages" in updates:
                messages = updates["messages"]
                for msg in messages:
                    if isinstance(msg, ToolMessage):
                        print(f"\n[TOOL OUTPUT] {msg.name}: {msg.content[:100]}...")
                        final_messages.append(msg)
                    elif isinstance(msg, AIMessage) and msg.tool_calls:
                        print(f"\n[LLM] Requested {len(msg.tool_calls)} tool call(s)")
                        for tc in msg.tool_calls:
                            print(f"   - {tc['name']} with args: {tc['args']}")
                    final_messages.append(msg)

    print("\n" + "-" * 60)
    print("\n📄 Final Response from LLM:")
    last_msg = final_messages[-1]
    if isinstance(last_msg, AIMessage) and last_msg.content:
        print(last_msg.content)
except Exception as e:
    print("-" * 60)
    print(f"\n❌ Error invoking graph: {type(e).__name__}: {e}")
    print("\nThis example requires a valid OpenAI API key configured in .env")

print("\n" + "=" * 60)
print("ToolNode example completed!")
print("\n💡 ToolNode features:")
print("   - Automatic parallel execution of multiple tool calls")
print("   - Configurable error handling: raise, return, or fallback")
print("   - Built-in state injection for tools that need context")
print("   - Works with LangGraph routing out of the box")
print("   - Returns ToolMessage objects added to the conversation state")
