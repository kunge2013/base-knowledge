---
title: Structured Output
date: 2026-04-14
last_updated: 2026-04-14
tags: [ai-agents, langchain, output-formatting, pydantic]
sources: [["wiki/sources/langchain-1-agents", "LangChain - 1. Agents"]]
---

# Structured Output

Structured Output（结构化输出）是让 AI Agent 输出符合特定模式（schema）的结构化数据，而不是自由文本。

## 使用场景

- 从非结构化文本提取特定信息
- 要求输出可被程序直接解析
- 数据管道中的数据标准化
- 保证输出字段存在且类型正确

## 两种策略

LangChain 提供两种策略实现结构化输出：

### 1. ProviderStrategy

使用模型提供商原生的结构化输出生成能力。

**优点**：更可靠，原生支持
**缺点**：仅部分提供商支持

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

contact = result["structured_response"]  # type: ContactInfo
```

### 2. ToolStrategy

使用人工工具调用来生成结构化输出。适用于任何支持工具调用的模型。

**优点**：适用于任何模型，兼容性好
**缺点**：通过工具调用迂回实现

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
    "messages": [{"role": "user", "content": "Extract contact info..."}]
})

contact = result["structured_response"]  # type: ContactInfo
```

## 默认行为

从 LangChain 1.0 开始：
- 如果模型支持原生结构化输出，默认使用 `ProviderStrategy`
- 否则自动回退到 `ToolStrategy`
- 也可以显式指定策略

## 相关链接

- [[concepts/toolstrategy|ToolStrategy]]  - 工具策略
- [[concepts/providerstrategy|ProviderStrategy]]  - 提供商原生策略
- [[sources/langchain-1-agents|LangChain - 1. Agents]]
- [[concepts/langchain|LangChain]]
