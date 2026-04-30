"""
09_structured_output.py - Structured Output for Deep Agents

演示如何为 Deep Agents 配置结构化输出：
1. 使用 Pydantic 模型定义响应格式
2. 结构化输出的获取和验证
3. 复杂嵌套结构示例

Key Concepts:
- response_format 参数
- Pydantic 模型验证
- 结构化数据捕获
"""

import os
from typing import Literal, Optional
from dotenv import load_dotenv

load_dotenv()

# =============================================================================
# 方式 1: 基础 Pydantic 响应格式
# =============================================================================

from pydantic import BaseModel, Field
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


# 定义天气报告的 Pydantic 模型
class WeatherReport(BaseModel):
    """A structured weather report with current conditions and forecast."""

    location: str = Field(description="The location for this weather report")
    temperature: float = Field(description="Current temperature in Celsius")
    condition: str = Field(description="Current weather condition (e.g., sunny, cloudy, rainy)")
    humidity: int = Field(description="Humidity percentage")
    wind_speed: float = Field(description="Wind speed in km/h")
    forecast: str = Field(description="Brief forecast for the next 24 hours")


agent_with_structured_output = create_deep_agent(
    model="google_genai:gemini-3.1-pro-preview",
    response_format=WeatherReport,
    tools=[internet_search],
)

# 使用示例
# result = agent_with_structured_output.invoke({
#     "messages": [{
#         "role": "user",
#         "content": "What's the weather like in San Francisco?"
#     }]
# })
#
# # 访问结构化响应
# print(result["structured_response"])
# # WeatherReport(
# #     location='San Francisco, California',
# #     temperature=18.3,
# #     condition='Sunny',
# #     humidity=48,
# #     wind_speed=7.6,
# #     forecast='Pleasant sunny conditions...'
# # )


# =============================================================================
# 方式 2: 复杂嵌套结构
# =============================================================================

class ProductInfo(BaseModel):
    """Product information."""
    name: str = Field(description="Product name")
    price: float = Field(description="Product price in USD")
    category: str = Field(description="Product category")
    rating: float = Field(description="Average rating (0-5)", ge=0, le=5)
    in_stock: bool = Field(description="Whether the product is in stock")


class ProductComparison(BaseModel):
    """A comparison of multiple products."""
    products: list[ProductInfo] = Field(description="List of products being compared")
    best_value: str = Field(description="Name of the best value product")
    recommendation: str = Field(description="Overall recommendation")
    comparison_summary: str = Field(description="Summary of key differences")


agent_product_comparison = create_deep_agent(
    model="google_genai:gemini-3.1-pro-preview",
    response_format=ProductComparison,
    tools=[internet_search],
)


# =============================================================================
# 方式 3: 研究报告结构
# =============================================================================

class ResearchSource(BaseModel):
    """A source used in research."""
    title: str = Field(description="Title of the source")
    url: str = Field(description="URL of the source")
    relevance: str = Field(description="Why this source is relevant")
    credibility: Literal["high", "medium", "low"] = Field(description="Credibility assessment")


class ResearchFindings(BaseModel):
    """Structured research findings."""
    topic: str = Field(description="The research topic")
    executive_summary: str = Field(description="Brief overview of findings")
    key_points: list[str] = Field(description="Main research findings as bullet points")
    sources: list[ResearchSource] = Field(description="Sources used in research")
    limitations: str = Field(description="Any limitations or uncertainties")
    conclusion: str = Field(description="Final conclusion")


agent_research = create_deep_agent(
    model="google_genai:gemini-3.1-pro-preview",
    response_format=ResearchFindings,
    tools=[internet_search],
    system_prompt="""You are an expert researcher who produces structured reports.

Always use the response format to provide well-organized research findings.
Include multiple credible sources and note any limitations in your findings.
""",
)


# =============================================================================
# 方式 4: 数据分析报告
# =============================================================================

class DataStatistics(BaseModel):
    """Statistical summary of a dataset."""
    count: int = Field(description="Number of observations")
    mean: float = Field(description="Mean value")
    median: float = Field(description="Median value")
    std_dev: float = Field(description="Standard deviation")
    min_value: float = Field(description="Minimum value")
    max_value: float = Field(description="Maximum value")


