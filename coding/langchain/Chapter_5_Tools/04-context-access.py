"""
4. Access Context (State, Context, Store)

Tools can access runtime context:
- config: Read-only configuration and thread context
- runtime: Access to current state, long-term store, streaming
"""

from typing import Optional, Any
from langchain.tools import tool
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from langgraph.store.base import BaseStore
from llm_config import get_llm

print("=" * 60)
print("4. Context Access Example")
print("Access state, context, store from within tools")
print("=" * 60)


# Access the configuration context (immutable)
# `config` is a reserved parameter name that gets injected
@tool
def get_user_info(config: Optional[dict] = None) -> str:
    """Get information about the current user from configuration.

    The `config` parameter is automatically injected by the system.
    """
    print(f"\n[TOOL EXECUTION] get_user_info called")
    print(f"   Injected config: {config is not None}")

    if config and "user_id" in config:
        user_id = config["user_id"]
        result = f"Current user ID is: {user_id}"
    else:
        result = "No user ID configured in this session."

    print(f"[TOOL RESULT]: {result}")
    return result


# Access state from tool (read-only current state)
# `runtime.state` gives you access to the current graph state
@tool
def read_conversation_history(runtime: Any, config: Optional[dict] = None) -> str:
    """Read the conversation history from the current runtime state.

    Uses the injected `runtime` parameter to access current state.
    """
    print(f"\n[TOOL EXECUTION] read_conversation_history called")
    print(f"   Runtime available: {runtime is not None}")

    # Access current state
    current_state = runtime.state
    print(f"   Current state has keys: {list(current_state.keys()) if current_state else 'None'}")

    if current_state and "messages" in current_state:
        messages = current_state["messages"]
        count = len(messages)
        result = f"There are {count} messages in the conversation history.\n"
        if count > 0:
            last_message = messages[-1]
            result += f"The last message was from {last_message.type}: {last_message.content[:100]}..."
    else:
        result = "No conversation history found in state."

    print(f"[TOOL RESULT]: {result}")
    return result


# Access long-term store to read/write memories
@tool
def remember(key: str, value: str, runtime: Any) -> str:
    """Store a key-value memory in the long-term store.

    Args:
        key: The memory key to store under
        value: The value to remember
        runtime: Runtime context providing access to store
    """
    print(f"\n[TOOL EXECUTION] remember called with key={key}, value={value}")

    store: BaseStore = runtime.store
    namespace = ("memories",)

    # Store the memory
    store.put(namespace, key, {"value": value})
    result = f"Successfully stored memory: {key} = {value}"

    print(f"[TOOL RESULT]: {result}")
    return result


@tool
def recall(key: str, runtime: Any) -> str:
    """Recall a previously stored memory from the long-term store.

    Args:
        key: The memory key to recall
        runtime: Runtime context providing access to store
    """
    print(f"\n[TOOL EXECUTION] recall called with key={key}")

    store: BaseStore = runtime.store
    namespace = ("memories",)

    item = store.get(namespace, key)
    if item:
        value = item.value["value"]
        result = f"Recalled memory: {key} = {value}"
    else:
        result = f"No memory found for key: {key}"

    print(f"[TOOL RESULT]: {result}")
    return result


print("\n🔧 Configuration:")
print("   - get_user_info: Accesses injected config parameter")
print("   - read_conversation_history: Accesses runtime.state")
print("   - remember/recall: Accesses runtime.store for long-term memory")
print("   - `config` and `runtime` are reserved parameter names")

# Create agent
from langgraph.store.memory import InMemoryStore
store = InMemoryStore()

agent = create_agent(
    model=get_llm("gpt-4.1"),
    tools=[get_user_info, read_conversation_history, remember, recall],
    store=store,
    middleware=[],
)

print("\n✅ Agent created successfully with InMemoryStore!")

# Invoke
print("\n🚀 Invoking agent...")
query = """
Store the fact that my favorite color is blue in memory.
Then recall that memory. Also check how many messages are in conversation history.
"""
print(f"\n👤 User: {query.strip()}")
print("🤖 LLM is processing... Tools will access context.")
print("-" * 60)

try:
    result = agent.invoke({
        "messages": [HumanMessage(content=query)],
    }, config={"user_id": "user_12345"})

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
except Exception as e:
    print("-" * 60)
    print(f"\n❌ Error invoking LLM: {type(e).__name__}: {e}")
    print("\nThis example requires a valid OpenAI API key configured in .env")

print("\n" + "=" * 60)
print("Context access example completed!")
print("\n💡 Context types:")
print("   - config: Immutable thread configuration (user_id, etc.)")
print("   - runtime.state: Current graph state (read-only)")
print("   - runtime.store: Long-term key-value storage across threads")
print("   - runtime.stream: Streaming token output to the client")
print("   - Parameters named `config` and `runtime` are automatically injected")
