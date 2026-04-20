# 短期记忆

短期记忆系统让应用程序能够在单个线程或对话中记住之前的交互。对于 AI Agent 来说，记忆至关重要，因为它让它们能够记住之前的交互、从反馈中学习，并适应用户偏好。

## 一、短期记忆概述

### 1.1 记忆的作用

记忆是一个记住之前交互信息的系统，对 AI Agent 至关重要：
- 记住之前的交互
- 从反馈中学习
- 适应用户偏好
- 提高效率和用户满意度

### 1.2 线程与对话历史

```mermaid
graph LR
    A[Thread 1] --> B[Conversation History]
    C[Thread 2] --> D[Conversation History]
    E[Thread N] --> F[Conversation History]

    B --> G[Checkpointer]
    D --> G
    F --> G

    G --> H[持久存储]

    style B fill:#e1f5ff
    style D fill:#e1f5ff
    style F fill:#e1f5ff
    style G fill:#ffe1e1
```

**关键概念：**
- **线程（Thread）**：组织会话中的多个交互，类似邮件将消息分组在单个对话中
- **对话历史（Conversation History）**：最常见的短期记忆形式
- **Checkpointer**：将状态持久化到数据库或内存，支持对话恢复

### 1.3 上下文窗口挑战

长对话对当今的 LLM 提出挑战：
- 完整的历史可能无法放入 LLM 的上下文窗口
- 导致上下文丢失或错误
- 即使模型支持完整上下文长度，大多数 LLM 在长上下文上仍然表现不佳
- 模型会因陈旧或离题的内容而"分心"
- 响应时间更慢、成本更高

## 二、基本使用

### 2.1 使用 Checkpointer

**场景：** 为 Agent 添加短期记忆（线程级持久化）

**代码示例：**

```python
"""01_basic_usage.py
使用 checkpointer 实现短期记忆
"""

from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from llm_config import default_llm
from langchain.tools import tool

@tool
def get_user_info(query: str) -> str:
    """Get user information."""
    return f"User info for: {query}"

# 创建带 checkpointer 的 Agent
agent = create_agent(
    default_llm,
    tools=[get_user_info],
    checkpointer=InMemorySaver(),
)

# 使用 thread_id 维护对话历史
config = {"configurable": {"thread_id": "1"}"

# 第一次交互
result1 = agent.invoke(
    {"messages": [{"role": "user", "content": "Hi! My name is Bob."}]},
    config
)
print(f"First response: {result1['messages'][-1].content}")

# 第二次交互 - Agent 记住了名字
result2 = agent.invoke(
    {"messages": [{"role": "user", "content": "What's my name?"}]},
    config
)
print(f"Second response: {result2['messages'][-1].content}")
```

**工作原理：**
1. Agent 将状态存储在图的状态中
2. Checkpointer 将状态持久化到数据库或内存
3. 使用 `thread_id` 可以在任何时候恢复对话
4. 状态在每次调用开始时读取，在 Agent 调用或步骤（如工具调用）完成时更新

### 2.2 生产环境配置

**场景：** 使用数据库支持的生产级 Checkpointer

**代码示例：**

```python
"""生产环境配置示例
使用 PostgreSQL Checkpointer
"""

from langchain.agents import create_agent
from langgraph.checkpoint.postgres import PostgresSaver

DB_URI = "postgresql://postgres:postgres@localhost:5442/postgres?sslmode=disable"

with PostgresSaver.from_conn_string(DB) as checkpointer:
    checkpointer.setup()  # 在 PostgreSQL 中自动创建表
    agent = create_agent(
        default_llm,
        tools=[get_user_info],
        checkpointer=checkpointer,
    )

    # 使用 Agent
    result = agent.invoke(
        {"messages": [{"role": "user", "content": "Hello"}]},
        {"configurable": {"thread_id": "1"}}
    )
```

**可用的 Checkpointer：**
- **InMemorySaver**：内存存储，用于开发和测试
- **PostgresSaver**：PostgreSQL 存储，用于生产环境
- **SQLiteSaver**：SQLite 存储，轻量级持久化
- **AzureCosmosDBSaver**：Azure Cosmos DB 存储

### 2.3 自定义状态模式

**场景：** 扩展 AgentState 添加额外字段

**代码示例：**

