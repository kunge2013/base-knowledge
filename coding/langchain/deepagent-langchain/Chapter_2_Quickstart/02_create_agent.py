"""
02_create_agent.py - Creating a Deep Agent with Research Capabilities

This module demonstrates how to create a deep agent using the deepagents library.
The agent is configured with a search tool and system prompt for research tasks.

Key Concepts:
- create_deep_agent function for agent creation
- System prompt design for steering agent behavior
- Tool integration with deep agents
- Model configuration options (string vs instance)
"""

import os
from typing import Literal

from tavily import TavilyClient
from deepagents import create_deep_agent

# =============================================================================
# Step 1: Create the Search Tool
# =============================================================================

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


# =============================================================================
# Step 2: Define System Prompt
# =============================================================================

research_instructions = """You are an expert researcher. Your job is to conduct thorough research and then write a polished report.

You have access to an internet search tool as your primary means of gathering information.

## `internet_search`

Use this to run an internet search for a given query. You can specify the max number of results to return, the topic, and whether raw content should be included.
"""

# =============================================================================
# Step 3: Create the Deep Agent
# =============================================================================

# Option 1: Using model string (provider:model format)
# Recommended for simple setups
agent = create_deep_agent(
    model="google_genai:gemini-3.1-pro-preview",
    tools=[internet_search],
    system_prompt=research_instructions,
)

# Option 2: Using initialized model instance
# Uncomment the following lines to use a model instance instead:
# from langchain_google_genai import ChatGoogleGenerativeAI
# model_instance = ChatGoogleGenerativeAI(
#     model="gemini-2.0-flash",
#     temperature=0.1,
#     max_tokens=1000,
# )
# agent = create_deep_agent(
#     model=model_instance,
#     tools=[internet_search],
#     system_prompt=research_instructions,
# )

# =============================================================================
# Agent Capabilities
# =============================================================================

print("Deep Agent created successfully!")
print("\nThis agent has the following capabilities:")
print("1. Plans its approach using write_todos tool")
print("2. Conducts research by calling internet_search tool")
print("3. Manages context using file system tools (write_file, read_file)")
print("4. Spawns subagents for complex subtasks")
print("5. Synthesizes findings into coherent reports")
print("\nTo run the agent, execute: 03_invoke_agent.py")
