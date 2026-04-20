"""
13. Shell Tool Middleware Example

Expose a persistent shell session to agents for command execution.
"""

import os
from langchain.agents import create_agent
from langchain.agents.middleware import (
    ShellToolMiddleware,
    HostExecutionPolicy,
    RedactionRule,
)
from langchain.tools import tool
from langchain.messages import HumanMessage
from llm_config import get_llm

print("=" * 60)
print("Shell Tool Middleware Example")
print("Expose persistent shell session to agents for command execution")
print("=" * 60)


@tool
def web_search(query: str) -> str:
    """Search the web for information."""
    print(f"\n[TOOL EXECUTION] web_search called with query: {query}")
    result = f"Search results for '{query}': LangChain shell middleware enables agent command execution."
    print(f"[TOOL RESULT]: {result}")
    return result


# Get current directory for workspace
current_dir = os.path.abspath(os.path.dirname(__file__))
print(f"\n🔧 Configuration (Host execution):")
print(f"   workspace_root: {current_dir}")
print("   execution_policy: HostExecutionPolicy()")
print("   redaction_rules: [api_key detection]")

# Basic shell tool with host execution + redaction
agent = create_agent(
    model=get_llm("gpt-4.1"),
    tools=[web_search],
    middleware=[
        ShellToolMiddleware(
            workspace_root=current_dir,
            execution_policy=HostExecutionPolicy(),
            redaction_rules=[
                RedactionRule(pii_type="api_key", detector=r"sk-[a-zA-Z0-9]{32}"),
            ],
        ),
    ],
)

print("\n✅ Agent created successfully!")
print("\nThe agent now has a persistent shell tool it can use.")

# Invoke with a query that will list files
print("\n🚀 Invoking agent...")
query = f"List all the Python files in the current directory ({current_dir}) and tell me how many there are."
print(f"\n👤 User: {query}")
print("\n🤖 Agent will execute shell command(s) to answer...")
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
print("Shell Tool middleware example completed!")
print("\n💡 Execution policies:")
print("   - HostExecutionPolicy: Full host access (default, trusted environments)")
print("   - DockerExecutionPolicy: Isolated Docker container (stronger isolation)")
print("   - CodexSandboxExecutionPolicy: Reuses Codex CLI sandbox")
print("\n🔒 Security: Use appropriate isolation based on your deployment.")
print("   Redaction rules can sanitize output before returning to model.")

