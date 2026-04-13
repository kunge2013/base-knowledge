"""
7. To-do List Middleware Example

Equip agents with task planning and tracking capabilities for complex multi-step tasks.
"""

import os
from langchain.agents import create_agent
from langchain.agents.middleware import TodoListMiddleware
from langchain.tools import tool
from llm_config import get_llm
from langchain.messages import HumanMessage


@tool
def list_files(directory: str) -> str:
    """List all files and directories in the specified directory.

    Args:
        directory: The directory path to list contents from. Use "." for current directory.
    """
    print(f"\n[TOOL EXECUTION] list_files called with directory: {directory}")
    try:
        contents = os.listdir(directory)
        result = f"Contents of {directory}:\n"
        for item in sorted(contents):
            item_path = os.path.join(directory, item)
            if os.path.isdir(item_path):
                result += f"  📁 {item}/\n"
            else:
                size = os.path.getsize(item_path)
                result += f"  📄 {item} ({size} bytes)\n"
        print(f"[TOOL RESULT]:\n{result}")
        return result
    except Exception as e:
        error_msg = f"Error listing directory {directory}: {str(e)}"
        print(f"[TOOL ERROR]: {error_msg}")
        return error_msg


@tool
def read_file(file_path: str) -> str:
    """Read the contents of a text file.

    Args:
        file_path: Path to the file to read.
    """
    print(f"\n[TOOL EXECUTION] read_file called with file_path: {file_path}")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        preview = content[:500] + ("..." if len(content) > 500 else "")
        print(f"[TOOL RESULT] Content preview ({len(content)} chars total):\n{preview}")
        return content
    except Exception as e:
        error_msg = f"Error reading file {file_path}: {str(e)}"
        print(f"[TOOL ERROR]: {error_msg}")
        return error_msg


@tool
def write_file(file_path: str, content: str) -> str:
    """Write content to a text file.

    Args:
        file_path: Path where to write the file.
        content: Content to write to the file.
    """
    print(f"\n[TOOL EXECUTION] write_file called with file_path: {file_path}")
    print(f"[TOOL INPUT] Content length: {len(content)} chars")
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        result = f"Successfully wrote {len(content)} characters to {file_path}"
        print(f"[TOOL RESULT]: {result}")
        return result
    except Exception as e:
        error_msg = f"Error writing file {file_path}: {str(e)}"
        print(f"[TOOL ERROR]: {error_msg}")
        return error_msg


@tool
def run_python_test(file_path: str) -> str:
    """Run a Python test file and return the output.

    Args:
        file_path: Path to the Python test file to run.
    """
    print(f"\n[TOOL EXECUTION] run_python_test called with file_path: {file_path}")
    import subprocess
    import sys
    try:
        result = subprocess.run(
            [sys.executable, file_path],
            capture_output=True,
            text=True,
            timeout=30
        )
        output = f"Exit code: {result.returncode}\n\nSTDOUT:\n{result.stdout}\n\nSTDERR:\n{result.stderr}"
        print(f"[TOOL RESULT]:\n{output}")
        return output
    except Exception as e:
        error_msg = f"Error running test {file_path}: {str(e)}"
        print(f"[TOOL ERROR]: {error_msg}")
        return error_msg


# Create agent with TodoListMiddleware
print("=" * 60)
print("Creating agent with TodoListMiddleware...")
print("Available tools: list_files, read_file, write_file, run_python_test")
print("=" * 60)

agent = create_agent(
    model=get_llm("gpt-4.1"),
    tools=[list_files, read_file, write_file, run_python_test],
    middleware=[TodoListMiddleware()],
)

print("\n✅ Agent created successfully!")
print("\nTodoListMiddleware automatically adds:")
print("  - write_todos tool for task planning")
print("  - system prompt guiding effective task usage")
print("=" * 60)

# Invoke the agent with a complex multi-step task
user_query = """Help me analyze the current directory:
1. First, list all Python files in the current directory
2. Then, read the contents of llm_config.py to see how it's configured
3. Finally, create a summary file named directory_summary.txt with the findings
"""

print(f"\n👤 USER QUERY:\n{user_query}")
print("\n🚀 Invoking agent...")
print("-" * 60)

# Invoke and capture the result
result = agent.invoke({
    "messages": [HumanMessage(content=user_query)]
})

print("-" * 60)
print("\n✅ Agent execution completed!")
print(f"\n📄 FINAL RESPONSE:")
print(result)
print("\n" + "=" * 60)
print("To-do List middleware example completed successfully!")

