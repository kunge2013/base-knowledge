"""
05_subagents.py - Subagents Configuration for Deep Agents

演示如何为 Deep Agents 配置子代理：
1. 使用字典定义子代理配置
2. 子代理继承和覆盖主代理配置
3. 多子代理协作场景

Key Concepts:
- 子代理隔离复杂任务
- 避免上下文膨胀
- 专业化子代理
"""

import os
from typing import Literal
from dotenv import load_dotenv

load_dotenv()

# =============================================================================
# 共享工具定义
# =============================================================================

from tavily import TavilyClient
from deepagents import create_deep_agent

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
# 方式 1: 基础子代理配置
# =============================================================================

# 定义研究子代理
research_subagent = {
    "name": "research-agent",
    "description": "Used to research more in-depth questions. This agent specializes in gathering and analyzing information from multiple sources.",
    "system_prompt": "You are a great researcher with expertise in information gathering and analysis. "
                     "Your job is to conduct thorough research on complex topics. "
                     "Always search for multiple sources and cross-reference information.",
    "tools": [internet_search],
    # "model": "openai:gpt-5.4",  # 可选：覆盖主代理模型，默认使用主代理模型
}

subagents = [research_subagent]

agent_with_subagent = create_deep_agent(
    model="anthropic:claude-sonnet-4-6",
    subagents=subagents,
)


# =============================================================================
# 方式 2: 多个专业化子代理
# =============================================================================

# 新闻分析子代理
news_analyst_subagent = {
    "name": "news-analyst",
    "description": "Specialized in analyzing current news and recent events. Use this for time-sensitive information.",
    "system_prompt": """You are a news analyst specializing in current events and recent developments.

Your responsibilities:
- Search for the latest news on topics
- Analyze multiple news sources
- Identify key trends and patterns
- Distinguish between facts and opinions
- Note the recency and relevance of information

Always prioritize recent, credible news sources.
""",
    "tools": [internet_search],
    "model": "google_genai:gemini-3.1-pro-preview",
}

# 技术分析子代理
tech_analyst_subagent = {
    "name": "tech-analyst",
    "description": "Expert in technical analysis, code review, and technology research.",
    "system_prompt": """You are a technical analyst with deep expertise in software development and technology.

Your expertise includes:
- Programming languages and frameworks
- Software architecture and design patterns
- Technical documentation analysis
- Code best practices
- Technology trends and comparisons

Provide clear, accurate technical explanations with code examples when appropriate.
""",
    "tools": [internet_search],
    "model": "anthropic:claude-sonnet-4-6",
}

# 金融分析子代理
finance_analyst_subagent = {
    "name": "finance-analyst",
    "description": "Specialized in financial analysis, market research, and economic data.",
    "system_prompt": """You are a financial analyst with expertise in markets, economics, and financial data.

Your capabilities:
- Market analysis and trends
- Company financial health assessment
- Economic indicator interpretation
- Investment research
- Risk analysis

Always note that you provide analysis, not financial advice. Include appropriate disclaimers.
""",
    "tools": [internet_search],
}

multi_agent_system = create_deep_agent(
    model="anthropic:claude-sonnet-4-6",
    subagents=[news_analyst_subagent, tech_analyst_subagent, finance_analyst_subagent],
    system_prompt="""You are a master analyst coordinating a team of specialized analysts.

Your team includes:
- news-analyst: For current events and recent news
- tech-analyst: For technical and software-related analysis
- finance-analyst: For financial and market analysis

Your role:
1. Understand the user's request
2. Delegate to the appropriate specialist(s)
3. Synthesize their findings into a comprehensive response
4. Highlight key insights and conclusions
""",
)


# =============================================================================
# 方式 3: 层次化子代理（子代理再有子代理）
# =============================================================================

# 初级研究子代理
junior_researcher = {
    "name": "junior-researcher",
    "description": "Performs initial data gathering and basic research tasks.",
    "system_prompt": "You are a junior researcher. Gather basic information on topics using available tools.",
    "tools": [internet_search],
}

# 高级研究子代理
senior_researcher = {
    "name": "senior-researcher",
    "description": "Performs deep analysis and synthesis of research findings.",
    "system_prompt": """You are a senior researcher with expertise in analysis and synthesis.

Your responsibilities:
- Analyze information gathered by junior researchers
- Identify patterns and connections
- Draw well-supported conclusions
- Write comprehensive reports
""",
    "tools": [internet_search],
}

hierarchical_agent = create_deep_agent(
    model="anthropic:claude-sonnet-4-6",
    subagents=[junior_researcher, senior_researcher],
)


# =============================================================================
# 子代理使用场景
# =============================================================================

"""
子代理使用场景：

1. 专业化分工
   - 不同领域由不同子代理处理
   - 每个子代理有专门的知识和工具

2. 任务隔离
   - 复杂任务委托给子代理
   - 避免主代理上下文膨胀

3. 模型优化
   - 简单任务使用便宜模型
   - 复杂分析使用强大模型

4. 并行处理
   - 多个子代理可并行工作
   - 提高整体效率

5. 层次化处理
   - 初级代理收集信息
   - 高级代理分析综合
"""

if __name__ == "__main__":
    print("=" * 60)
    print("Deep Agents - 子代理配置示例")
    print("=" * 60)

    print("\n[1] 基础子代理:")
    print("  - research-agent: 专业研究子代理")
    print("  - 包含专用工具和提示词")

    print("\n[2] 多子代理系统:")
    print("  - news-analyst: 新闻分析")
    print("  - tech-analyst: 技术分析")
    print("  - finance-analyst: 金融分析")
    print("  - 主代理协调各子代理")

    print("\n[3] 层次化子代理:")
    print("  - junior-researcher: 初级信息收集")
    print("  - senior-researcher: 高级分析综合")

    print("\n[子代理优势]:")
    print("  - 专业化分工")
    print("  - 任务隔离，避免上下文膨胀")
    print("  - 可针对不同任务选择不同模型")
    print("  - 支持并行处理")
