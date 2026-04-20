# Chapter 10: Prebuilt Middleware (预置中间件)

本章节包含 LangChain 预置中间件的所有示例代码。每个中间件都有独立的示例文件展示其用法。

## 文件说明

| 文件 | 中间件 | 描述 |
|------|--------|------|
| **llm_config.py** | - | LLM 配置，所有示例共享此配置 |
| **01-summarization.py** | Summarization | 当接近 token 限制时自动总结对话历史，压缩旧上下文同时保留最近消息 |
| **02-human-in-the-loop.py** | Human-in-the-loop | 在工具执行前暂停，等待人工批准、编辑或拒绝工具调用 |
| **03-model-call-limit.py** | Model Call Limit | 限制模型调用次数，防止无限循环或过度成本 |
| **04-tool-call-limit.py** | Tool Call Limit | 控制工具执行次数，可以全局限制或针对特定工具限制 |
| **05-model-fallback.py** | Model Fallback | 当主模型失败时自动回退到备用模型 |
| **06-pii-detection.py** | PII Detection | 检测和处理对话中的个人身份信息(PII)，支持多种处理策略 |
| **07-todo-list.py** | To-do List | 为代理提供任务规划和跟踪能力 |
| **08-llm-tool-selector.py** | LLM Tool Selector | 在调用主模型之前使用 LLM 智能选择相关工具，减少 token 使用 |
| **09-tool-retry.py** | Tool Retry | 使用指数退避自动重试失败的工具调用 |
| **10-model-retry.py** | Model Retry | 使用指数退避自动重试失败的模型调用 |
| **11-llm-tool-emulator.py** | LLM Tool Emulator | 使用 LLM 模拟工具执行，用于测试目的，替代实际工具调用 |
| **12-context-editing.py** | Context Editing | 通过清除旧工具输出来管理对话上下文，当 token 达到限制时 |
| **13-shell-tool.py** | Shell Tool | 向代理暴露持久化 shell 会话以执行命令 |
| **14-file-search.py** | File Search | 提供 Glob 和 Grep 搜索工具，用于文件系统代码探索 |
| **15-filesystem.py** | Filesystem | 为代理提供文件系统工具，用于存储上下文和长期记忆 (ls, read_file, write_file, edit_file) |
| **16-subagent.py** | Subagent | 允许生成子代理，实现上下文隔离，保持主代理上下文窗口清洁 |

## 使用方法

1. 确保已安装依赖：
```bash
pip install -r ../requirements.txt
```

2. 配置环境变量：
   - 设置 `OPENAI_API_KEY` 环境变量
   - 可选设置 `OPENAI_BASE_URL` 自定义 API 地址
   - 可选设置 `model` 和 `temperature` 覆盖默认模型配置

3. 运行任意示例：
```bash
python 01-summarization.py
```

## Provider-agnostic 中间件特性

所有这些中间件都与 LLM 提供商无关，可以与任何 LLM 提供商一起使用：

- **对话管理**: Summarization, Context Editing
- **安全与控制**: Human-in-the-loop, Model Call Limit, Tool Call Limit, PII Detection
- **可靠性**: Model Fallback, Tool Retry, Model Retry
- **性能优化**: LLM Tool Selector
- **功能增强**: To-do List, LLM Tool Emulator
- **系统集成**: Shell Tool, File Search, Filesystem, Subagent
