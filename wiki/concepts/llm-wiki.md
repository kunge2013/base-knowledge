---
title: LLM Wiki
date: 2026-04-09
last_updated: 2026-04-09
tags: [concept, knowledge-base, ai-era, llm]
sources: [["wiki/sources/karpathys-llm-wiki-the-complete-guide-to-his-idea-file", "Karpathy's LLM Wiki - The Complete Guide to His Idea File"]]
---

# LLM Wiki

**LLM Wiki** 是 Andrej Karpathy 提出的一种新型知识库模式：由 LLM 代理增量维护的结构化 Markdown 知识库，知识在*摄取时*处理而不是*查询时*处理，实现知识的复利增长。

## 核心理念

LLM Wiki 与传统 RAG 的关键区别：

| 维度 | 传统 RAG | LLM Wiki |
|------|----------|----------|
| **知识处理时机** | 查询时（每次提问都从头合成） | 摄取时（每个来源处理一次） |
| **交叉引用** | 查询时临时发现 | 预构建并持续维护 |
| **矛盾处理** | 通常不会察觉 | 在摄取过程中标记 |
| **知识积累** | 无积累 — 每次查询从零开始 | 随每个来源复利增长 |
| **输出格式** | 瞬时聊天回复 | 持久化 Markdown 文件 |
| **维护者** | 系统（黑盒） | LLM（透明、可编辑） |

## 三层架构

LLM Wiki 采用清晰的**三层架构**分离关注点：

1. **第一层 `raw/`** - 原始来源，不可变，LLM 只读取不修改
2. **第二层 `wiki/`** - LLM 生成的结构化 Markdown 维基，LLM 负责完整维护
3. **第三层 Schema** - `CLAUDE.md` / `AGENTS.md` 规则文件，告诉 LLM 如何维护

详细说明：[[concepts/three-layer-architecture|Three-Layer Architecture - 三层架构]]

## 三大核心操作

### 1. Ingest（摄取）
- 将新源文件放入 `raw/`
- LLM 读取 → 创建源摘要 → 提取概念 → 更新交叉引用 → 更新索引 → 追加日志
- 单个来源可能影响 10-15 个页面，知识整合一次完成

### 2. Query（查询）
- LLM 在整个 wiki 中找到相关页面
- 综合出带引用的答案
- 有价值的答案可保存回 wiki 供未来复用

### 3. Lint（健康检查）
- 定期扫描检查矛盾、过时内容、孤立页面、缺失概念
- 保持 wiki 健康演进

## 优势

- **复利增长**：每添加一个来源都让整个 wiki 更丰富
- **人机分工**：人提供来源和问题，LLM 做所有繁琐的簿记维护
- **透明可编辑**：所有知识都是可读可编辑的 Markdown 文件
- **可追溯**：raw/ 保存原始来源，随时可以核实

## 适用场景

1. **个人知识库** - 追踪目标、健康、心理、自我提升
2. **研究** - 深入研究主题，数周/数月逐步构建不断演进的综合论点
3. **读书** - 逐章归档，为角色、主题、情节构建页面
4. **企业/团队** - 汇集 Slack、会议、文档，维护团队知识
5. **竞争分析、尽职调查、旅行规划、课程笔记** - 任何需要随时间积累知识的场景

## 历史渊源

LLM Wiki 精神上继承了 Vannevar Bush 在 1945 年提出的 **Memex** 构想：个人化的、关联式知识存储。Bush 当年无法解决维护问题，现在 LLM 可以自动完成，让这一愿景成为现实。

## 相关概念

- [[concepts/three-layer-architecture|Three-Layer Architecture - 三层架构]] - LLM Wiki 的核心架构
- [[concepts/idea-file|Idea File - 想法文件]] - LLM Wiki 本身通过 Idea File 分享
- [[concepts/qmd|qmd - Quick Markdown Search]] - 本地 markdown 搜索引擎，可选用于 LLM Wiki
- [[concepts/retrieval-augmented-generation-rag|Retrieval-Augmented Generation (RAG)]] - 对比的传统方案
- [[entities/andrej-karpathy|Andrej Karpathy]] - 提出者

## 参考文献

- [[sources/karpathys-llm-wiki-the-complete-guide-to-his-idea-file|Karpathy's LLM Wiki - The Complete Guide to His Idea File]]
