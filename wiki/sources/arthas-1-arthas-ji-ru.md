---
title: Arthas - 1. Arthas接入
date: 2026-04-14
last_updated: 2026-04-14
tags: [arthas, java, debugging, mcp]
sources: [["raw/articles/arthas/1. arthas接入.md", "Arthas 接入笔记"]]
---

# Arthas - 1. Arthas接入

这是一篇实操笔记，记录了如何在 Spring Boot 应用中接入 Alibaba Arthas 并启用 MCP (Model Context Protocol) 支持。

## 关键内容

### Spring Boot 集成

使用官方提供的 `arthas-spring-boot-starter` 启动器：

```xml
<dependency>
    <groupId>com.taobao.arthas</groupId>
    <artifactId>arthas-spring-boot-starter</artifactId>
    <version>4.1.8</version>
</dependency>
```

**版本说明**：`4.1.8` 版本原生支持 MCP。

### 配置示例

```yaml
arthas:
  mcpEndpoint: /mcp
  httpPort: 8563
  password: 123456
```

### Web UI 访问

访问地址：`http://localhost:8563/ui/#/dashboard`

### MCP 集成

可以在 Claude 或其他 MCP 客户端中通过 HTTP 连接到 Arthas：

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

## 要点总结

- Arthas 是一款 Java 应用诊断调试工具
- 版本 4.1.8+ 支持 MCP 协议，可以让 AI 客户端直接连接诊断 Java 应用
- 通过 MCP，AI 可以直接查看 JVM 状态、线程、内存信息，执行诊断命令
