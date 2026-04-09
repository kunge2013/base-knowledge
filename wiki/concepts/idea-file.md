---
title: Idea File - 想法文件
date: 2026-04-09
last_updated: 2026-04-09
tags: [concept, ai-era, open-ideas]
sources: [["wiki/sources/karpathys-llm-wiki-the-complete-guide-to-his-idea-file", "Karpathy's LLM Wiki - The Complete Guide to His Idea File"]]
---

# Idea File（想法文件）

**Idea File** 是 Andrej Karpathy 在 AI 代理时代提出的一种新分享方式：分享*想法*而不是*代码*，让接收者的 AI 代理根据想法定制化构建实现。

## 定义

> "The idea of the idea file is that in this era of LLM agents, there is less of a point/need of sharing the specific code/app, you just share the idea, then the other person's agent customizes & builds it for your specific needs."

—— Andrej Karpathy

## 核心思想

在 AI 代理时代（人人都可以使用 Claude Code、OpenAI Codex 等），分享*想法*比分享*代码*更有用：

- **想法是可移植的**：适应不同环境（编辑器、操作系统、工具链）
- **代码是特定的**：绑定特定设置，需要大量适配工作
- **AI 代理可以帮你构建**：接收者把想法文件粘贴给 AI 代理，代理会根据你的具体环境定制实现

## 为什么这是进步

传统分享方式：分享 GitHub repo → 接收者克隆 → 配置环境 → 修复依赖 → 适配自己的使用习惯 → 很麻烦

新思路：分享 idea file → 接收者粘贴给 AI 代理 → 代理定制构建 → 直接用

## 例子：LLM Wiki

Karpathy 分享 LLM Wiki 不是分享一个完整的代码项目，而是分享一个 idea file（GitHub Gist）描述：
- 整体架构是什么
- 三层目录结构
- 工作流（Ingest/Query/Lint）
- 页面格式约定

接收者把这个 Gist 粘贴给自己的 AI 代理，代理就会在他的环境中搭建出一个符合他需求的 LLM Wiki，不需要 Karpathy 考虑不同环境适配。

## 本质：开放想法而非开放代码

这是一种新型的"开源"：**开放想法**，而不是开放代码。想法文件故意保持一定抽象，让每个人的 AI 代理可以根据具体需求实例化。正如 Karpathy 所说：

> "The document's only job is to communicate the pattern. Your LLM can figure out the rest."

## 相关概念

- [[concepts/llm-wiki|LLM Wiki]] - LLM Wiki 是 idea file 概念的第一个示例
- [[entities/andrej-karpathy|Andrej Karpathy]] - 提出者

## 参考文献

- [[sources/karpathys-llm-wiki-the-complete-guide-to-his-idea-file|Karpathy's LLM Wiki - The Complete Guide to His Idea File]]
