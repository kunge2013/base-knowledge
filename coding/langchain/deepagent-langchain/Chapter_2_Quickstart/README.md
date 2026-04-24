# Chapter 2: Quickstart - Deep Agents

本章节代码实现了 Deep Agents 的快速入门，展示如何创建第一个具有规划、文件系统工具和子代理能力的深度代理。

## 环境准备

在运行代码之前，请确保已安装以下依赖：

```bash
pip install deepagents tavily-python langchain-openai python-dotenv rich
```

### API Key 配置

复制 `.env.example` 为 `.env` 并填入你的 API Key：

```bash
export GOOGLE_API_KEY="your-api-key"
export TAVILY_API_KEY="your-tavily-api-key"
# 如果使用 OpenAI
export OPENAI_API_KEY="your-openai-api-key"
```

## 文件说明

| 文件名 | 功能描述 |
|--------|----------|
| `llm_config.py` | LLM 配置模块，统一管理语言模型设置 |
| `01_search_tool.py` | 使用 Tavily API 创建互联网搜索工具 |
| `02_create_agent.py` | 创建具有研究能力的 Deep Agent |
| `03_invoke_agent.py` | 运行代理的三种方式：基础调用、流式输出、事件流 |

## 运行示例

### 1. 测试搜索工具

```bash
python 01_search_tool.py
```

输出搜索结果，验证 Tavily API 配置正确。

### 2. 创建代理

```bash
python 02_create_agent.py
```

创建 Deep Agent 实例，展示代理的五大核心能力。

### 3. 运行代理

```bash
python 03_invoke_agent.py
```

提供三种调用方式：
- **基础调用**: 简单直接，获取最终结果
- **流式调用**: 实时显示输出
- **事件流**: 调试模式，显示工具调用和子代理活动

## 核心概念

### 1. 工具定义

使用类型注解自动生成工具 schema：

```python
def internet_search(
    query: str,
    max_results: int = 5,
    topic: Literal["general", "news", "finance"] = "general",
    include_raw_content: bool = False,
):
    """Run an internet search"""
```

### 2. 系统提示设计

系统提示用于引导代理行为：

```python
research_instructions = """You are an expert researcher..."""
```

### 3. 代理创建

```python
agent = create_deep_agent(
    model="google_genai:gemini-3.1-pro-preview",
    tools=[internet_search],
    system_prompt=research_instructions,
)
```

### 4. 代理调用

```python
# 基础调用
result = agent.invoke({"messages": [{"role": "user", "content": "What is LangChain?"}]})

# 流式输出
for chunk in agent.stream({...}):
    ...
```

## 下一步

- 查看 [Chapter_2_Quickstart_SUMMARY.md](./Chapter_2_Quickstart_SUMMARY.md) 获取详细的 Agentic 设计模式摘要
- 继续阅读 Chapter 3 了解如何自定义代理