```python
"""02_custom_state.py
自定义 Agent 状态模式
"""

from langchain.agents import create_agent, AgentState
from langgraph.checkpoint.memory import InMemorySaver
from llm_config import default_llm
from langchain.tools import tool

class CustomAgentState(AgentState):
    user_id: str
    preferences: dict

@tool
def get_user_info(query: str) -> str:
    """Get user information."""
    return f"User info for: {query}"

# 创建带自定义状态的 Agent
agent = create_agent(
    default_llm,
    tools=[get_user_info],
    state_schema=CustomAgentState,
    checkpointer=InMemorySaver(),
)

# 在 invoke 中传递自定义状态
result = agent.invoke(
    {
        "messages": [{"role": "user", "content": "Hello"}],
        "user_id": "user_123",
        "preferences": {"theme": "dark"}
    },
    {"configurable": {"thread_id": "1"}}
)

print(f"Response: {result['messages'][-1].content}")
print(f"User ID: {result['user_id']}")
print(f"Preferences: {result['preferences']}")
```

## 三、记忆管理策略

### 3.1 策略概述

```mermaid
graph TD
    A[对话历史] --> B{策略选择}
    B -->|修剪| C[Trim Messages]
    B -->|删除| D[Delete Messages]
    B -->|摘要| E[Summarize Messages]
    B -->|自定义| F[Custom Strategies]

    C --> G[适应上下文窗口]
    D --> G
    E --> G
    F --> G

    style B fill:#e1f5ff
    style G fill:#ffe1e1
```

**常见策略：**
1. **修剪消息（Trim messages）**：移除前 N 个或后 N 个消息
2. **删除消息（Delete messages）**：从 LangGraph 状态中永久删除消息
3. **摘要消息（Summarize messages）**：摘要历史记录中的较早消息并用摘要替换
4. **自定义策略（Custom strategies）**：例如消息过滤等

### 3.2 修剪消息

**场景：** 保持最后几条消息以适应上下文窗口

**流程图：**

```mermaid
sequenceDiagram
    participant User
    participant Middleware
    participant LLM

    User->>Middleware: 输入消息
    Middleware->>Middleware: 检查消息数量
    alt 消息过多
        Middleware->>Middleware: 保留系统消息 + 最近 N 条
        Middleware->>Middleware: 移除其他消息
    end
    Middleware->>LLM: 处理后的消息
    LLM->>User: 响应
```

**代码示例：**

```python
"""03_trim_messages.py
使用中间件修剪消息
"""

from langchain.messages import RemoveMessage
from langgraph.graph.message import REMOVE_ALL_MESSAGES
from langchain.checkpoint.memory import InMemorySaver
from langchain.agents import create_agent, AgentState
from langchain.agents.middleware import before_model
from langgraph.runtime import Runtime
from typing import Any
from llm_config import default_llm

@before_model
def trim_messages(state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
    """Keep only: last few messages to fit context window."""
    messages = state["messages"]

    if len(messages) <= 3:
        return None  # 不需要更改

    # 保留第一条消息（系统）和最后几条消息
    first_msg = messages[0]
    recent_messages = messages[-3:] if len(messages) % 2 == 0 else messages[-4:]
    new_messages = [first_msg] + recent_messages

    return {
        "messages": [
                RemoveMessage(id=REMOVE_ALL_MESSAGES),
                *new_messages
            ]
    }

# 创建带修剪中间件的 Agent
agent = create_agent(
    default_llm,
    tools=[],
    middleware=[trim_messages],
    checkpointer=InMemorySaver(),
)

config = {"configurable": {"thread_id": "1"}}

# 模拟多次交互
print("Trimming messages to keep conversation manageable...")
result = agent.invoke({"messages": "hi, my name is bob"}, config)
result = agent.invoke({"messages": "write a short poem about cats"}, config)
result = agent.invoke({"messages": "now do same but for dogs"}, config)
final_response = agent.invoke({"messages": "what's my name?"}, config)

print(f"Final response: {final_response['messages'][-1].content}")
```

**输出示例：**
```
Your name is Bob. You told me that earlier.
If you'd like me to call you a nickname or use a different name, just say the word.
```

### 3.3 删除消息

**场景：** 从图状态中删除特定消息或清除整个消息历史

**代码示例：**

```python
"""04_delete_messages.py
使用 RemoveMessage 删除消息
"""

from langchain.messages import RemoveMessage
from langchain.agents import create_agent, AgentState
from langchain.agents.middleware import after_model
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.runtime import Runtime
from llm_config import default_llm

@after_model
def delete_old_messages(state: AgentState, runtime: Runtime) -> dict | None:
    """Remove old messages to keep conversation manageable."""
    messages = state["messages"]
    if len(messages) > 2:
        # 删除最早的两条消息
        return {"messages": [RemoveMessage(id=m.id) for m in messages[:2]]}
    return None

# 创建带删除中间件的 Agent
agent = create_agent(
    default_llm,
    tools=[],
    system_prompt="Please be concise and to the point.",
    middleware=[delete_old_messages],
    checkpointer=InMemorySaver(),
)

config = {"configurable": {"thread_id": "1"}]

print("Deleting old messages to manage conversation length...")
for event in agent.stream(
    {"messages": [{"role": "user", "content": "hi! I'm bob"}]},
    config,
    stream_mode="values",
):
    if "messages" in event:
        message_types = [(message.type, message.content[:50]) for message in event["messages"]]
        print(f"Messages: {message_types}")
```

