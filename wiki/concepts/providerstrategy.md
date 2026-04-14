---
title: ProviderStrategy
date: 2026-04-14
last_updated: 2026-04-14
tags: [ai-agents, langchain, structured-output]
sources: [["wiki/sources/langchain-1-agents", "LangChain - 1. Agents"]]
---

# ProviderStrategy

ProviderStrategy 是 LangChain 中实现[[structured-output|Structured Output]]的一种策略，它使用模型提供商的原生结构化输出生成能力。

## 工作原理

利用 LLM 提供商原生支持的 JSON schema 约束输出功能，直接让模型生成符合指定 schema 的 JSON 输出。

## 优缺点

**优点**：
- 原生支持，更可靠
- 不需要通过工具调用迂回实现
- 性能更好

**缺点**：
- 仅支持提供结构化输出能力的模型提供商
- 兼容性有限

## 使用示例

```python
from pydantic import BaseModel
from langchain.agents import create_agent
from langchain.agents.structured_output import ProviderStrategy

class ContactInfo(BaseModel):
    name: str
    email: str
    phone: str

agent = create_agent(
    model="gpt-4.1",
    response_format=ProviderStrategy(ContactInfo)
)

result = agent.invoke({
    "messages": [{"role": "user", "content": "Extract contact info..."}]
})

contact_info = result["structured_response"]  # type: ContactInfo
```

## 默认行为

从 LangChain 1.0 开始，当你直接传递 schema 时：
```python
agent = create_agent(
    model="gpt-4.1",
    response_format=ContactInfo  # Pydantic schema directly
)
```
LangChain 会自动检测模型是否支持原生结构化输出：
- 如果支持，默认使用 `ProviderStrategy`
- 如果不支持，自动回退到 `ToolStrategy`

## 适用场景

- 模型支持原生结构化输出
- 需要最高可靠性
- 生产环境优先选择

## 相关链接

- [[concepts/structured-output|Structured Output]] - 结构化输出概述
- [[concepts/toolstrategy|ToolStrategy]] - 工具策略
- [[sources/langchain-1-agents|LangChain - 1. Agents]]
