---
title: Static Model Selection
date: 2026-04-14
last_updated: 2026-04-14
tags: [ai-agents, langchain, model-selection]
sources: [["wiki/sources/langchain-1-agents", "LangChain - 1. Agents"]]
---

# Static Model Selection

Static Model Selection（静态模型选择）是在创建 Agent 时就确定模型，并且在整个执行过程中保持不变的模型选择策略。

## 特点

- 简单直接，配置一次保持不变
- 大多数场景的默认选择
- 执行开销最小
- 不根据上下文动态变化

## 使用示例

```python
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

# 使用标识符字符串（自动推断）
agent = create_agent("openai:gpt-5", tools=tools)

# 或直接传递模型实例进行完整配置
model = ChatOpenAI(
    model="gpt-5",
    temperature=0.1,
    max_tokens=1000,
    timeout=30
)
agent = create_agent(model, tools=tools)
```

## 适用场景

- 简单的 Agent 应用
- 对话过程中不需要改变模型
- 成本和性能要求优先

## 对比

| 特性 | Static Model Selection | Dynamic Model Selection |
|------|------------------------|-------------------------|
| 配置时机 | 创建 Agent 时 | 运行时 |
| 上下文感知 | 不支持 | 支持 |
| 复杂度 | 低 | 高 |
| 适用场景 | 简单应用 | 复杂路由、成本优化 |

## 相关链接

- [[concepts/dynamic-model-selection|Dynamic Model Selection]] - 动态模型选择
- [[sources/langchain-1-agents|LangChain - 1. Agents]]
- [[concepts/ai-agents|AI Agents - AI 智能体]]
