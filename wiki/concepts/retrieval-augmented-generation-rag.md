---
title: Retrieval-Augmented Generation (RAG)
date: 2026-04-09
last_updated: 2026-04-09
tags: [concept, llm, retrieval, knowledge-base]
sources: [["wiki/sources/karpathys-llm-wiki-the-complete-guide-to-his-idea-file", "Karpathy's LLM Wiki - The Complete Guide to His Idea File"]]
---

# Retrieval-Augmented Generation (RAG)

**Retrieval-Augmented Generation (RAG，检索增强生成)** 是目前主流的大语言模型知识库方案，在查询时从文档库检索相关片段再由 LLM 合成回答。

## 基本工作流程

传统 RAG 的处理流程：

1. **索引阶段**：用户上传文档集合 → 系统分块 → 计算嵌入 → 存储到向量数据库
2. **查询阶段**：用户提问 → 根据嵌入相似度检索相关块 → 将检索结果放入上下文 → LLM 从头合成回答
3. **每次查询都重复上述过程**，知识不积累

## Karpathy 对 RAG 的批评

在 LLM Wiki 模式中，RAG 是需要改进的基线：

- LLM 每次提问都需要从零开始重新发现、重新合成知识
- 知识不随时间积累
- 一个需要从 5 篇文档综合的微妙问题，每次都需要重新找齐、重新拼接

## 与 LLM Wiki 的对比

| 维度 | 传统 RAG | LLM Wiki |
|------|----------|----------|
| **知识处理时机** | 查询时（每次提问都从头合成） | 摄取时（每个来源处理一次） |
| **交叉引用** | 查询时临时发现 | 预构建并持续维护 |
| **矛盾处理** | 通常不会察觉 | 在摄取过程中标记 |
| **知识积累** | 无积累 — 每次查询从零开始 | 随每个来源复利增长 |
| **输出格式** | 瞬时聊天回复 | 持久化 Markdown 文件 |
| **维护者** | 系统（黑盒） | LLM（透明、可编辑） |

详见 [[concepts/llm-wiki|LLM Wiki]]。

## 相关概念

- [[concepts/llm-wiki|LLM Wiki]] - 对比的新型知识库模式
- [[concepts/embeddings|Embeddings - 嵌入]] - RAG 使用的核心技术
- [[concepts/three-layer-architecture|Three-Layer Architecture - 三层架构]] - LLM Wiki 的架构

## 参考文献

- [[sources/karpathys-llm-wiki-the-complete-guide-to-his-idea-file|Karpathy's LLM Wiki - The Complete Guide to His Idea File]]
