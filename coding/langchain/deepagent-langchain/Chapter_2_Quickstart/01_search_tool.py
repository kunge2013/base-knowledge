"""
01_search_tool.py - Creating a Search Tool for Deep Agents

This module demonstrates how to create a custom search tool using Tavily API.
The search tool can be used by deep agents to conduct internet research.

Key Concepts:
- Tool definition with type hints for automatic schema generation
- Using Literal types for constrained string parameters
- Integrating external APIs (Tavily) as agent tools
"""

import os
from typing import Literal
from dotenv import load_dotenv

load_dotenv()

from tavily import TavilyClient

# Initialize Tavily client with API key from environment
tavily_client = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])


def internet_search(
    query: str,
    max_results: int = 5,
    topic: Literal["general", "news", "finance"] = "general",
    include_raw_content: bool = False,
):
    """
    Run an internet search using Tavily API.

    This function serves as a tool that deep agents can call to gather
    information from the internet. The type hints automatically generate
    a proper schema for the agent to understand the parameters.

    Args:
        query: The search query string
        max_results: Maximum number of search results to return (default: 5)
        topic: Category of search - 'general', 'news', or 'finance' (default: 'general')
        include_raw_content: Whether to include full page content in results (default: False)

    Returns:
        dict: Search results from Tavily API containing:
            - query: The original search query
            - results: List of search result dictionaries with:
                - title: Page title
                - url: Page URL
                - content: Snippet from the page
                - score: Relevance score
            - raw_content: Full page content if requested

    Example:
        >>> results = internet_search("What is LangChain?", max_results=3)
        >>> for result in results['results']:
        ...     print(f"Title: {result['title']}")
        ...     print(f"URL: {result['url']}")
    """
    return tavily_client.search(
        query,
        max_results=max_results,
        include_raw_content=include_raw_content,
        topic=topic,
    )


# Example usage - standalone test
if __name__ == "__main__":
    # Test the search tool
    query = "What is LangChain framework?"
    print(f"Searching for: {query}")
    print("-" * 50)

    results = internet_search(query, max_results=3)

    print(f"Found {len(results.get('results', []))} results:\n")

    for i, result in enumerate(results.get("results", []), 1):
        print(f"{i}. {result.get('title', 'No title')}")
        print(f"   URL: {result.get('url', 'No URL')}")
        print(f"   Content: {result.get('content', 'No content')[:100]}...")
        print()
