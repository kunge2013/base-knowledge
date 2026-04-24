"""
02_custom_tools.py - Custom Tools for Deep Agents

演示如何为 Deep Agents 创建和配置自定义工具：
1. 使用 Python 函数定义工具（类型注解自动生成 schema）
2. 使用 @tool 装饰器创建工具
3. 工具的文档字符串作为 Agent 理解工具用途的描述

Key Concepts:
- 类型注解驱动 Schema 生成
- @tool 装饰器
- 文档字符串即工具描述
"""

import os
from typing import Literal
from dotenv import load_dotenv

load_dotenv()

# =============================================================================
# 方式 1: 使用 Python 函数定义工具（推荐）
# =============================================================================

from tavily import TavilyClient
from deepagents import create_deep_agent

tavily_client = TavilyClient(api_key=os.environ.get("TAVILY_API_KEY", ""))


def internet_search(
    query: str,
    max_results: int = 5,
    topic: Literal["general", "news", "finance"] = "general",
    include_raw_content: bool = False,
):
    """
    Run an internet search using Tavily API.

    Args:
        query: The search query string
        max_results: Maximum number of search results to return (default: 5)
        topic: Category of search - 'general', 'news', or 'finance' (default: 'general')
        include_raw_content: Whether to include full page content in results (default: False)

    Returns:
        dict: Search results from Tavily API
    """
    return tavily_client.search(
        query,
        max_results=max_results,
        include_raw_content=include_raw_content,
        topic=topic,
    )


agent_with_tools = create_deep_agent(
    model="google_genai:gemini-3.1-pro-preview",
    tools=[internet_search],
)


# =============================================================================
# 方式 2: 使用 @tool 装饰器
# =============================================================================

from langchain.tools import tool


@tool
def get_weather(city: str) -> str:
    """Get the weather in a city."""
    # 示例实现 - 实际使用请替换为真实 API
    return f"The weather in {city} is sunny."


@tool
def calculate_bmi(weight_kg: float, height_m: float) -> float:
    """
    Calculate Body Mass Index (BMI).

    Args:
        weight_kg: Weight in kilograms
        height_m: Height in meters

    Returns:
        BMI value
    """
    return weight_kg / (height_m ** 2)


@tool
def convert_currency(amount: float, from_currency: str, to_currency: str) -> str:
    """
    Convert currency from one to another.

    Args:
        amount: Amount to convert
        from_currency: Source currency code (e.g., USD, EUR)
        to_currency: Target currency code (e.g., USD, EUR)

    Returns:
        Converted amount string
    """
    # 示例实现 - 实际使用请替换为真实汇率 API
    exchange_rates = {
        ("USD", "EUR"): 0.85,
        ("EUR", "USD"): 1.18,
        ("USD", "CNY"): 7.2,
        ("CNY", "USD"): 0.14,
    }
    rate = exchange_rates.get((from_currency.upper(), to_currency.upper()), 1.0)
    return f"{amount * rate:.2f} {to_currency.upper()}"


agent_with_multiple_tools = create_deep_agent(
    model="google_genai:gemini-3.1-pro-preview",
    tools=[get_weather, calculate_bmi, convert_currency, internet_search],
)


# =============================================================================
# 方式 3: 使用 Pydantic 定义工具 Schema
# =============================================================================

from pydantic import BaseModel, Field


class SearchInput(BaseModel):
    """Input schema for search tool."""
    query: str = Field(description="The search query string")
    max_results: int = Field(default=5, description="Maximum number of results")
    topic: Literal["general", "news", "finance"] = Field(default="general")


def search_with_pydantic(query: str, max_results: int = 5, topic: str = "general"):
    """Search tool with explicit Pydantic schema."""
    return tavily_client.search(query, max_results=max_results, topic=topic)


# =============================================================================
# 工具最佳实践
# =============================================================================

"""
工具定义最佳实践：

1. 函数命名
   - 使用动词 + 名词结构（如 internet_search, get_weather）
   - 名称应清晰描述工具功能

2. 类型注解
   - 所有参数必须有类型注解
   - 使用 Literal 限制字符串取值范围
   - 返回类型明确声明

3. 文档字符串
   - 第一行简洁描述工具功能
   - 详细 Args 说明每个参数
   - Returns 说明返回值格式

4. 错误处理
   - 工具内部应处理异常情况
   - 返回友好的错误信息

5. 参数设计
   - 提供合理的默认值
   - 避免过多参数（建议不超过 5 个）
"""

if __name__ == "__main__":
    print("=" * 60)
    print("Deep Agents - 自定义工具示例")
    print("=" * 60)

    print("\n[1] Python 函数定义工具:")
    print("  - internet_search(query, max_results, topic)")
    print("  - 类型注解自动生成 schema")

    print("\n[2] @tool 装饰器:")
    print("  - @tool def get_weather(city: str) -> str")
    print("  - @tool def calculate_bmi(weight_kg, height_m)")
    print("  - @tool def convert_currency(amount, from, to)")

    print("\n[3] Pydantic Schema:")
    print("  - class SearchInput(BaseModel)")
    print("  - 显式定义输入 schema")

    print("\n[工具最佳实践]:")
    print("  - 动词 + 名词命名")
    print("  - 完整类型注解")
    print("  - 详细文档字符串")
    print("  - 合理默认值")
