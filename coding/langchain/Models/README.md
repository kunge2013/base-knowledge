# LangChain Models - 代码示例

本目录包含 LangChain Models 官方文档中所有代码示例，基于 LangChain v1.0。

## 概述

Models 是 LangChain 中 LLM 聊天模型的抽象层，提供统一接口给所有主流 LLM 提供商使用。支持多种调用方式（invoke、stream、batch）、工具调用、结构化输出、以及各种高级配置选项。

## 文件说明

| 文件 | 说明 | 主题 |
|------|------|------|
| `llm_config.py` | LLM 配置模板，所有示例共享此配置 | 基础配置 |
| `01_basic_initialization.py` | 使用 `init_chat_model` 基本初始化 | 初始化 |
| `02_model_parameters.py` | 配置模型参数 | 参数配置 |
| `03_invoke_single.py` | 单消息调用 | 调用方式 |
| `04_invoke_conversation_dict.py` | 字典格式对话历史调用 | 对话历史 |
| `05_invoke_conversation_objects.py` | 消息对象格式对话历史调用 | 对话历史 |
| `06_streaming_basic.py` | 基础流式输出 | 流式输出 |
| `07_streaming_accumulate.py` | 累积流式片段 | 流式输出 |
| `08_astream_events.py` | 异步事件流式输出 | 流式输出 |
| `09_batch_basic.py` | 批量并行处理多个请求 | 批量处理 |
| `10_batch_max_concurrency.py` | 批量处理控制最大并发 | 批量处理 |
| `11_batch_as_completed.py` | 流式输出批量结果 | 批量处理 |
| `12_tool_calling_basic.py` | 基础工具调用 | 工具调用 |
| `13_tool_calling_loop.py` | 手动工具调用执行循环 | 工具调用 |
| `14_parallel_tool_calls.py` | 多工具并行调用 | 工具调用 |
| `15_disable_parallel_tool_calls.py` | 禁用并行工具调用 | 工具调用 |
| `16_streaming_tool_calls.py` | 流式工具调用 | 工具调用 |
| `17_accumulate_tool_calls.py` | 累积流式工具调用片段 | 工具调用 |
| `18_force_tool_choice.py` | 强制选择工具 | 工具调用 |
| `19_structured_output_pydantic.py` | Pydantic 结构化输出 | 结构化输出 |
| `20_structured_output_include_raw.py` | 包含原始消息的结构化输出 | 结构化输出 |
| `21_structured_output_nested.py` | 嵌套模式结构化输出 | 结构化输出 |
| `22_model_profile.py` | 获取模型能力配置 | 模型配置 |
| `23_custom_model_profile.py` | 自定义模型能力配置 | 模型配置 |
| `24_update_model_profile.py` | 更新现有模型配置 | 模型配置 |
| `25_multimodal_output.py` | 多模态输出（图像） | 多模态 |
| `26_reasoning_blocks.py` | 获取推理步骤内容块 | 推理 |
| `27_server_side_tool_use.py` | 服务端工具执行 | 工具调用 |
| `28_rate_limiting.py` | 客户端限流 | 高级配置 |
| `29_custom_base_url.py` | 自定义 API 基础 URL | 高级配置 |
| `30_http_proxy.py` | HTTP 代理配置 | 高级配置 |
| `31_log_probs.py` | 获取 token 对数概率 | 高级配置 |
| `32_token_usage_callback.py` | 聚合 token 使用统计 | 监控 |
| `33_invocation_config.py` | 自定义调用配置 | 调用配置 |
| `34_configurable_model.py` | 运行时可配置模型 | 动态配置 |
| `35_configurable_multiple.py` | 多参数可配置模型 | 动态配置 |
| `36_configurable_tool_calling.py` | 可配置模型工具调用 | 动态配置 |

## 核心功能

### 1. 初始化
- `init_chat_model`: 统一初始化入口，自动推断提供商
- 支持所有主流提供商（OpenAI、Anthropic、Azure、Google、AWS 等）

### 2. 调用方式
- **invoke**: 完整响应一次性返回，最简单
- **stream**: 流式逐步返回，提升用户体验
- **batch**: 批量并行处理多个请求

### 3. 工具调用
- 绑定工具到模型，模型决定何时调用
- 支持并行调用多个工具
- 支持流式工具调用
- 支持服务端工具执行

### 4. 结构化输出
- 支持 Pydantic、TypedDict、JSON Schema
- 自动验证，嵌套结构支持
- 可选返回原始消息获取元数据

### 5. 高级特性
- 模型能力 profile（`langchain>=1.1`）
- 多模态输入输出
- 推理内容块访问
- 限流控制
- 自定义 base URL 和代理
- 运行时可配置模型切换

## 环境配置

设置环境变量后运行任何示例：

```bash
export OPENAI_API_KEY="your-api-key"
# 可选：自定义 API 基础 URL
export OPENAI_BASE_URL="your-base-url"

# 安装依赖
pip install -r requirements.txt

# 运行示例
python 12_tool_calling_basic.py
```

更多详细信息请查看 [Models 范式摘要](Chapter_Models_SUMMARY.md)
