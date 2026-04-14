---
title: Dynamic Tools
date: 2026-04-14
last_updated: 2026-04-14
tags: [ai-agents, langchain, tools, context-engineering]
sources: [["wiki/sources/langchain-1-agents", "LangChain - 1. Agents"]]
---

# Dynamic Tools

Dynamic Tools（动态工具）是根据运行时上下文、状态、权限动态调整可用工具集合的工具管理方式。

## 问题背景

不是每个场景都需要所有工具：
- 太多工具可能导致上下文过载（overload context window）
- 太多工具会增加模型选择错误率
- 某些工具仅在特定条件下可用（如认证后）

动态工具选择基于状态调整暴露给模型的工具集合，可以解决这些问题。

## 实现方式

有两种方式取决于工具是否预先可知：
1. **过滤预注册工具** - 所有工具已知，基于条件过滤（推荐）
2. **运行时注册** - 工具在运行时动态注册

## 示例：基于状态过滤工具

```python
from langchain.agents import create_agent
from langchain.agents.middleware import wrap_model_call, ModelRequest, ModelResponse

@wrap_model_call
def state_based_tools(
    request: ModelRequest,
    handler
) -> ModelResponse:
    """Filter tools based on conversation State."""
    # Read from State: check if user has authenticated
    state = request.state
    is_authenticated = state.get("authenticated", False)
    message_count = len(state["messages"])

    # Only enable sensitive tools after authentication
    if not is_authenticated:
        tools = [t for t in request.tools if t.name.startswith("public_")]
        request = request.override(tools=tools)
    elif message_count < 5:
        # Limit tools early in conversation
        tools = [t for t in request.tools if t.name != "advanced_search"]
        request = request.override(tools=tools)

    return handler(request)

agent = create_agent(
    model="gpt-4.1",
    tools=[public_search, private_search, advanced_search],
    middleware=[state_based_tools]
)
```

## 适用场景

- **基于权限**：未认证用户只能访问公共工具，认证后才能访问敏感工具
- **基于对话阶段**：对话早期只开放基础工具，深入讨论后开放高级工具
- **基于功能开关**：根据功能开关动态启用/禁用功能
- **基于用户角色**：不同角色的用户可用工具不同

## 最佳实践

这种方法最适合：
- 所有可能工具在启动/编译时已知
- 需要基于权限、功能开关、对话状态过滤
- 工具是静态的但可用性是动态的

## 相关链接

- [[concepts/static-tools|Static Tools]] - 静态工具
- [[concepts/agent-middleware|Agent Middleware]] - 通过中间件实现
- [[concepts/context-engineering|Context Engineering - 上下文工程]] - 避免上下文过载
- [[sources/langchain-1-agents|LangChain - 1. Agents]]