**重要提示：**
- 删除消息时，确保生成的消息历史是有效的
- 检查所使用的 LLM 提供商的限制
- 一些提供商期望消息历史以 `user` 消息开头
- 大多数提供商要求带有工具调用的 `assistant` 消息后跟相应的 `tool` 结果消息

### 3.4 摘要消息

**场景：** 使用更复杂的方法摘要消息历史

**优势：**
- 保留重要信息而不失去上下文
- 减少token 使用
- 保持对话的连贯性

**代码示例：**

```python
"""05_summarize_messages.py
使用内置的摘要中间件
"""

from langchain.agents import create_agent
from langchain.agents.middleware import SummarizationMiddleware
from langgraph.checkpoint.memory import InMemorySaver
from llm_config import default_llm

checkpointer = InMemorySaver()

# 创建带摘要中间件的 Agent
agent = create_agent(
    default_llm,
    tools=[],
    middleware=[
        SummarizationMiddleware(
                model=default_llm,
                trigger=("tokens", 4000),  # 超过 4000 tokens 时触发
                keep=("messages", 20)       # 保留最后 20 条消息
            )
    ],
    checkpointer=checkpointer,
)

config = {"configurable": {"thread_id": "1"}}

print("Summarizing message history to manage context window...")
agent.invoke({"messages": "hi, my name is bob"}, config)
agent.invoke({"messages": "write a short poem about cats"}, config)
agent.invoke({"messages": "now do same but for dogs"}, config)
final_response = agent.invoke({"messages": "what's my name?"}, config)

print(f"Final response: {final_response['messages'][-1].content}")
```

**输出示例：**
```
Your name is Bob!
```

## 四、访问记忆

### 4.1 访问方式概述

```mermaid
graph TD
    A[短期记忆访问] --> B[工具]
    A --> C[提示]
    A --> D[Before Model]
    A --> E[After Model]

    B --> F[读写状态]
    C --> G[创建动态提示]
    D --> H[处理消息]
    E --> I[验证响应]

    style A fill:#e1f5ff
```

### 4.2 从工具中读取短期记忆

**场景：** 工具需要访问对话状态

**代码示例：**

```python
"""06_tool_read_state.py
从工具读取短期记忆
"""

from langchain.agents import create_agent, AgentState
from langchain.tools import tool, ToolRuntime
from llm_config import default_llm

class CustomState(AgentState):
    user_id: str

@tool
def get_user_info(
    runtime: ToolRuntime
) -> str:
    """Look up user info."""
    user_id = runtime.state["user_id"]
    return "User is John Smith" if user_id == "user_123" else "Unknown user"

agent = create_agent(
    default_llm,
    tools=[get_user_info],
    state_schema=CustomState,
)

result = agent.invoke({
    "messages": "look up user information",
    "user_id": "user_123"
})

print(f"Response: {result['messages'][-1].content}")
```

### 4.3 从工具中写入短期记忆

**场景：** 工具需要更新 Agent 的短期记忆

**代码示例：**

```python
"""07_tool_write_state.py
从工具写入短期记忆
"""

from langchain.tools import tool, ToolRuntime
from langchain.messages import ToolMessage
from langchain.agents import create_agent, AgentState
from langgraph.types import Command
from pydantic import BaseModel
from llm_config import default_llm

class CustomState(AgentState):
    user_name: str

class CustomContext(BaseModel):
    user_id: str

@tool
def update_user_info(
    runtime: ToolRuntime[CustomContext, CustomState],
) -> Command:
    """Look up and update user info."""
    user_id = runtime.context.user_id
    name = "John Smith" if user_id == "user_123" else "Unknown"
    return Command(update={
        "user_name": name,
        # 更新消息历史
        "messages": [
            ToolMessage(
                "Successfully looked up user information",
                tool_call_id=runtime.tool_call_id
            )
        ]
    })

@tool
def greet(
    runtime: ToolRuntime[CustomContext, CustomState]
) -> str | Command:
    """Greet user once you found their info."""
    user_name = runtime.state.get("user_name", None)
    if user_name is None:
        return Command(update={
                "messages": [
                    ToolMessage(
                                "Please call 'update_user_info' tool first.",
                                tool_call_id=runtime.tool_call_id
                            )
                ]
            })
    return f"Hello {user_name}!"

agent = create_agent(
    default_llm,
    tools=[update_user_info, greet],
    state_schema=CustomState,
    context_schema=CustomContext,
)

print("Tools that update state:")
result = agent.invoke(
    {"messages": [{"role": "user", "content": "greet me"}]},
    context=CustomContext(user_id="user_123"),
)
print(f"Response: {result['messages'][-1].content}")
```

