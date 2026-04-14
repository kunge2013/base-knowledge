---
title: Agent Memory
date: 2026-04-14
last_updated: 2026-04-14
tags: [ai-agents, langchain, state, memory]
sources: [["wiki/sources/langchain-1-agents", "LangChain - 1. Agents"]]
---

# Agent Memory

Agent Memory（Agent 记忆）是 Agent 在对话过程中存储和检索信息的能力。

## 内置记忆

LangChain Agents 通过消息状态自动维护对话历史。完整的对话消息序列保存在状态中，模型可以访问所有历史消息。

## 自定义状态（额外记忆）

你可以通过扩展 `AgentState` 定义自定义状态模式来让 Agent 记住额外的信息，而不仅仅是消息。

有两种方式定义自定义状态：

### 1. 通过 Middleware 定义（推荐）

当自定义状态需要被特定的中间件钩子和工具访问时，使用这种方式：

```python
from langchain.agents import AgentState
from langchain.agents.middleware import AgentMiddleware
from typing import Any

class CustomState(AgentState):
    user_preferences: dict

class CustomMiddleware(AgentMiddleware):
    state_schema = CustomState
    tools = [tool1, tool2]

    def before_model(self, state: CustomState, runtime) -> dict[str, Any] | None:
        # 在这里处理自定义状态
        ...

agent = create_agent(
    model,
    tools=tools,
    middleware=[CustomMiddleware()]
)

# Agent 现在可以跟踪额外状态信息
result = agent.invoke({
    "messages": [{"role": "user", "content": "I prefer technical explanations"}],
    "user_preferences": {"style": "technical", "verbosity": "detailed"},
})
```

### 2. 通过 `state_schema` 参数定义

作为快捷方式，当自定义状态仅在工具中使用时可以这样定义：

```python
from langchain.agents import AgentState

class CustomState(AgentState):
    user_preferences: dict

agent = create_agent(
    model,
    tools=tools,
    state_schema=CustomState
)
```

> LangChain 1.0 之后，自定义状态模式**必须**是 `TypedDict` 类型。不再支持 Pydantic 模型和 dataclasses。

## 记忆分类

### 短期记忆

- 存储在对话状态中
- 只在当前对话会话中保留
- 包括对话历史和当前状态

### 长期记忆

- 跨会话持久化存储
- 需要额外实现
- 可以用来存储用户偏好、过去对话总结等

## 相关链接

- [[concepts/custom-agent-state|Custom Agent State]] - 自定义状态
- [[sources/langchain-1-agents|LangChain - 1. Agents]]
- [[concepts/ai-agents|AI Agents - AI 智能体]]
- [[concepts/langgraph|LangGraph]] - 基于图的状态管理
