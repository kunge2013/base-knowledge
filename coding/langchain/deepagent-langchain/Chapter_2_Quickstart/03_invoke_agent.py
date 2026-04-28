"""
03_invoke_agent.py - Running and Streaming a Deep Agent

This module demonstrates how to invoke a deep agent and stream its output.
It shows both basic invocation and streaming for real-time updates.

Key Concepts:
- Basic agent invocation with invoke()
- Streaming output for real-time updates
- Accessing agent responses from the result
- Observing tool calls and subagent work
"""

from rich.console import Console
from rich.markdown import Markdown
from deepagents import create_deep_agent

# Reuse the search tool and instructions from 02_create_agent.py
import os
from typing import Literal
from dotenv import load_dotenv

load_dotenv()

from tavily import TavilyClient

tavily_client = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])


def internet_search(
    query: str,
    max_results: int = 5,
    topic: Literal["general", "news", "finance"] = "general",
    include_raw_content: bool = False,
):
    """Run an internet search using Tavily API."""
    return tavily_client.search(
        query,
        max_results=max_results,
        include_raw_content=include_raw_content,
        topic=topic,
    )


research_instructions = """You are an expert researcher. Your job is to conduct thorough research and then write a polished report.

You have access to an internet search tool as your primary means of gathering information.

## `internet_search`

Use this to run an internet search for a given query. You can specify the max number of results to return, the topic, and whether raw content should be included.
"""

# Create the agent
agent = create_deep_agent(
    model="google_genai:gemini-3.1-pro-preview",
    tools=[internet_search],
    system_prompt=research_instructions,
)


# =============================================================================
# Method 1: Basic Invocation (Non-streaming)
# =============================================================================

def invoke_agent_basic():
    """Run the agent and get final result."""
    console = Console()

    console.print("\n[bold blue]=== Basic Agent Invocation ===[/bold blue]\n")
    console.print("[yellow]Question: What is LangChain?[/yellow]\n")

    console.print("[dim]Running agent... (this may take a moment)[/dim]\n")

    result = agent.invoke({"messages": [{"role": "user", "content": "What is LangChain?"}]})

    # Print the agent's response
    console.print("\n[bold green]=== Agent Response ===[/bold green]\n")

    response_content = result["messages"][-1].content
    console.print(Markdown(response_content))

    return result


# =============================================================================
# Method 2: Streaming Invocation (Real-time Updates)
# =============================================================================

def invoke_agent_streaming():
    """Stream the agent output for real-time updates."""
    console = Console()

    console.print("\n[bold blue]=== Streaming Agent Invocation ===[/bold blue]\n")
    console.print("[yellow]Question: What is LangGraph?[/yellow]\n")

    console.print("[dim]Streaming agent response...[/dim]\n")
    console.print("[bold green]Response:[/bold green]\n")

    # Stream the agent's response
    for chunk in agent.stream({"messages": [{"role": "user", "content": "What is LangGraph?"}]}):
        # Check if there's a message in the chunk
        if "messages" in chunk and chunk["messages"]:
            message = chunk["messages"][-1]
            if hasattr(message, 'content') and message.content:
                console.print(message.content, end="")

    console.print("\n\n[dim]Streaming complete![/dim]")


# =============================================================================
# Method 3: Streaming with Event Details (Debug Mode)
# =============================================================================

def invoke_agent_with_events():
    """Stream with detailed events for debugging agent behavior."""
    console = Console()

    console.print("\n[bold blue]=== Agent Invocation with Events ===[/bold blue]\n")
    console.print("[yellow]Question: What is the difference between LangChain and LangGraph?[/yellow]\n")

    console.print("[dim]Observing agent events...[/dim]\n")

    # Use astream_events for detailed event streaming
    import asyncio

    async def stream_events():
        async for event in agent.astream_events(
            {"messages": [{"role": "user", "content": "What is the difference between LangChain and LangGraph?"}]},
            version="v2"
        ):
            event_type = event.get("event")
            event_name = event.get("name", "")

            # Log tool calls
            if event_type == "on_tool_start":
                console.print(f"\n[bold cyan]🔧 Tool Called:[/bold cyan] {event_name}")

            elif event_type == "on_tool_end":
                console.print(f"[bold green]✓ Tool Completed:[/bold green] {event_name}")

            # Log subagent events
            elif "subagent" in event_name.lower():
                console.print(f"[bold magenta]🤖 Subagent Event:[/bold magenta] {event_name}")

            # Log chat model events
            elif event_type == "on_chat_model_stream":
                content = event.get("data", {}).get("chunk", "")
                if content:
                    console.print(content, end="")

    console.print("\n[dim]Running async event stream...[/dim]\n")
    asyncio.run(stream_events())


# =============================================================================
# Main Execution
# =============================================================================

if __name__ == "__main__":
    console = Console()

    console.print("\n" + "=" * 60)
    console.print("[bold]Deep Agents Quickstart - Agent Invocation Demo[/bold]")
    console.print("=" * 60)

    console.print("\nSelect invocation method:")
    console.print("1. Basic invocation (simple, non-streaming)")
    console.print("2. Streaming invocation (real-time text output)")
    console.print("3. Event streaming (debug mode with tool calls)")
    console.print("4. Run all methods")

    choice = input("\nEnter choice (1-4, default: 1): ").strip() or "1"

    if choice == "1":
        invoke_agent_basic()
    elif choice == "2":
        invoke_agent_streaming()
    elif choice == "3":
        invoke_agent_with_events()
    elif choice == "4":
        console.print("\n\n[bold]--- Running All Methods ---[/bold]\n")
        invoke_agent_basic()
        console.print("\n\n")
        invoke_agent_streaming()
        console.print("\n\n")
        invoke_agent_with_events()
    else:
        console.print("[red]Invalid choice[/red]")
