---
title: Arthas
date: 2026-04-14
last_updated: 2026-04-14
tags: [java, debugging, diagnostics, alibaba]
sources: [["wiki/sources/arthas-1-arthas-ji-ru", "Arthas - 1. Arthas接入"]]
---

# Arthas

Arthas 是阿里巴巴开源的 Java 应用诊断调试工具，允许开发者在线排查问题，无需重启应用，动态跟踪 Java 代码，监控 JVM 状态。

## 核心功能

- 在线诊断问题，不重启 JVM
- 反编译类查看源代码
- 查看方法调用入参和返回值
- 监控方法调用执行时间
- 查看 JVM 状态（内存、GC、线程）
- 支持火焰图分析性能问题
- 版本 4.1.8+ 原生支持 **[[model-context-protocol-mcp|MCP (Model Context Protocol)]]**

## Spring Boot 集成

通过官方 starter 快速集成：

```xml
<dependency>
    <groupId>com.taobao.arthas</groupId>
    <artifactId>arthas-spring-boot-starter</artifactId>
    <version>4.1.8</version>
</dependency>
```

## MCP 支持

Arthas 4.1.8+ 支持 MCP 协议，允许 AI 客户端（如 Claude Code）直接连接 Arthas 服务，自动诊断 Java 应用问题：

```yaml
arthas:
  mcpEndpoint: /mcp
  httpPort: 8563
  password: 123456
```

## 相关链接

- [[entities/alibaba|Alibaba]] - 开发者
- [[model-context-protocol-mcp|Model Context Protocol (MCP)]] - MCP 协议集成
