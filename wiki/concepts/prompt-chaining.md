---
title: Prompt Chaining - 提示词链
date: 2026-04-09
last_updated: 2026-04-09
tags: [agentic-pattern, prompt-engineering, fundamental-pattern]
sources: [["wiki/sources/agentic-design-patterns-chapter-1-prompt-chaining", "Agentic Design Patterns - Chapter 1 - Prompt Chaining"]]
---

# Prompt Chaining（提示词链）

**提示词链**（也称为**管道模式**，Pipeline Pattern）是构建智能体系统最基础的设计模式，它采用分而治之的策略，将复杂问题分解为一系列顺序执行的子问题。

## 定义

提示词链是一种多步骤 LLM 交互范式：不再要求 LLM 在单一的整体化步骤中解决复杂问题，而是将问题分解为一系列更小、更易管理的子问题，每个子问题通过专门设计的提示词单独处理，一个提示词的输出会作为输入传递给链中的下一个提示词。

## 核心思想

通过顺序分解，每一步只专注于完成一个特定的子任务，从而减少 LLM 的认知负荷，提高输出的准确性和可靠性。前一步的输出为后一步提供上下文，形成依赖链，使 LLM 能够在先前工作的基础上逐步构建最终解决方案。

## 解决的问题

单一提示词处理复杂任务时会出现以下问题：

| 问题 | 描述 |
|------|------|
| **指令忽略** | 部分提示内容被模型忽视 |
| **上下文偏离** | 模型失去对初始上下文的追踪 |
| **错误传播** | 早期错误被后续步骤放大 |
| **上下文窗口不足** | 单一提示词需要容纳所有信息，容易超出窗口限制 |
| **幻觉增加** | 认知负荷增加导致生成更多错误信息 |

## 关键原则

1. **分而治之**：将复杂任务分解为多个聚焦的子步骤
2. **顺序依赖**：前一步输出作为后一步输入，建立清晰的依赖关系
3. **模块化**：每个步骤可以独立设计、优化和调试
4. **结构化输出**：使用 JSON/XML 等格式确保步骤间数据传递的准确性
5. **可扩展性**：支持在步骤之间插入外部工具调用

## 结构化输出的重要性

提示词链的可靠性高度依赖于步骤之间传递的数据完整性。如果输出不明确或格式不佳，后续提示词会因错误输入而失败。使用结构化输出：
- 确保数据机器可读
- 可以精确解析
- 消除歧义
- 减少自然语言解释导致的错误

**示例**：
```json
{
  "trends": [
    {
      "trend_name": "AI-Powered Personalization",
      "supporting_data": "73% of consumers prefer..."
    }
  ]
}
```

## 典型应用场景

### 1. 信息处理工作流
```
提取文本 → 总结 → 提取实体 → 搜索知识库 → 生成报告
```
应用领域：自动化内容分析、AI 研究助手、复杂报告生成

### 2. 复杂查询回答
```
分解子问题 → 分别研究每个子问题 → 综合信息 → 给出答案
```
适用场景：需要多步推理或多源信息集成的问题

### 3. 数据提取和转换
```
尝试提取 → 验证结果 → （条件性）修正错误 → 重复直至正确
```
适用场景：从非结构化文本（发票、表单、邮件）提取结构化数据

### 4. 内容生成工作流
```
构思主题 → 生成大纲 → 分段起草 → 审查完善
```
适用场景：创意写作、技术文档创作等

### 5. 有状态对话智能体
```
识别意图 → 更新对话状态 → 基于状态生成响应 → 重复
```
作用：维护多轮对话的上下文连贯性

### 6. 代码生成和完善
```
理解需求 → 生成伪代码/大纲 → 编写代码 → 审查错误 → 完善文档
```
应用领域：AI 辅助软件开发

### 7. 多模态多步推理
分解不同模态任务，逐步处理和整合

## 何时使用

当任务符合以下特征时，应考虑使用提示词链：
- ✅ 任务对于单个提示词过于复杂
- ✅ 涉及多个不同的处理阶段
- ✅ 需要在步骤之间与外部工具交互
- ✅ 构建需要执行多步推理并维护状态的智能体系统

## 代码示例（LangChain LCEL）

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = ChatOpenAI(temperature=0)

# 提示词 1：提取信息
prompt_extract = ChatPromptTemplate.from_template(
    "从以下文本中提取技术规格：\n\n{text_input}"
)

# 提示词 2：转换为 JSON
prompt_transform = ChatPromptTemplate.from_template(
    "将以下规格转换为 JSON 对象：\n\n{specifications}"
)

# 使用 LCEL 构建链
extraction_chain = prompt_extract | llm | StrOutputParser()
full_chain = (
    {"specifications": extraction_chain}
    | prompt_transform | llm | StrOutputParser()
)

# 执行
result = full_chain.invoke({
    "text_input": "新款笔记本配备 3.5 GHz 八核处理器、16GB 内存和 1TB 固态硬盘。"
})
```

## 相关框架

- [[concepts/langchain|LangChain]] - 提供 LCEL 表达式语言方便构建链
- [[concepts/langgraph|LangGraph]] - 扩展支持状态化和循环计算
- Google Agent Development Kit (ADK) - Google 智能体开发框架
- [[concepts/crew-ai|Crew AI]] - 多智能体任务编排框架

## 相关概念

- [[concepts/prompt-engineering|提示词工程]]
- [[concepts/context-engineering|上下文工程]]
- [[concepts/agentic-design-patterns|智能体设计模式]]
- [[concepts/pipeline-pattern|管道模式]]
- [[concepts/routing|路由]] - 下一个基础模式，添加条件动态决策
- [[concepts/ai-agents|AI 智能体]] - 提示词链是构建 AI 智能体的基础模式

## 参考文献

- [[sources/agentic-design-patterns-chapter-1-prompt-chaining|Agentic Design Patterns - Chapter 1 - Prompt Chaining]]
