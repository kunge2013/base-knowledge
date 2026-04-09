---
title: Karpathy's LLM Wiki - The Complete Guide to His Idea File
date: 2026-04-09
last_updated: 2026-04-09
tags: [article, llm-wiki, karpathy, guide]
sources: [["raw/articles/llm/Karpathy's LLM Wiki The Complete Guide to His Idea File.md", "Karpathy's LLM Wiki - The Complete Guide to His Idea File"]]
---

# Karpathy's LLM Wiki: The Complete Guide to His Idea File

这是 Antigravity.codes 对 Andrej Karpathy 发布的 **LLM Wiki idea file** 的深度解析文章，完整拆解了 Karpathy 的 LLM Wiki 构想，从核心理念、三层架构、核心操作到工具栈和分步实现，提供了一份可直接上手的完整指南。

## 概述

2026 年 4 月，Andrej Karpathy 发布推文提出「将 tokens 花在知识上而非代码」，随后分享了一个 GitHub Gist "idea file" 描述完整的 LLM Wiki 架构。本文是对这个 idea file 的全方位解读，涵盖了每个细节和实现步骤。

## 核心对比：LLM Wiki vs 传统 RAG

| 维度 | 传统 RAG | LLM Wiki |
|------|----------|----------|
| **知识处理时机** | 查询时（每次提问都从头合成） | 摄取时（每个来源处理一次） |
| **交叉引用** | 查询时临时发现 | 预构建并持续维护 |
| **矛盾处理** | 通常不会察觉 | 在摄取过程中标记 |
| **知识积累** | 无积累 — 每次查询从零开始 | 随每个来源复利增长 |
| **输出格式** | 瞬时聊天回复 | 持久化 Markdown 文件 |
| **维护者** | 系统（黑盒） | LLM（透明、可编辑） |

## 三层架构

### 第一层：raw/ - 原始来源
- 你精心挑选的源文件集合（文章、论文、图像、数据）
- **不可变原则**：LLM 只读取，从不修改
- 这是你的事实来源，可随时追溯

### 第二层：wiki/ - LLM 生成的维基
- LLM 完全拥有这一层
- 目录结构：
  - `index.md` - 所有页面的主目录
  - `log.md` - 按时间顺序的活动记录（仅限追加）
  - `overview.md` - 高层综合
  - `concepts/` - 概念页面
  - `entities/` - 实体页面（作者、公司、机构）
  - `sources/` - 来源摘要
  - `comparisons/` - 查询生成的对比分析

### 第三层：Schema - 规则文件
- `CLAUDE.md`（Claude Code）或 `AGENTS.md`（OpenAI Codex）
- 告诉 LLM wiki 的结构、规范和工作流
- 这是让通用 LLM 变成**系统化 wiki 维护者**的关键
- Schema 会随着使用共同演进

## 三大核心操作

### 1. Ingest（摄取）
- 将新源文件放入 `raw/`，让 LLM 处理
- LLM 读取文件 → 讨论要点 → 创建源摘要 → 更新相关概念/实体 → 更新索引 → 追加日志
- 单个来源可能影响 10-15 个 wiki 页面
- 知识整合一次完成，不需要每次查询重做

### 2. Query（查询）
- 对 wiki 提问，LLM 找到相关页面 → 综合出带引用的答案
- **关键点**：有价值的答案可以**保存回 wiki** 作为新页面，这样你的探索也会产生复利

### 3. Lint（健康检查）
- 定期让 LLM 扫描 wiki 健康：
  - 页面之间的矛盾
  - 被新来源取代的过时主张
  - 没有入站链接的孤立页面
  - 已提及但缺少独立页面的概念
  - 缺失的交叉引用
  - 建议需要调查的新问题

## 推荐工具栈

| 工具 | 作用 | 必需 |
|------|------|------|
| Claude Code / OpenAI Codex / OpenCode | LLM 代理，维护 wiki | 是 |
| Obsidian | Markdown 浏览/编辑 | 推荐 |
| Obsidian Web Clipper | 将网页剪藏为 markdown 到 `raw/` | 推荐（网页来源） |
| qmd | 本地 markdown 搜索引擎（BM25 + 向量 + LLM 重排序） | 可选（小规模用 index.md 足够） |
| Marp | 从 wiki 内容生成幻灯片 | 可选 |
| Dataview | 基于 frontmatter 查询 | 可选 |
| Git | 版本控制 | 推荐 |

## 适用场景

1. **个人知识库** - 追踪目标、健康、心理、自我提升
2. **研究** - 深入研究主题，数周/数月逐步构建不断演进的综合论点
3. **读书** - 逐章归档，为角色、主题、情节构建页面
4. **企业/团队** - 汇集 Slack、会议、文档，维护团队知识
5. **竞争分析、尽职调查、旅行规划、课程笔记** - 任何需要随时间积累知识的场景

## 历史渊源

LLM Wiki 精神上继承了 Vannevar Bush 在 1945 年提出的 **Memex** 构想：个人化的、关联式知识存储。Bush 当年无法解决维护问题，现在 LLM 可以自动完成，让这一愿景成为现实。

## 社区贡献

文章整理了 GitHub Gist 讨论区中的社区想法：
- **`.brain` 文件夹模式** - 项目级持久记忆，是 Karpathy 模式的轻量级变种
- **智能体间通过 Gist 通信** - 不同 AI 前端之间用 gist 传递上下文
- **追加-回顾笔记** - LLM Wiki 是这种模式的进化版，自动回顾重组
- **团队协作** - 直接通过 git 共享 repo 即可

## 核心洞见

- **Idea File 新概念** - 在 AI 代理时代，分享**想法**比分享**代码**更有用，代理会为你定制实现
- **复利效应** - wiki 是持久的复利产物，每添加一个来源都让它更丰富
- **人机分工** - 你不需要编写 wiki，LLM 承担所有簿记工作；你负责寻找来源、提出正确问题
- **Karpathy 的类比**：*"Obsidian 是 IDE，LLM 是程序员，Wiki 是代码库"*

## 相关页面

- [[concepts/llm-wiki|LLM Wiki]] - 概念页面
- [[concepts/three-layer-architecture|Three-Layer Architecture - 三层架构]] - LLM Wiki 的三层架构详解
- [[concepts/retrieval-augmented-generation-rag|Retrieval-Augmented Generation (RAG)]] - 对比的传统方案
- [[entities/andrej-karpathy|Andrej Karpathy]] - 提出者
- [[entities/antigravity-codes|Antigravity.codes]] - 本文作者

## 原文链接

- https://antigravity.codes/zh/blog/karpathy-llm-wiki-idea-file
