"""
2. Human-in-the-loop Middleware Example

Pause agent execution for human approval, editing, or rejection of tool calls before they execute.
"""

from langchain.agents import create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware
from langgraph.checkpoint.memory import InMemorySaver
from langchain.messages import HumanMessage
from llm_config import get_llm
from langchain.tools import tool


@tool
def your_read_email_tool(email_id: str) -> str:
    """Mock function to read an email by its ID."""
    print(f"\n[TOOL EXECUTION] your_read_email_tool called with email_id: {email_id}")
    result = f"Email content for ID: {email_id}\n\nSubject: Monthly Report\nFrom: boss@company.com\nBody: Please review the attached financial report before tomorrow's meeting."
    print(f"[TOOL RESULT]: {result}")
    return result


@tool
def your_send_email_tool(recipient: str, subject: str, body: str) -> str:
    """Mock function to send an email."""
    print(f"\n[TOOL EXECUTION] your_send_email_tool called:")
    print(f"   Recipient: {recipient}")
    print(f"   Subject: {subject}")
    print(f"   Body length: {len(body)}")
    result = f"Email sent to {recipient} with subject '{subject}'"
    print(f"[TOOL RESULT]: {result}")
    return result


print("=" * 60)
print("Human-in-the-loop Middleware Example")
print("Pause for human approval before executing high-risk tool calls")
print("=" * 60)

print("\n🔧 Configuration:")
print("   - send_email: requires human approval (approve/edit/reject)")
print("   - read_email: no approval needed")
print("   - checkpointer: InMemorySaver (required for interrupts)")

checkpointer = InMemorySaver()

agent = create_agent(
    model=get_llm("gpt-4.1"),
    tools=[your_read_email_tool, your_send_email_tool],
    checkpointer=checkpointer,
    middleware=[
        HumanInTheLoopMiddleware(
            interrupt_on={
                "your_send_email_tool": {
                    "allowed_decisions": ["approve", "edit", "reject"],
                },
                "your_read_email_tool": False,
            }
        ),
    ],
)

print("\n✅ Agent created successfully!")

# Invoke with a test query that will use tools
print("\n🚀 Invoking agent with a query to LLM...")
query = """Read email with ID 12345 and then send a reply to jane@company.com with subject "Re: Monthly Report" summarizing the content."""
print(f"\n👤 User: {query}")
print("\n🤖 LLM is generating response...")
print("-" * 60)

# Configure thread ID for checkpoint
config = {"configurable": {"thread_id": "thread-1"}}

result = agent.invoke(
    {"messages": [HumanMessage(content=query)]},
    config=config
)

print("-" * 60)
print("\n📄 Agent execution result:")
if isinstance(result, dict) and 'messages' in result:
    for i, msg in enumerate(result['messages']):
        print(f"\n[{i}] {type(msg).__name__}:")
        if hasattr(msg, 'content') and msg.content:
            print(f"Content: {msg.content[:200]}{'...' if len(msg.content) > 200 else ''}")
        if hasattr(msg, 'tool_calls') and msg.tool_calls:
            print(f"Tool calls: {msg.tool_calls}")
else:
    print(result)

print("\n" + "=" * 60)
print("Human-in-the-loop middleware example completed!")
print("\n💡 Note: Full human-in-the-loop interaction requires the LangGraph")
print("   CLI to handle approval/editing/rejection when interruption occurs.")

