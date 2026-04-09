---
title: Three-Layer Architecture - 三层架构
date: 2026-04-09
last_updated: 2026-04-09
tags: [architecture, llm-wiki, pattern]
sources: [["wiki/sources/karpathys-llm-wiki-the-complete-guide-to-his-idea-file", "Karpathy's LLM Wiki - The Complete Guide to His Idea File"]]
---

# Three-Layer Architecture（三层架构）

**三层架构**是 LLM Wiki 模式的核心架构设计，由 Andrej Karpathy 提出。它将知识库清晰分为三层，每层有明确的职责和不变性约束。

## 架构图

```
┌─────────────────────────────────────────────────┐
│                 Schema (CLAUDE.md)               │  ← 第 3 层：规则告诉 LLM 如何维护
├─────────────────────────────────────────────────┤
│                   wiki/                         │  ← 第 2 层：LLM 生成的结构化 Markdown
│  ┌─────────┐ ┌─────────┐ ┌─────────┐          │
│  │concepts│ │entities│ │ sources│  ...       │
│  └─────────┘ └─────────┘ └─────────┘          │
├─────────────────────────────────────────────────┤
│                   raw/                          │  ← 第 1 层：原始来源，不可变
└─────────────────────────────────────────────────┘
```

## 各层职责

### 第一层：raw/ - 原始来源

**职责**：存储原始源文件，作为事实来源
**性质**：**不可变** —— LLM **只读取，绝不修改**
**内容**：文章、论文、数据文件、图片等原始材料

为什么要 immutable？
- 你始终可以追溯到原始来源核实信息
- 如果 LLM 摘要有误，可以修正
- 原始数据是你的知识基础

### 第二层：wiki/ - LLM 生成的维基

**职责**：存储 LLM 提取、整合后的结构化知识
**性质**：LLM 完全拥有这一层，负责创建、更新、维护
**目录结构**：
- `wiki/index.md` - 所有页面目录
- `wiki/log.md` - 仅限追加的活动日志
- `wiki/overview.md` - 高层综合概述
- `wiki/concepts/` - 概念页面（一个概念一个文件）
- `wiki/entities/` - 实体页面（作者、公司、机构等）
- `wiki/sources/` - 来源摘要页面
- `wiki/queries/` - 保存的查询回答和综合分析

### 第三层：Schema - 规则文件

**职责**：告诉 LLM wiki 的结构规范、工作流约定
**文件名**：
- Claude Code: `CLAUDE.md`
- OpenAI Codex: `AGENTS.md`
- OpenCode: `OPENCODE.md`

**内容**：
- 目录结构定义
- 页面格式要求（YAML frontmatter 字段）
- Ingest/Query/Lint 工作流步骤
- 各种约定（不修改 raw/、更新日期等）

**为什么需要 Schema**：
- 没有 Schema，通用 LLM 不了解你的约定
- Schema 是**持久化记忆**，跨会话保持一致性
- 把通用 LLM 变成**你的专属 wiki 维护者**
- Schema 会随着使用**共同演进**

## 设计原则

| 原则 | 说明 |
|------|------|
| **分离关注点** | 原始数据 vs 合成知识 vs 操作规则 |
| **不可变性** | raw/ 绝不修改，保证可追溯 |
| **LLM 维护** | wiki/ 完全由 LLM 维护，人类不做繁琐簿记 |
| **复利增长** | 每个新来源让整个 wiki 更丰富 |

## 相关概念

- [[concepts/llm-wiki|LLM Wiki]] - 整体模式
- [[entities/andrej-karpathy|Andrej Karpathy]] - 提出者

## 参考文献

- [[sources/karpathys-llm-wiki-the-complete-guide-to-his-idea-file|Karpathy's LLM Wiki - The Complete Guide to His Idea File]]
