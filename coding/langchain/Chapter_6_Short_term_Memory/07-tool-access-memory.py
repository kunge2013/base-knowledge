"""
7. Access Memory from Tools

Tools can read and write to short-term memory (agent state) directly using the `runtime` parameter.
This allows tools to persist intermediate results and access custom state fields.
"""

from typing import Optional
from pydantic import BaseModel
from langchain.tools import tool, ToolRuntime
from langchain.agents import create_agent, AgentState
from langgraph.types import Command
from langchain.messages import ToolMessage
from llm_config import get_llm

print("=" * 60)
print("7. Access Memory from Tools Example")
print("Tools can read/write short-term memory via runtime parameter")
print("=" * 60)


# 1. Define custom state
class CustomState(AgentState):
    user_name: Optional[str]  # Store user name in state


# 2. Define context schema
class CustomContext(BaseModel):
    user_id: str  # User ID from context


# 3. Tool that updates state based on context
@tool
def update_user_info(
    runtime: ToolRuntime[CustomContext, CustomState],
) -> Command:
    """Look up and update user info in short-term memory.

    Use this when you need to get the user's name from database and store it in memory.
    """
    print(f"\n[TOOL EXECUTION] update_user_info called")
    user_id = runtime.context.user_id
    print(f"   Got user_id from context: {user_id}")

    # Lookup (simulated)
    name = "John Smith" if user_id == "user_123" else "Unknown user"

    print(f"   Looked up name: {name}")
    print(f"   Updating state...")

    # Return command updates the state
    return Command(update={
        "user_name": name,
        "messages": [
            ToolMessage(
                f"Successfully looked up user information: name is {name}",
                tool_call_id=runtime.tool_call_id
            )
        ]
    })


@tool
def greet(
    runtime: ToolRuntime[CustomContext, CustomState],
) -> str | Command:
    """Greet the user once you know their name from memory.

    Use this after update_user_info to greet the user by name.
    """
    print(f"\n[TOOL EXECUTION] greet called")
    user_name = runtime.state.get("user_name", None)
    print(f"   Read user_name from state: {user_name}")

    if user_name is None:
        print("   user_name not found in state - need to look up first")
        return Command(update={
            "messages": [
                ToolMessage(
                    "Please call the 'update_user_info' tool to look up the user's name first.",
                    tool_call_id=runtime.tool_call_id
                )
            ]
        })

    result = f"Hello {user_name}! It's nice to meet you."
    print(f"[TOOL RESULT]: {result}")
    return result


print("\n🔧 Configuration:")
print("   - CustomState extends AgentState with user_name field")
print("   - CustomContext provides context from config")
print("   - ToolRuntime[Context, State] gives typed access")
print("   - update_user_info reads from context, writes to state")
print("   - greet reads user_name from state and greets")

# Create agent
agent = create_agent(
    model=get_llm("gpt-4.1"),
    tools=[update_user_info, greet],
    state_schema=CustomState,
    context_schema=CustomContext,
)

print("\n✅ Agent created with memory access from tools!")

# Invoke
print("\n🚀 Invoking agent...")
print(f"   User request: greet the user")
print(f"   context: CustomContext(user_id='user_123')")
print("-" * 60)

try:
    result = agent.invoke(
        {
            "messages": [{"role": "user", "content": "greet the user"}],
            "user_name": None,
        },
        context=CustomContext(user_id="user_123"),
    )

    print("-" * 60)
    print("\n📄 Final State:")
    print(f"   user_name in state: {result.get('user_name')}")
    print(f"\n📄 Final Response:")
    if 'messages' in result:
        last_msg = result['messages'][-1]
        if hasattr(last_msg, 'content'):
            print(last_msg.content)

except Exception as e:
    print("-" * 60)
    print(f"\n❌ Error: {type(e).__name__}: {e}")
    print("\nThis example requires a valid OpenAI API key configured in .env")

print("\n" + "=" * 60)
print("Tool access memory example completed!")
print("\n💡 Key patterns:")
print("   - `runtime: ToolRuntime` is automatically injected")
print("   - `runtime.context`: Access immutable context from config")
print("   - `runtime.state`: Read current short-term state")
print("   - Return `Command(update=...)` to modify state from tool")
print("   - Type parameterize: ToolRuntime[ContextType, StateType]")
