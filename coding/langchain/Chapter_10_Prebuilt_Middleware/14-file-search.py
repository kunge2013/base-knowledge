"""
14. File Search Middleware Example

Provide Glob and Grep search tools over a filesystem for code exploration.
"""

import os
from langchain.agents import create_agent
from langchain.agents.middleware import FilesystemFileSearchMiddleware
from langchain.messages import HumanMessage
from llm_config import get_llm

print("=" * 60)
print("File Search Middleware Example")
print("Provides Glob and Grep search tools for code exploration")
print("=" * 60)

# Get project root directory
current_dir = os.path.abspath(os.path.dirname(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
print(f"\n🔧 Configuration:")
print(f"   root_path: {project_root}")
print("   use_ripgrep: True (use ripgrep if available)")
print("   max_file_size_mb: 10 (skip files larger than this)")

agent = create_agent(
    model=get_llm("gpt-4.1"),
    tools=[],
    middleware=[
        FilesystemFileSearchMiddleware(
            root_path=project_root,
            use_ripgrep=True,
            max_file_size_mb=10,
        ),
    ],
)

print("\n✅ Agent created successfully!")
print("\nTwo tools added:")
print("   - glob_search: Fast file pattern matching")
print("   - grep_search: Content search with regex")

# Invoke with a search query
print("\n🚀 Invoking agent...")
query = "Find all Python files in this project that contain the word 'middleware' and tell me how many you found."
print(f"\n👤 User: {query}")
print("\n🤖 Agent will use the search tools...")
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
print("File Search middleware example completed!")
print("\n💡 Capabilities:")
print("   - Glob pattern matching: **/*.py, src/**/*.ts, etc.")
print("   - Regex content search with filtering")
print("   - Skips large files (> max_file_size_mb) to control token usage")
print("   - Uses ripgrep for faster searching if available")