### 4.4 动态提示

**场景：** 基于对话历史或自定义状态字段创建动态提示

**代码示例：**

```python
"""08_dynamic_prompt.py
创建基于状态的动态提示
"""

from langchain.agents import create_agent
from typing import TypedDict
from langchain.agents.middleware import dynamic_prompt, ModelRequest
from llm_config import default_llm
from langchain.tools import tool

class CustomContext(TypedDict):
    user_name: str

@tool
def get_weather(city: str) -> str:
    """Get weather in a city."""
    return f"The weather in {city} is always sunny!"

@dynamic_prompt
def dynamic_system_prompt(request: ModelRequest) -> str:
    user_name = request.runtime.context["user_name"]
    system_prompt = f"You are a helpful assistant. Address the user as {user_name}."
    return system_prompt

agent = create_agent(
    default_llm,
    tools=[get_weather],
    middleware=[dynamic_system_prompt],
    context_schema=CustomContext,
)

print("Dynamic prompt based on context:")
result = agent.invoke(
    {"messages": [{"role": "user", "content": "What is the weather in SF?"]]},
    context=CustomContext(user_name="John Smith"),
)

for msg in result["messages"]:
    print(f"{msg.type}: {msg.content[:100]}")
```

**输出示例：**
```
human: What is the weather in SF?
ai: Hi John Smith, the weather in San Francisco is always sunny!
```

### 4.5 Before Model 中间件

**场景：** 在模型调用之前处理消息

**代码示例：**

```python
"""使用 @before_model 中间件
"""

from langchain.messages import RemoveMessage
from langgraph.graph.message import REMOVE_ALL_MESSAGES
from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents import create_agent, AgentState
from langchain.agents.middleware import before_model
from langgraph.runtime import Runtime
from typing import Any

@before_model
def trim_messages(state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
    """Keep only the last few messages to fit context window."""
    messages = state["messages"]

    if len(messages) <= 3:
        return None  # 不需要更改

    first_msg = messages[0]
    recent_messages = messages[-3:] if len(messages) % 2 == 0 else messages[-4:]
    new_messages = [first_msg] + recent_messages

    return {
        "messages": [
                RemoveMessage(id=REMOVE_ALL_MESSAGES),
                *new_messages
            ]
    }

agent = create_agent(
    default_llm,
    tools=[],
    middleware=[trim_messages],
    checkpointer=InMemorySaver(),
)
```

### 4.6 After Model 中间件

**场景：** 在模型调用之后处理消息

**代码示例：**

```python
"""使用 @after_model 中间件
"""

from langchain.messages import RemoveMessage
from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents import create_agent, AgentState
from langchain.agents.middleware import after_model
from langgraph.runtime import Runtime

@after_model
def validate_response(state: AgentState, runtime: Runtime) -> dict | None:
    """Remove messages containing sensitive words."""
    STOP_WORDS = ["password", "secret"]
    last_message = state["messages"][-1]
    if any(word in last_message.content for word in STOP_WORDS):
        return {"messages": [RemoveMessage(id=last_message.id)]}
    return None

agent = create_agent(
    default_llm,
    tools=[],
    middleware=[validate_response],
    checkpointer=InMemorySaver(),
)
```

## 五、最佳实践总结

### 5.1 记忆管理策略选择

| 策略 | 适用场景 | 优势 | 劣势 |
|------|---------|------|------|
| **修剪消息** | 需要快速响应，可以失去一些上下文 | 简单快速 | 可能丢失重要信息 |
| **删除消息** | 需要彻底清理旧消息 | 完全清除 | 失去所有上下文 |
| **摘要消息** | 需要保留关键信息 | 保留上下文完整性 | 需要 LLM 调用 |
| **自定义策略** | 特定的业务需求 | 灵活性高 | 需要更多开发 |

### 5.2 中间件使用指南

| 中间件 | 触发时机 | 使用场景 |
|-------|---------|---------|
| **@before_model** | 模型调用之前 | 消息修剪、验证、转换 |
| **@after_model** | 模型调用之后 | 响应验证、消息清理、日志记录 |
| **@dynamic_prompt** | 提示生成时 | 基于状态的动态提示 |
| **SummarizationMiddleware** | 按需摘要时 | 内置的摘要功能 |

