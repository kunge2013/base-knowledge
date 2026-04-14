---
title: Model Context Protocol (MCP)
date: 2026-04-14
last_updated: 2026-04-14
tags: [protocol, ai, model-context, tools]
sources: [["wiki/sources/arthas-1-arthas-ji-ru", "Arthas - 1. Arthas接入"]]
---

# Model Context Protocol (MCP)

Model Context Protocol (MCP) 是一种开放协议，允许 AI 模型客户端与外部服务/工具进行标准化通信，使 AI 能够安全地调用外部工具获取上下文信息。

## 协议特点

- 标准化的工具调用接口
- 支持多种传输方式（stdio、streamableHTTP 等）
- 身份验证支持
- 可发现工具列表和功能描述
- 双向流式通信

## 使用场景

- AI 开发环境集成（Claude Code、VSCode 等）
- 让 AI 能够直接访问本地服务和工具
- Arthas 集成：AI 可以直接读取 Java 应用的 JVM 状态、线程信息、内存使用情况进行自动诊断

## 配置示例

Arthas MCP 服务器配置：

```json
{
  "mcpServers": {
    "arthas-mcp": {
      "type": "streamableHttp",
      "url": "http://localhost:8563/mcp",
      "headers": {
        "Authorization": "Bearer 123456"
      }
    }
  }
}
```

## 传输方式

- **stdio**: 标准输入输出，适用于本地进程间通信
- **streamableHttp**: 可流式 HTTP 传输，适用于网络服务

## 相关链接

- [[concepts/arthas|Arthas]] - 支持 MCP 的 Java 诊断工具
