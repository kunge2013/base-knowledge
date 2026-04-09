---
title: qmd - Quick Markdown Search
date: 2026-04-09
last_updated: 2026-04-09
tags: [tool, search, markdown]
sources: [["wiki/sources/karpathys-llm-wiki-the-complete-guide-to-his-idea-file", "Karpathy's LLM Wiki - The Complete Guide to His Idea File"]]
---

# qmd (Quick Markdown Search)

**qmd** 是由 Tobi Lutke (Shopify CEO) 开发的本地 markdown 文件搜索引擎，专为 LLM Wiki 这类 markdown 知识库设计。

## 特性

qmd 混合三种搜索策略，全部在本地设备运行，不需要云端 API：

1. **BM25 全文搜索** —— 关键词匹配（快速精确）
2. **向量语义搜索** —— 基于含义匹配（找到相关概念）
3. **LLM 重排序** —— 由 LLM 对结果评分，选出最相关的（最高质量）

## 为什么在 LLM Wiki 中需要 qmd

- 小规模 wiki（几百页）：维护良好的 `index.md` 足够用
- 当 wiki 增长超过 index.md 能在单个上下文放下的规模，qmd 就变得非常有用
- qmd 让你能在整个 wiki 中搜索关键词和语义，找到相关页面

## 基本使用

```bash
# 全局安装
npm install -g @tobilu/qmd

# 添加 wiki 集合
qmd collection add ./wiki --name my-research

# 关键词搜索（BM25）
qmd search "mixture of experts routing"

# 语义搜索（向量）
qmd vsearch "how do sparse models handle efficiency"

# 混合搜索 + LLM 重排序（最佳质量）
qmd query "what are the tradeoffs of top-k vs expert-choice routing"

# JSON 输出，供 LLM 代理消费
qmd query "scaling laws" --json

# 作为 MCP 服务器启动，供 Claude Code 等工具使用
qmd mcp
```

## 优势

- **本地运行**：使用 node-llama-cpp + GGUF 模型，数据不离开你的机器
- **混合策略**：结合了关键词的精确性和语义搜索的相关性
- **MCP 支持**：可以作为 MCP 服务器供 Claude Code 等 LLM 代理原生使用

## 作者

- **Tobi Lutke** — Shopify CEO，构建了这个工具专门用于 markdown 知识库搜索

## 相关概念

- [[concepts/llm-wiki|LLM Wiki]] - qmd 是 LLM Wiki 推荐的可选搜索工具
- [[concepts/knowledge-accumulation|Knowledge Accumulation]]

## 参考文献

- [[sources/karpathys-llm-wiki-the-complete-guide-to-his-idea-file|Karpathy's LLM Wiki - The Complete Guide to His Idea File]]
- GitHub: https://github.com/tobi/qmd
