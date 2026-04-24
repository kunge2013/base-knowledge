# Chapter 3: Customize Deep Agents - 自定义深度代理

本章节代码实现了 Deep Agents 的全面自定义配置，涵盖模型、工具、系统提示、中间件、子代理、人工审批、技能、记忆和结构化输出。

## 环境准备

在运行代码之前，请确保已安装以下依赖：

```bash
pip install deepagents tavily-python langchain-openai langchain-anthropic python-dotenv pydantic
```

### API Key 配置

复制 `.env.example` 为 `.env` 并填入你的 API Key：

```bash
export OPENAI_API_KEY="your-openai-api-key"
export ANTHROPIC_API_KEY="your-anthropic-api-key"
export GOOGLE_API_KEY="your-google-api-key"
export TAVILY_API_KEY="your-tavily-api-key"
```

## 文件说明

| 文件名 | 功能描述 |
|--------|----------|
| `llm_config.py` | LLM 配置模块，统一管理语言模型设置 |
| `01_model_configuration.py` | 模型配置：字符串格式 vs 模型实例，连接弹性配置 |
| `02_custom_tools.py` | 自定义工具：Python 函数、@tool 装饰器、Pydantic Schema |
| `03_system_prompt.py` | 系统提示设计：基础、结构化、领域专用、多语言 |
| `04_middleware.py` | 自定义中间件：日志、计时、验证、安全计数 |
| `05_subagents.py` | 子代理配置：专业化子代理、多子代理协作、层次化处理 |
| `06_human_in_the_loop.py` | 人工审批：工具级审批、决策类型、checkpointer |
| `07_skills.py` | 技能配置：从 URL 加载、自定义技能、多技能组合 |
| `08_memory.py` | 记忆文件：AGENTS.md、项目规范、个人偏好、团队规范 |
| `09_structured_output.py` | 结构化输出：Pydantic 模型、嵌套结构、验证约束 |

## 核心配置参数

`create_deep_agent` 的核心配置选项：

```python
create_deep_agent(
    model: str | BaseChatModel | None = None,              # 模型配置
    tools: Sequence[BaseTool | Callable | dict] | None = None,  # 工具列表
    *,
    system_prompt: str | SystemMessage | None = None,      # 系统提示
    middleware: Sequence[AgentMiddleware] = (),            # 中间件
    subagents: Sequence[SubAgent | ...] | None = None,     # 子代理
    skills: list[str] | None = None,                       # 技能
    memory: list[str] | None = None,                       # 记忆文件
    response_format: ResponseFormat | type | dict | None = None,  # 结构化输出
    backend: BackendProtocol | BackendFactory | None = None,      # 后端
    interrupt_on: dict[str, bool | InterruptOnConfig] | None = None,  # 人工审批
    checkpointer: Checkpointer | None = None,              # 检查点（人工审批必需）
) -> CompiledStateGraph
```

## 运行示例

### 1. 模型配置

```bash
python 01_model_configuration.py
```

展示三种模型配置方式：
- `provider:model` 字符串格式
- 模型实例初始化
- 连接弹性配置（重试、超时）

### 2. 自定义工具

```bash
python 02_custom_tools.py
```

演示工具定义的三种方式：
- Python 函数（类型注解自动生成 schema）
- `@tool` 装饰器
- Pydantic Schema

### 3. 系统提示设计

```bash
python 03_system_prompt.py
```

展示系统提示的最佳实践：
- 基础角色定义
- 结构化提示词
- 领域专用提示
- 多语言支持

### 4. 中间件

```bash
python 04_middleware.py
```

演示自定义中间件：
- `@wrap_tool_call` 日志中间件
- `AgentMiddleware` 类（计时、验证）
- 使用 graph state 避免竞态条件

### 5. 子代理

```bash
python 05_subagents.py
```

展示子代理配置：
- 专业化子代理（新闻、技术、金融分析）
- 多子代理协作系统
- 层次化处理（初级/高级研究员）

### 6. 人工审批

```bash
python 06_human_in_the_loop.py
```

演示人工审批流程：
- 工具级审批配置
- 决策类型（approve, edit, reject）
- checkpointer 的必要性

### 7. 技能配置

```bash
python 07_skills.py
```

展示技能配置方式：
- 从 URL 加载技能
- 自定义技能内容
- 多技能组合

### 8. 记忆文件

```bash
python 08_memory.py
```

演示记忆文件使用：
- AGENTS.md 格式
- 项目规范、个人偏好
- 团队规范、领域知识

### 9. 结构化输出

```bash
python 09_structured_output.py
```

展示结构化输出：
- Pydantic 模型定义
- 嵌套结构
- 验证约束

## Agentic 设计模式

本章节涵盖的 Agentic 设计模式：

| 模式 | 文件 | 说明 |
|------|------|------|
| 模型抽象 | 01_model_configuration.py | 解耦模型选择与 agent 逻辑 |
| 工具封装 | 02_custom_tools.py | 外部 API 封装为 agent 工具 |
| 提示工程 | 03_system_prompt.py | 结构化提示引导 agent 行为 |
| 中间件 | 04_middleware.py | 横切关注点（日志、验证、计时） |
| 子代理 | 05_subagents.py | 专业化分工、任务隔离 |
| 人工审批 | 06_human_in_the_loop.py | 敏感操作的人类监督 |
| 技能加载 | 07_skills.py | 按需加载专业知识 |
| 记忆持久化 | 08_memory.py | 跨会话上下文 |
| 结构化输出 | 09_structured_output.py | 类型安全的响应格式 |

## 下一步

- 查看 [Chapter_3_Customize_SUMMARY.md](./Chapter_3_Customize_SUMMARY.md) 获取详细的 Agentic 设计模式摘要
- 继续阅读后续章节了解更多高级用法