class DataInsight(BaseModel):
    """A key insight from data analysis."""
    insight: str = Field(description="Description of the insight")
    confidence: Literal["high", "medium", "low"] = Field(description="Confidence level")
    supporting_data: str = Field(description="Data that supports this insight")


class DataAnalysisReport(BaseModel):
    """Complete data analysis report."""
    dataset_description: str = Field(description="Description of the analyzed dataset")
    statistics: DataStatistics = Field(description="Statistical summary")
    insights: list[DataInsight] = Field(description="Key insights discovered")
    recommendations: list[str] = Field(description="Actionable recommendations")
    caveats: str = Field(description="Important caveats or limitations")


agent_data_analysis = create_deep_agent(
    model="google_genai:gemini-3.1-pro-preview",
    response_format=DataAnalysisReport,
)


# =============================================================================
# 方式 5: 代码审查报告
# =============================================================================

class CodeIssue(BaseModel):
    """A code quality issue."""
    line_number: Optional[int] = Field(description="Line number if applicable")
    issue_type: Literal["bug", "performance", "security", "style", "maintainability"] = Field(
        description="Type of issue"
    )
    severity: Literal["critical", "major", "minor"] = Field(description="Issue severity")
    description: str = Field(description="Description of the issue")
    suggestion: str = Field(description="Suggested fix")


class CodeReviewReport(BaseModel):
    """Structured code review report."""
    overall_quality: Literal["excellent", "good", "fair", "poor"] = Field(
        description="Overall code quality assessment"
    )
    summary: str = Field(description="Executive summary of the review")
    strengths: list[str] = Field(description="Code strengths")
    issues: list[CodeIssue] = Field(description="Identified issues")
    priority_fixes: list[str] = Field(description="High-priority fixes to address first")
    general_recommendations: str = Field(description="General improvement recommendations")


agent_code_reviewer = create_deep_agent(
    model="google_genai:gemini-3.1-pro-preview",
    response_format=CodeReviewReport,
    system_prompt="""You are an expert code reviewer with deep knowledge of Python best practices.

Provide structured, actionable code reviews that help developers improve their code quality.
Focus on both identifying issues and suggesting concrete improvements.
""",
)


# =============================================================================
# 结构化输出最佳实践
# =============================================================================

"""
结构化输出最佳实践：

1. Pydantic 模型设计
   - 使用 Field 提供详细字段描述
   - 添加验证约束（ge, le, min_length 等）
   - 使用 Literal 限制枚举值

2. 嵌套结构
   - 复杂报告使用嵌套模型
   - 每个嵌套模型职责单一
   - 列表字段用于多条记录

3. 字段描述
   - description 清晰明确
   - 帮助模型理解字段用途
   - 提高输出质量

4. 验证约束
   - ge/le: 数值范围
   - min_length/max_length: 字符串长度
   - pattern: 正则匹配
   - Literal: 枚举值限制

5. 访问响应
   - result["structured_response"] 获取验证后的响应
   - 可以直接访问模型字段
   - 类型安全，IDE 支持自动补全
"""

if __name__ == "__main__":
    print("=" * 60)
    print("Deep Agents - 结构化输出示例")
    print("=" * 60)

    print("\n[1] 基础 Pydantic 模型:")
    print("  - WeatherReport: 天气报告")
    print("  - 包含字段描述和类型约束")

    print("\n[2] 嵌套结构:")
    print("  - ProductComparison: 产品对比")
    print("  - ProductInfo 嵌套在列表中")

    print("\n[3] 研究报告:")
    print("  - ResearchFindings: 结构化研究报告")
    print("  - ResearchSource 嵌套")
    print("  - 包含来源和可信度评估")

    print("\n[4] 数据分析:")
    print("  - DataAnalysisReport: 完整数据分析报告")
    print("  - DataStatistics: 统计摘要")
    print("  - DataInsight: 关键洞察")

    print("\n[5] 代码审查:")
    print("  - CodeReviewReport: 结构化代码审查")
    print("  - CodeIssue: 代码问题分类")
    print("  - 优先级和建议")

    print("\n[最佳实践]:")
    print("  - Field 描述清晰")
    print("  - 验证约束完整")
    print("  - 嵌套结构职责单一")
    print("  - result['structured_response'] 访问")
