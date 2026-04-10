# LangChain Agents - 代码示例

本目录包含 LangChain Agents 官方文档中所有代码示例，基于 LangChain v1.0。

## 概述

Agents 将语言模型与工具结合，创建能够推理任务、决定使用哪些工具并迭代地朝着解决方案工作的系统。`create_agent` 提供了生产就绪的代理实现，使用 LangGraph 基于图的运行时。

## 文件说明

| 文件 | 说明 | 主题 |
|------|------|------|
| `llm_config.py` | LLM 配置模板，所有示例共享此配置 | 基础配置 |
| `01_static_model_string.py` | 使用字符串标识符创建静态模型 | 模型配置 |
| `02_static_model_instance.py` | 使用直接模型实例创建静态模型 | 模型配置 |
| `03_dynamic_model_selection.py` | 根据对话复杂度动态选择模型 | 动态模型 |
| `04_static_tools.py` | 使用 `@tool` 装饰器定义静态工具 | 工具定义 |
| `05_dynamic_tools_state_based.py` | 基于状态动态过滤工具 | 动态工具 |
| `06_tool_error_handling.py` | 自定义工具错误处理 | 错误处理 |
| `07_system_prompt_string.py` | 使用字符串配置系统提示词 | 系统提示词 |
| `08_system_prompt_structured.py` | 结构化系统提示词与 Anthropic 缓存 | 系统提示词 |
| `09_dynamic_system_prompt.py` | 基于运行时上下文动态生成系统提示词 | 动态提示词 |
| `10_agent_naming.py` | 为代理设置名称用于子图标识 | 代理命名 |
| `11_basic_invocation.py` | 基本代理调用示例 | 调用方式 |
| `12_structured_output_tool_strategy.py` | 使用 ToolStrategy 结构化输出 | 结构化输出 |
| `13_structured_output_provider_strategy.py` | 使用 ProviderStrategy 结构化输出 | 结构化输出 |
| `14_custom_state_middleware.py` | 通过中间件定义自定义状态 | 自定义状态 |
| `15_custom_state_schema.py` | 通过 state_schema 参数定义自定义状态 | 自定义状态 |
| `16_streaming_example.py` | 流式输出显示中间进度 | 流式输出 |

## 核心组件

### 1. Model（模型）
- **静态模型**: 创建代理时配置一次，保持不变
- **动态模型**: 根据运行时上下文动态选择，支持成本优化和复杂路由逻辑

### 2. Tools（工具）
- **静态工具**: 创建代理时定义，执行期间保持不变
- **动态工具**: 运行时修改可用工具集，基于权限、状态、上下文过滤
- **自定义错误处理**: 使用中间件自定义工具错误处理

### 3. System Prompt（系统提示词）
- 支持字符串、SystemMessage 格式
- 支持动态生成基于上下文

### 4. Advanced Concepts（高级概念）
- **结构化输出**: 两种策略 - ToolStrategy（兼容所有模型）和 ProviderStrategy（使用原生能力）
- **Memory/State**: 自定义状态模式跟踪对话之外的额外信息
- **Streaming**: 流式输出显示中间步骤

## 环境配置

设置环境变量后运行任何示例：

```bash
export OPENAI_API_KEY="your-api-key"
# 可选：自定义 API 基础 URL
export OPENAI_BASE_URL="your-base-url"

# 安装依赖
pip install -r requirements.txt

# 运行示例
python 04_static_tools.py
```

## ReAct 循环工作流程

Agents 遵循 ReAct 模式（Reasoning + Acting）：

1. **推理**: 分析问题决定是否需要调用工具
2. **行动**: 调用一个或多个工具
3. **观察**: 获取工具返回结果
4. **重复**: 继续直到可以给出最终答案

更多详细信息请查看 [Agents 范式摘要](../Chapter_Agents_SUMMARY.md)
