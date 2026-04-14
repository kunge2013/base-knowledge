---
title: Static Tools
date: 2026-04-14
last_updated: 2026-04-14
tags: [ai-agents, langchain, tools]
sources: [["wiki/sources/langchain-1-agents", "LangChain - 1. Agents"]]
---

# Static Tools

Static Tools（静态工具）是在创建 Agent 时就定义好完整工具列表，在整个执行过程中工具集合保持不变的工具管理方式。

## 特点

- 简单直接，最常用
- 工具列表固定不变
- 实现开销最小
- 适合工具集合稳定的场景

## 使用示例

```python
from langchain.tools import tool
from langchain.agents import create_agent

@tool
def search(query: str) -> str:
    """Search for information."""
    return f"Results for: {query}"

@tool
def get_weather(location: str) -> str:
    """Get weather information for a location."""
    return f"Weather in {location}: Sunny, 72°F"

agent = create_agent(model, tools=[search, get_weather])
```

如果提供空工具列表，Agent 将只包含单个 LLM 节点，不具备工具调用能力。

## 适用场景

- 工具集合在设计时就确定
- 不需要基于权限或上下文过滤
- 简单 Agent 应用

## 对比

| 特性 | Static Tools | Dynamic Tools |
|------|--------------|---------------|
| 定义时机 | 创建 Agent 时 | 运行时动态调整 |
| 上下文感知 | 不支持 | 支持 |
| 复杂度 | 低 | 高 |
| 避免上下文过载 | 不适用 | 可以 |

## 相关链接

- [[concepts/dynamic-tools|Dynamic Tools]] - 动态工具
- [[sources/langchain-1-agents|LangChain - 1. Agents]]
- [[concepts/ai-agents|AI Agents - AI 智能体]]
