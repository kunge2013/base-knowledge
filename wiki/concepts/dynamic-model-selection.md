---
title: Dynamic Model Selection
date: 2026-04-14
last_updated: 2026-04-14
tags: [ai-agents, langchain, model-selection, routing]
sources: [["wiki/sources/langchain-1-agents", "LangChain - 1. Agents"]]
---
d
# Dynamic Model Selection

Dynamic Model Selection（动态模型选择）是根据运行时上下文和状态，在 Agent 执行过程中动态选择不同模型的策略。

## 使用场景

- **成本优化**: 简单问题使用低成本小模型，复杂问题使用强大模型
- **路由**: 根据问题类型路由到专门针对该领域微调的模型
- **对话阶段**: 早期简单问题使用小模型，深入讨论后切换到大模型

## 使用示例

```python
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain.agents.middleware import wrap_model_call, ModelRequest, ModelResponse

basic_model = ChatOpenAI(model="gpt-4.1-mini")
advanced_model = ChatOpenAI(model="gpt-4.1")

@wrap_model_call
def dynamic_model_selection(request: ModelRequest, handler) -> ModelResponse:
    """Choose model based on conversation complexity."""
    message_count = len(request.state["messages"])

    if message_count > 10:
        # Use an advanced model for longer conversations
        model = advanced_model
    else:
        model = basic_model

    return handler(request.override(model=model))

agent = create_agent(
    model=basic_model,  # Default model
    tools=tools,
    middleware=[dynamic_model_selection]
)
```

## 限制

使用结构化输出时，不支持已经预先绑定工具（pre-bound）的模型。确保传递给中间件的模型没有预先调用 `bind_tools`。

## 相关链接

- [[concepts/static-model-selection|Static Model Selection]] - 静态模型选择
- [[concepts/agent-middleware|Agent Middleware]] - 通过中间件实现
- [[sources/langchain-1-agents|LangChain - 1. Agents]]
- [[concepts/routing|Routing - 路由]]
