---
title: Custom Agent State
date: 2026-04-14
last_updated: 2026-04-14
tags: [ai-agents, langchain, langgraph, state]
sources: [["wiki/sources/langchain-1-agents", "LangChain - 1. Agents"]]
---

# Custom Agent State

Custom Agent State（自定义 Agent 状态）允许你扩展默认 Agent 状态来存储额外信息，实现更复杂的记忆能力。

## 定义方式

自定义状态**必须**继承 `AgentState` 并定义为 `TypedDict`。

> LangChain 1.0+ 要求：Pydantic 模型和 dataclasses 不再支持。

## 两种定义方式

### 1. 通过 Middleware（推荐）

当你的自定义状态需要被特定的中间件钩子和工具访问时，使用这种方式：

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
        # 在模型调用前处理自定义状态
        ...

agent = create_agent(
    model,
    tools=tools,
    middleware=[CustomMiddleware()]
)
```

这种方式的优点：可以将状态扩展保持在概念上的范围内，只被相关的中间件和工具访问。

### 2. 通过 `state_schema` 参数

作为快捷方式，当自定义状态仅在工具中使用不需要中间件访问时，可以直接在 `create_agent` 中定义：

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

这种方式仍然支持向后兼容性，但不推荐用于复杂场景。

## 使用示例

```python
result = agent.invoke({
    "messages": [{"role": "user", "content": "I prefer technical explanations"}],
    "user_preferences": {"style": "technical", "verbosity": "detailed"},
})
```

现在 Agent 可以在整个对话过程中记住 `user_preferences`。

## 相关链接

- [[concepts/agent-memory|Agent Memory]] - Agent 记忆概述
- [[concepts/agent-middleware|Agent Middleware]] - 通过中间件扩展
- [[sources/langchain-1-agents|LangChain - 1. Agents]]
- [[concepts/langgraph|LangGraph]] - 基于图的状态管理