### 5.3 Checkpointer 选择

| Checkpointer | 使用场景 | 优势 |
|-----------|---------|------|
| **InMemorySaver** | 开发、测试 | 无外部依赖，快速 |
| **PostgresSaver** | 生产环境 | 持久化、高可用性 |
| **SQLiteSaver** | 轻量级应用 | 无需数据库服务器 |
| **AzureCosmosDBSaver** | Azure 环境 | 云原生集成 |

### 5.4 常见陷阱

- **忘记 thread_id**：始终使用唯一的 thread_id 来区分不同的对话
- **消息历史无效**：删除或修剪消息后，确保消息历史对 LLM 提供商有效
- **过度摘要**：摘要过于频繁可能增加成本和延迟
- **状态冲突**：并行工具调用更新相同状态字段时，需要定义 reducer
- **内存泄漏**：确保定期清理或总结旧线程的状态

## 六、完整工作流程示例

以下是一个完整的短期记忆工作流程，展示了从配置到使用的全过程：

```python
"""完整短期记忆工作流程示例
"""

from dataclasses import dataclass
from typing import Any, TypedDict
from pydantic import BaseModel
from langchain.agents import create_agent, AgentState
from langchain.agents.middleware import before_model, dynamic_prompt, ModelRequest
from langchain.tools import tool, ToolRuntime
from langchain.messages import ToolMessage
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.runtime import Runtime
from langgraph.types import Command
from llm_config import default_llm

# 自定义状态
class CustomAgentState(AgentState):
    user_id: str
    user_name: str
    preferences: dict

class CustomContext(BaseModel):
    user_id: str

# 定义工具
@tool
def get_user_info(runtime: ToolRuntime) -> str:
    """Get user information from state."""
    user_id = runtime.state["user_id"]
    return "User is John Smith" if user_id == "user_123" else "Unknown user"

@tool
def set_preference(
    pref_name: str,
    pref_value: str,
    runtime: ToolRuntime
) -> Command:
    """Set user preference in state."""
    return Command(update={
                "preferences": {pref_name: pref_value},
                "messages": [
                    ToolMessage(
                        f"Set {pref_name} to {pref_value}",
                        tool_call_id=runtime.tool_call_id
                    )
                ]
            })

# 定义中间件
@before_model
def trim_messages(state: CustomAgentState, runtime: Runtime) -> dict[str, Any] | None:
    """Keep conversation manageable."""
    messages = state["messages"]
    if len(messages) > 10:
        return {
            "messages": [
                state["messages"][0],  # Keep system message
                *state["messages"][-5:]  # Keep last 5 messages
            ]
        }
    return None

@dynamic_prompt
def personalized_prompt(request: ModelRequest) -> str:
    """Create personalized system prompt."""
    user_name = request.runtime.state.get("user_name", "User")
    return f"You are a helpful assistant. Address the user as {user_name}."

# 配置 Agent
checkpointer = InMemorySaver()

agent = create_agent(
    default_llm,
    tools=[get_user_info, set_preference],
    state_schema=CustomAgentState,
    context_schema=CustomContext,
    middleware=[trim_messages, personalized_prompt],
    checkpointer=checkpointer,
    system_prompt="You are a helpful personal assistant."
)

# 使用示例
config = {"configurable": {"thread_id": "session_123"}}

# 第一次交互
result1 = agent.invoke(
    {
        "messages": [{"role": "user", "content": "Hi, I'm Bob"}],
        "user_id": "user_123"
    },
    config
)
print(f"First response: {result1['messages'][-1].content}")

# 第二次交互 - Agent 记住了名字
result2 = agent.invoke(
    {
        "messages": [{"role": "user", "content": "Who am I?"}],
        "user_id": "user_123"
    },
    config
)
print(f"Second response: {result2['messages'][-1].content}")

# 设置偏好
result3 = agent.invoke(
    {
        "messages": [{"role": "user", "content": "I prefer dark theme"}],
        "user_id": "user_123"
    },
    config
)
print(f"Third response: {result3['messages'][-1].content}")
```

这个完整示例展示了短期记忆系统的核心功能：
1. 基础的 checkpointer 配置
2. 自定义状态模式
3. 多种记忆管理策略（修剪）
4. 从工具中读写状态
5. 动态提示生成
6. 中间件集成

短期记忆是构建能够进行多轮对话的 AI 应用的基础，通过合理的状态管理和消息处理策略，可以创建高效、用户友好的交互体验。
