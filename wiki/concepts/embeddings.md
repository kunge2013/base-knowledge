---
title: Embeddings - 嵌入
date: 2026-04-09
last_updated: 2026-04-09
tags: [ml-concept, nlp, vector]
sources: [["wiki/sources/agentic-design-patterns-chapter-2-routing", "Agentic Design Patterns - Chapter 2 - Routing"]]
---

# Embeddings（嵌入）

**嵌入**（Embeddings）是将文本、图像等数据转换为低维稠密向量的技术，在 AI 智能体系统中广泛用于语义表示和相似性比较。

## 定义

嵌入是一种数据表示方式，它将离散的符号信息（如词语、句子或整个文档）映射到连续的向量空间中。语义相近的内容在向量空间中距离更近。

## 在智能体路由中的应用

在 [[concepts/routing|路由]] 模式中，基于嵌入的路由是一种重要实现方式：
1. 将输入查询转换为向量嵌入
2. 将此嵌入与预先为每个路由分类计算好的代表嵌入进行比较
3. 查询被路由到嵌入最相似（余弦距离最近）的路由

这种方法特别适合**语义路由**，决策基于输入的含义而不仅仅是关键词匹配。

## 特性

- **语义保留**：语义相似的内容在向量空间中距离较近
- **稠密向量**：通常是几百到几千维的连续向量
- **可比较**：可以使用余弦相似度或欧氏距离计算相似性
- **低维**：相比 one-hot 编码维度大大降低

## 应用场景

- 基于嵌入的语义路由
- 语义搜索
- [[concepts/retrieval-augmented-generation-rag|RAG]]（检索增强生成）
- 文档聚类
- 推荐系统

## 相关概念

- [[concepts/routing|路由]] - 基于嵌入的路由是四种路由方法之一
- [[concepts/retrieval-augmented-generation-rag|RAG]] - RAG 大量使用嵌入技术
- 语义相似性

## 参考文献

- [[sources/agentic-design-patterns-chapter-2-routing|Agentic Design Patterns - Chapter 2 - Routing]]
