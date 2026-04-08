---
title: Idea Files
created: 2026-04-08
updated: 2026-04-08
sources: [raw/articles/Karpathy's LLM Wiki The Complete Guide to His Idea File.md]
related: [wiki-vs-rag.md](wiki-vs-rag.md), [three-layer-architecture.md](three-layer-architecture.md)
tags: [idea-files, pattern-sharing, ai-agents, karpathy, knowledge-management]
---

# Idea Files

Idea files are a new format for sharing patterns and architectures in the age of LLM agents—a shift from sharing code to sharing concepts that agents can be customized and built to fit specific needs.

## Definition

Karpathy defines it as: "The idea file concept is that in today's LLM agent era, the significance/necessity of sharing specific code/applications is reduced—instead, you share ideas, and the receiving party's agent can customize and build to fit their specific needs."

## Why Idea Files Matter

**Portability over Implementation:**
- Code is specific: tied to OS, editor, libraries, configuration
- Ideas are portable: agent adapts to user's environment
- Karpathy uses macOS + Obsidian + Claude Code
- You might use Linux + VS Code + OpenAI Codex
- Shared GitHub repo requires fork, modify, debug
- Shared idea file: copy, paste, agent builds custom version

**Abstraction by Design:**
- Idea files are intentionally "somewhat abstract/ambiguous"
- Deliberate vagueness allows multiple valid approaches
- Document's last line: "The sole purpose of this document is to communicate the pattern. The rest is for your LLM to figure out."

## How to Use Idea Files

1. Copy the gist content (complete llm-wiki.md file)
2. Paste into your LLM agent context (Claude Code, Codex, OpenCode)
3. Tell the agent: "Based on this idea file about [your topic], create an LLM Wiki"
4. Agent creates directory structure, writes schema files, guides first ingestion

## New Open Source: Open Ideas

This creates a new form of open source—not open code, but **open ideas** designed to be interpreted and instantiated by AI agents. GitHub gist discussion tabs become collaborative idea spaces where people "tweak ideas or contribute their own."

## Community Extensions

- **.brain folder pattern**: Project-specific memory (index.md, architecture.md, decisions.md) shared between AI sessions
- **Agent-to-agent communication**: Using gists as communication channels between different AI frontends (Claude, Grok)
- **Append-and-Review Note**: Simpler workflow precursor to LLM Wiki—append-only note file with periodic manual review

## Related Concepts

- [Wiki vs RAG](wiki-vs-rag.md) - How idea files enable persistent wiki approach over traditional RAG
- [Three-Layer Architecture](three-layer-architecture.md) - Schema layer defined by idea files

## Sources

- raw/articles/Karpathy's LLM Wiki The Complete Guide to His Idea File.md - Introduced concept of idea files, their purpose, usage patterns, and community extensions
