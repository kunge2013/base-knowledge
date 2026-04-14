---
title: ToolStrategy
date: 2026-04-14
last_updated: 2026-04-14
tags: [ai-agents, langchain, structured-output]
sources: [["wiki/sources/langchain-1-agents", "LangChain - 1. Agents"]]
---

# ToolStrategy

ToolStrategy 是 LangChain 中实现[[structured-output|Structured Output]]的一种策略，它使用人工工具调用来生成结构化输出。

## 工作原理

ToolStrategy 创建一个特殊的工具，该工具接受符合你定义 schema 的参数。模型调用这个特殊工具，其参数就是结构化输出。

这种方法不依赖模型提供商的原生结构化输出支持，只要模型支持工具调用即可工作。

## 优缺点

**优点**：
- 适用于任何支持工具调用的模型
- 兼容性好，回退方案
- schema 定义一致（Pydantic）

**缺点**：
- 迂回方式，不是原生支持
- 可能比 ProviderStrategy 可靠性低一点

## 使用示例

```python
from pydantic import BaseModel
from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy

class ContactInfo(BaseModel):
    name: str
    email: str
    phone: str

agent = create_agent(
    model="gpt-4.1-mini",
    tools=[search_tool],
    response_format=ToolStrategy(ContactInfo)
)

result = agent.invoke({
    "messages": [{"role": "user", "content": "Extract contact info from: John Doe, john@example.com, (555) 123-4567"}]
})

contact_info = result["structured_response"]
# ContactInfo(name='John Doe', email='john@example.com', phone='(555) 123-4567')
```

## 适用场景

- 模型不支持原生结构化输出
- 需要兼容多种模型提供商
- 作为回退方案

## 对比

| 特性 | ToolStrategy | ProviderStrategy |
|------|--------------|------------------|
| 依赖原生支持 | 否 | 是 |
| 兼容性 | 所有支持工具调用的模型 | 仅支持的模型 |
| 可靠性 | 良好 | 更好 |

## 相关链接

- [[concepts/structured-output|Structured Output]] - 结构化输出概述
- [[concepts/providerstrategy|ProviderStrategy]] - 提供商原生策略
- [[sources/langchain-1-agents|LangChain - 1. Agents]]
