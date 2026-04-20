"""
12. Context Editing Middleware Example

Manage conversation context by clearing older tool call outputs when token
limits are reached, while preserving recent results.
"""

from langchain.agents import create_agent
from langchain.agents.middleware import ContextEditingMiddleware, ClearToolUsesEdit
from langchain.tools import tool
from langchain.messages import HumanMessage
from llm_config import get_llm

print("=" * 60)
print("Context Editing Middleware Example")
print("Clear older tool outputs when token limits are reached, preserve recent")
print("=" * 60)


@tool
def web_search(query: str) -> str:
    """Search the web for information."""
    print(f"\n[TOOL EXECUTION] web_search called with query: {query}")
    result = f"Search results for '{query}': Found multiple relevant documents discussing LangChain middleware."
    print(f"[TOOL RESULT]: {result[:80]}...")
    return result


@tool
def calculator(expression: str) -> str:
    """Calculate a mathematical expression."""
    print(f"\n[TOOL EXECUTION] calculator called with: {expression}")
    try:
        result = str(eval(expression))
        print(f"[TOOL RESULT]: {result}")
        return result
    except Exception as e:
        return f"Error: {e}"


@tool
def query_database(sql: str) -> str:
    """Query a database with SQL."""
    print(f"\n[TOOL EXECUTION] query_database called with: {sql[:60]}...")
    result = "Returned 15 rows matching your query with various aggregate statistics."
    print(f"[TOOL RESULT]: {result}")
    return result


tools = [web_search, calculator, query_database]

print("\n🔧 Configuration:")
print("   Strategy: ClearToolUsesEdit")
print("   trigger: 2000 tokens (clear when context exceeds this)")
print("   keep: 3 (keep the 3 most recent tool results)")
print("   clear_tool_inputs: False (keep tool call arguments)")
print("   placeholder: '[cleared]' (text for cleared outputs)")

agent = create_agent(
    model=get_llm("gpt-4.1"),
    tools=tools,
    middleware=[
        ContextEditingMiddleware(
            edits=[
                ClearToolUsesEdit(
                    trigger=2000,
                    keep=3,
                    clear_tool_inputs=False,
                    exclude_tools=[],
                    placeholder="[cleared]",
                ),
            ],
        ),
    ],
)

print("\n✅ Agent created successfully!")

# Invoke with a query that will use multiple tools
print("\n🚀 Invoking agent...")
query = """Search for information about LangChain middleware, then calculate the sum of 15 and 27,
then query the database for recent entries about middleware best practices."""
print(f"\n👤 User: {query}")
print("\n🤖 Agent is executing multiple tool calls...")
print("When token count exceeds 2000, older tool outputs will be cleared.")
print("-" * 60)

result = agent.invoke({
    "messages": [HumanMessage(content=query)]
})

print("-" * 60)
print("\n📄 Final Response:")
if isinstance(result, dict) and 'messages' in result:
    last_msg = result['messages'][-1]
    if hasattr(last_msg, 'content'):
        print(last_msg.content)
    else:
        print(last_msg)
else:
    print(result)

print("\n" + "=" * 60)
print("Context Editing middleware example completed!")
print("\n💡 How it works:")
print("   1. Monitor token count in conversation")
print("   2. When threshold reached, clear older tool outputs")
print("   3. Keep most recent N tool results")
print("   4. Optionally preserve tool call arguments for context")
print("\nThis helps keep context windows manageable in long conversations")
print("with many tool calls by removing older outputs that are no longer needed.")

