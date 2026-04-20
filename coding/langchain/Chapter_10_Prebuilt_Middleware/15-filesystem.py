"""
15. Filesystem Middleware Example

Provides four tools for interacting with both short-term and long-term memory:
- ls: List the files in the filesystem
- read_file: Read an entire file or a certain number of lines from a file
- write_file: Write a new file to the filesystem
- edit_file: Edit an existing file in the filesystem
"""

import os
from langchain.agents import create_agent
from deepagents.middleware.filesystem import FilesystemMiddleware
from deepagents.backends import CompositeBackend, StateBackend, StoreBackend
from langgraph.store.memory import InMemoryStore
from langchain.messages import HumanMessage
from llm_config import get_llm

print("=" * 60)
print("Filesystem Middleware Example")
print("Provides filesystem tools for context storage and long-term memory")
print("=" * 60)

# Get current directory
current_dir = os.path.abspath(os.path.dirname(__file__))
notes_path = os.path.join(current_dir, "notes.txt")

print("\n🔧 Configuration:")
print("   Backend: CompositeBackend with persistent storage for /memories/")
print("   StateBackend: Ephemeral storage in graph state (default)")
print("   StoreBackend: Persistent storage across threads for /memories/")
print(f"   Working from directory: {current_dir}")

# Configure persistent storage
store = InMemoryStore()

agent = create_agent(
    model=get_llm("claude-sonnet-4-6"),
    store=store,
    middleware=[
        FilesystemMiddleware(
            backend=CompositeBackend(
                default=StateBackend(),
                routes={"/memories/": StoreBackend(store)}
            ),
            system_prompt="Use the filesystem tools to manage files and store notes.",
            custom_tool_descriptions={
                "ls": "List files in the current directory.",
                "read_file": "Read the contents of a text file.",
                "write_file": "Write content to a new file.",
                "edit_file": "Edit an existing file by replacing text."
            }
        ),
    ],
)

print("\n✅ Agent created successfully with 4 filesystem tools:")
print("   - ls: List the files in the filesystem")
print("   - read_file: Read an entire file or specific lines")
print("   - write_file: Write a new file to the filesystem")
print("   - edit_file: Edit an existing file in the filesystem")

# Invoke with a task that uses filesystem tools
print("\n🚀 Invoking agent...")
query = f"""List the Python files in the current directory, then write a summary
of what you found to a file called {os.path.basename(notes_path)}."""
print(f"\n👤 User: {query}")
print("\n🤖 Agent will use filesystem tools to complete the task...")
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
print("Filesystem middleware example completed!")
print("\n💡 Storage routing:")
print("   - Paths starting with /memories/ → persisted to StoreBackend")
print("   - All other paths → ephemeral in StateBackend (gone after thread)")
print("   - This gives you flexible short-term vs long-term memory for agents")

