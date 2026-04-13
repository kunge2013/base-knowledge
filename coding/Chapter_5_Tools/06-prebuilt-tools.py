"""
6. Prebuilt Tools

LangChain comes with many prebuilt tools for common use cases.
This example demonstrates how to use several popular prebuilt tools.
"""

from langchain.agents import create_agent
from langchain.messages import HumanMessage
from langchain.tools import tool
# Import common prebuilt tools
from langchain_community.tools import (
    WikipediaQueryRun,
    ArxivQueryRun,
)
from langchain_community.utilities import (
    WikipediaAPIWrapper,
    ArxivAPIWrapper,
)
from llm_config import get_llm

print("=" * 60)
print("6. Prebuilt Tools Example")
print("Using LangChain's built-in tools for common tasks")
print("=" * 60)


# Wikipedia prebuilt tool
print("\n🔧 Setting up Wikipedia tool...")
wikipedia_api = WikipediaAPIWrapper(top_k_results=3, doc_content_chars_max=1000)
wikipedia = WikipediaQueryRun(api_wrapper=wikipedia_api)
print(f"   Wikipedia tool created: {wikipedia.name}")

# Arxiv prebuilt tool for research papers
print("🔧 Setting up Arxiv tool...")
arxiv_api = ArxivAPIWrapper(top_k_results=3, max_query_length=300)
arxiv = ArxivQueryRun(api_wrapper=arxiv_api)
print(f"   Arxiv tool created: {arxiv.name}")

# Custom tool that also demonstrates how wrapping works
@tool
def format_summary(text: str) -> str:
    """Format the search results into a clean summary.

    Args:
        text: The raw text from the search to format
    """
    print(f"\n[TOOL EXECUTION] format_summary called")
    result = f"### Summary:\n{text}\n\n(Formatted from search results)"
    print(f"[TOOL RESULT]: Summary formatted to {len(result)} characters")
    return result


print("\n🔧 Configuration:")
print("   - Wikipedia: Search Wikipedia for general knowledge")
print("   - Arxiv: Search research papers on arXiv.org")
print("   - format_summary: Custom formatting tool")

tools = [wikipedia, arxiv, format_summary]

# Create agent
agent = create_agent(
    model=get_llm("gpt-4.1"),
    tools=tools,
    middleware=[],
)

print("\n✅ Agent created successfully with 3 tools!")

# Invoke
print("\n🚀 Invoking agent...")
query = "Search Wikipedia for information about Claude Shannon, then search Arxiv for recent papers on large language models. Summarize what you find."
print(f"\n👤 User: {query}")
print("🤖 LLM will use the prebuilt tools to search...")
print("-" * 60)

try:
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
except Exception as e:
    print("-" * 60)
    print(f"\n❌ Error invoking LLM: {type(e).__name__}: {e}")
    print("\nThis example requires a valid OpenAI API key configured in .env")

print("\n" + "=" * 60)
print("Prebuilt tools example completed!")
print("\n💡 Categories of prebuilt tools:")
print("   - Search: Google Search, Tavily, Bing, Wikipedia, Arxiv")
print("   - Database: SQL, MongoDB, Cassandra, Redis")
print("   - File: CSV, PDF, JSON, Excel parsing")
print("   - Code: Python REPL, Bash, Docker")
print("   - APIs: GitHub, Slack, Gmail, Notion, LinkedIn")
print("   - Many more available in langchain-community package")
