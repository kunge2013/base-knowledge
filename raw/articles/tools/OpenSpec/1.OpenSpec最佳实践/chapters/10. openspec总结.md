---
title: OpenSpec 最佳实践 - 大白话总结
date: 2026-06-23
last_updated: 2026-06-23
tags: [tools/openspec, summary]
sources: [["raw/articles/tools/OpenSpec/1.OpenSpec最佳实践/chapters/", "OpenSpec 最佳实践全章节"]]
---

# OpenSpec 大白话总结：AI 时代的"先想清楚再动手"开发法

## 一、OpenSpec 到底是啥？

一句话：**OpenSpec 是一个让你在写代码之前，先用 Markdown 文档把需求说清楚的工具。**

### 它解决什么问题？

以前你跟 AI 说"帮我做个登录功能"，AI 可能做出完全不是你想要的东西，然后你来回改，改来改去浪费时间。

OpenSpec 的思路是：**先跟 AI 在文档层面把"做什么、为什么做、怎么验收"达成一致，再动手写代码。**

流程对比：

```
传统流程：  提需求 → 直接写代码 → 测试 → 发现不对 → 重做
OpenSpec：  提需求 → 写规范文档 → AI验证文档 → 按文档写代码 → 验收通过
```

### 四个核心理念

| 理念 | 大白话 |
|------|--------|
| 流动不僵化 | 文档随时能改，不用等"评审通过"才能下一步 |
| 迭代不瀑布 | 一点一点加需求，不是一上来就写完100页文档 |
| 简单不复杂 | 全是 Markdown 文件，不需要学什么复杂工具 |
| 新老项目都行 | 老项目可以逐步引入，新项目可以从一开始就用 |

---

## 二、安装（从零开始配环境）

### 前置条件

只需要一台装了 **Node.js 20.19.0 或以上版本** 的电脑。

检查方法：
```bash
node --version
```

如果版本太低，用 `nvm` 或 `fnm` 升级。

### 安装命令

```bash
# 推荐用 pnpm（速度快）
pnpm add -g @fission-ai/openspec@latest

# 或者用 npm
npm install -g @fission-ai/openspec@latest
```

### 验证装好了没

```bash
openspec --version    # 显示版本号，比如 1.3.1
openspec --help       # 显示所有命令的帮助信息
```

看到版本号就说明装好了。

### 可选：终端自动补全

装完后在终端敲 `openspec` 敲到一半按 Tab 键能自动补全命令。需要的话运行：
```bash
openspec completion --help
```

---

## 三、项目初始化（在你的项目里引入 OpenSpec）

### 一条命令搞定

```bash
cd your-project        # 进入你的项目目录
openspec init           # 执行初始化
```

### 初始化时干了啥？

1. **问你用啥 AI 工具**：它会弹窗让你选 Claude Code、Cursor、GitHub Copilot 等（空格键选择，回车确认）
2. **创建目录结构**：生成 `openspec/` 工作目录
3. **配置 AI 技能文件**：自动把斜杠命令和技能文件放到对应 AI 工具的目录下

### 不想交互？可以用非交互模式

```bash
# 不配置任何 AI 工具（只创建目录结构）
openspec init --tools none

# 配置所有 AI 工具
openspec init --tools all

# 只配置特定工具
openspec init --tools claude,cursor
```

### 初始化后长这样

```
your-project/
├── openspec/
│   ├── config.yaml      # 项目配置（技术栈、规则等）
│   ├── changes/         # 变更提案目录（每个功能一个文件夹）
│   └── specs/           # 主规范目录（已归档的规范放这里）
├── .claude/             # 如果选了 Claude Code
│   ├── commands/opsx/   # 斜杠命令文件
│   └── skills/          # AI 技能文件
└── ... (你项目原来的文件)
```

### config.yaml 是啥？

这是你的**项目说明书**，告诉 AI 你用的技术栈、约定规则等。AI 每次规划时都会读这个文件。

```yaml
schema: spec-driven

context: |
  Tech stack: TypeScript, React, Node.js
  Testing: Jest
  We maintain backwards compatibility

rules:
  proposal:
    - Include rollback plan for risky changes
  specs:
    - Use Given/When/Then format for scenarios
```

---

## 四、创建变更提案（每个功能/改动都是一个"变更"）

### 核心概念：什么是"变更"？

在 OpenSpec 里，**所有事情都以"变更"为单位**：
- 开发一个新功能 → 一个变更
- 修一个 Bug → 一个变更
- 做一次重构 → 一个变更

### 创建变更：两种方式

**方式一：一句话生成所有文档（推荐）**

在 AI 工具（如 Claude Code）的对话里输入：
```
/opsx:propose "实现用户登录功能"
```

AI 会自动：
1. 取个名字：`user-login`
2. 创建目录：`openspec/changes/user-login/`
3. 生成所有文档：proposal.md、design.md、specs/、tasks.md

**方式二：只创建空目录**

```bash
openspec new change user-login
```

只创建空目录，不生成文档，适合想一步步自己写的场景。

### 变更目录里都有啥？

```
openspec/changes/user-login/
├── .openspec.yaml     # AI 自动管理的元数据（别手动改）
├── proposal.md        # 【必填】为什么要做？做什么？
├── design.md          # 【推荐】技术方案怎么写？
├── tasks.md           # 【推荐】任务清单，按里程碑列出来
└── specs/             # 【必填】具体需求规范
    └── user-auth/
        └── spec.md    # 能力规范（用 Given/When/Then 格式）
```

### 变更的完整生命周期

```
提案(propose) → 写规范 → 验证(validate) → 实现(apply) → 归档(archive)
```

1. **提案**：`/opsx:propose "xxx"` 一步生成所有文档骨架
2. **写规范**：编辑 proposal.md 和 specs/ 里的内容
3. **验证**：`openspec validate user-login` 检查格式对不对
4. **实现**：`/opsx:apply` 让 AI 按 tasks.md 一步步写代码
5. **归档**：`/opsx:archive` 把规范合并到主目录，清理临时文件夹

---

## 五、文档怎么写？（格式规范）

### 5.1 proposal.md — 提案文档

**必须包含两个章节**（验证器会强制检查）：

```markdown
## Why

### Background（背景）
当前系统是裸奔的，谁都能访问所有数据。

### Problem Statement（问题描述）
需要增加用户认证机制，支持用户名密码和第三方登录。

### Alternatives Considered（备选方案）
1. 自建认证 — 可控但成本高
2. 用 Auth0 — 好用但贵
3. 用 Keycloak — 开源免费 ✓ 选这个

## What Changes

### New Resources Added
- 新增 User 模型
- 新增 Session 管理模块

### New Capabilities
- 用户注册和登录
- 第三方 OAuth 登录
- 会话管理和安全退出
```

> **重点**：`## Why` 和 `## What Changes` 这两个标题大小写必须完全一致，一个字都不能差。

### 5.2 spec.md — 能力规范（最重要的部分）

每个能力一个文件夹，每个 spec.md 的格式是：

```markdown
# 用户认证

## ADDED Requirements

### Requirement: 用户名密码登录

系统应支持用户使用用户名和密码登录。

**Priority**: P0 (Critical)
**Rationale**: 最基础的认证方式。

#### Scenario: 正确密码登录成功

Given 用户已注册，账号为 test@example.com
When 用户使用正确的密码登录
Then 登录成功，返回会话令牌

#### Scenario: 错误密码登录失败

Given 用户已注册，账号为 test@example.com
When 用户使用错误的密码登录
Then 登录失败，返回"账号或密码错误"提示
```

#### 必须掌握的格式要点

| 元素      | 正确写法                       | 常见错误                                                   |
| ------- | -------------------------- | ------------------------------------------------------ |
| Delta 头 | `## ADDED Requirements`    | 忘了写这个头                                                 |
| 需求标题    | `### Requirement: 用户名密码登录` | `### REQ-001: ...` 或 `### 用户名密码登录`（少了"Requirement:"前缀） |
| 场景标题    | `#### Scenario: 正确密码登录成功`  | `#### Scenario: 登录`（太模糊）                               |
| 场景内容    | Given/When/Then 格式         | 写自然语言描述，不用 Gherkin                                     |

#### 什么是 Delta Header？

"Delta" 就是**"变更量"的意思。**Delta Header 就是告诉 OpenSpec 工具：**这段文档描述的是哪种类型的变更**。

打个比方，你写了一篇规范文档，OpenSpec 需要知道：
- 这些需求是**全新加的**？
- 还是**在旧需求基础上改的**？
- 还是**要删掉的旧需求**？

Delta Header 就干这件事。它就是一个 Markdown 二级标题，有三种写法：

| Header | 含义 | 大白话 |
|--------|------|--------|
| `## ADDED Requirements` | 新增需求 | "这些都是新加的功能" |
| `## MODIFIED Requirements` | 修改已有需求 | "这些需求以前有，我现在要改" |
| `## REMOVED Requirements` | 删除/废弃需求 | "这些需求不要了，废掉" |

**为什么叫 Delta？** 因为每次变更（Change）本质上都是在给系统规范做"增量更新"（delta），而不是从头重写。Delta Header 就是标记这个"增量"的类型。

#### Delta Header 怎么选？

| Header | 什么时候用 |
|--------|-----------|
| `## ADDED Requirements` | 新增的能力或需求（最常用） |
| `## MODIFIED Requirements` | 修改了已有规范里的需求 |
| `## REMOVED Requirements` | 废弃或删除某个需求 |

### 5.3 Gherkin 格式 — Given/When/Then 咋写？

这是"验收场景"的标准写法：

| 关键字   | 含义           | 例子                 |
| ----- | ------------ | ------------------ |
| Given | 前提条件，一开始系统啥样 | `Given 用户已登录`      |
| When  | 触发动作，做了啥操作   | `When 用户点击"提交订单"`  |
| Then  | 预期结果，应该发生啥   | `Then 订单状态变为"待支付"` |
| And   | 连接多个条件/结果    | `And 用户收到确认邮件`     |

**好的例子：**
```
Scenario: 使用信用卡支付订单

Given 用户已登录系统
And 购物车中有 2 件商品，总价 299 元
And 用户已绑定信用卡
When 用户选择"信用卡支付"并确认
Then 订单创建成功
And 从信用卡扣除 299 元
And 库存减少 2 件
```

**烂的例子：**
```
Scenario: 支付
Given 系统
When 支付
Then 成功
```
问题：太模糊，没法验证。

---

## 六、验证文档（检查格式对不对）

### 验证命令

```bash
openspec validate user-login
```

输出 `Change 'user-login' is valid` 就说明格式没问题了。

### 三个最常见的错误

**错误1：找不到任何 Delta**

原因：specs/ 目录下没有能力文件夹，或者 spec.md 里没有 Delta Header。

解决：确保结构是 `specs/能力名/spec.md`，且 spec.md 里有 `## ADDED Requirements`。

**错误2：需求条目解析失败**

原因：需求标题格式写错了。

```
❌ ### REQ-001: GPU Discovery
❌ ### GPU Discovery
✅ ### Requirement: GPU 自动发现
```

**错误3：缺少场景块**

原因：每个需求下面至少得有一个 `#### Scenario:` 块。

```
❌ 只写了需求描述，没写场景
✅ 每个需求都配上至少一个 Given/When/Then 场景
```

### 调试小技巧

```bash
# 查看变更的完成进度
openspec status --change user-login

# 查看 AI 是怎么解析你的文档的（JSON 格式）
openspec show user-login --json --deltas-only
```

---

## 七、常用命令速查

| 场景           | 命令                                  |
| ------------ | ----------------------------------- |
| 初始化项目        | `openspec init --tools claude`      |
| 创建变更（一步生成文档） | 在 AI 里用 `/opsx:propose "xxx"`       |
| 仅创建空目录       | `openspec new change add-auth`      |
| 验证格式         | `openspec validate add-auth`        |
| 查看进度         | `openspec status --change add-auth` |
| 列出所有变更       | `openspec list --changes`           |
| 归档完成的变更      | `openspec archive add-auth`         |
| 更新 AI 技能文件   | `openspec update`                   |
| 查看版本号        | `openspec --version`                |

### AI 斜杠命令速查（默认 4 个）

| 命令 | 作用 |
|------|------|
| `/opsx:propose "描述"` | 一步创建变更 + 生成所有文档 |
| `/opsx:explore` | 探索模式，先看看代码库，不写代码 |
| `/opsx:apply` | 按 tasks.md 一步步实现代码 |
| `/opsx:archive` | 完成并归档当前变更 |

### 扩展命令（需要额外开启）

| 命令 | 作用 |
|------|------|
| `/opsx:new` | 只创建空目录 |
| `/opsx:continue` | 按顺序逐步生成文档 |
| `/opsx:ff` | 快进一步生成所有文档 |
| `/opsx:verify` | 检查代码是否符合规范 |
| `/opsx:onboard` | 新手 15 分钟引导教程 |

---

## 八、最佳实践（实战经验总结）

### 8.1 写提案：想清楚再说

- **先写 Why，再写 What**：先说服别人为什么需要做，再说具体做什么
- **保持简洁**：proposal.md 是高层概述，细节放 specs/ 里
- **明确范围**：说清楚哪些做（In Scope），哪些不做（Out of Scope）
- **❌ 不要**：写"优化性能"这种模糊话，要说"将页面加载时间从 3s 降到 1s 以内"

### 8.2 写规范：模块化、粒度适中

- **一个能力一个文件夹**，别把不相关的东西塞到一个 spec.md 里
- **需求粒度适中**：每个需求应该是一个可测试的功能点
- **标注优先级**：P0（必须做）、P1（应该做）、P2（可以做）
- **写 Rationale**：解释为什么需要这个需求

### 8.3 与 AI 协作的技巧

1. **先探索后提案**：不确定时先 `/opsx:explore` 看看，想清楚了再 `/opsx:propose`
2. **定期清空对话**：开始实现前清空上下文，避免 AI 被旧信息干扰
3. **增量迭代**：做完一个需求就验证，再做下一个
4. **别一股脑丢指令**：用 `/opsx:apply` 让 AI 按任务清单逐步实现，别直接说"帮我写完"

### 8.4 老项目引入 OpenSpec

- **从小处入手**：选一个小的、相对独立的新功能开始用
- **别试图补全所有历史代码的规范**：那是不可能的任务
- **逐步建立体系**：先尝到甜头，再慢慢推广

### 8.5 团队协作

- **PR 审查时检查文档**：Why 清不清晰？Scenario 够不够具体？
- **需求变了先改文档再改代码**：文档是契约，是唯一的真相来源
- **完成就归档**：用 `openspec archive` 把规范合并到主目录

---

## 九、FAQ 精选

**Q：OpenSpec 和 Swagger/OpenAPI 有啥区别？**

A：OpenSpec 管的是"业务需求和验收标准"（做什么），OpenAPI 管的是"接口定义"（怎么调用）。先用 OpenSpec 定义需求，再用 OpenAPI 定义接口细节，两者配合使用。

**Q：老项目怎么引入？**

A：三步走：`openspec init --tools none` → 为下一个新功能创建变更 → 逐步推广。不用推翻重来。

**Q：AI 不遵循规范怎么办？**

A：① 运行 `openspec update` 刷新 AI 技能文件 ② 在 config.yaml 的 rules 里加硬性约束 ③ 用 `/opsx:apply` 让 AI 严格按任务清单执行。

**Q：BDD 场景（Given/When/Then）是 AI 写还是人写？**

A：**人主导核心逻辑，AI 辅助补全**。核心业务场景必须人写或人审，AI 适合做格式转换和边缘场景推导。别完全让 AI 从零生成 Spec。

**Q：多个变更能同时进行吗？**

A：可以，每个变更是独立文件夹互不干扰。但建议小步快跑，完成一个归档一个，减少合并冲突。

---

## 十、一图总结

```
┌─────────────────────────────────────────────────┐
│                   OpenSpec 工作流                   │
├─────────────────────────────────────────────────┤
│                                                 │
│  1. 安装     npm install -g @fission-ai/openspec  │
│  2. 初始化   openspec init --tools claude         │
│  3. 提案     /opsx:propose "做xxx"                │
│  4. 写规范   编辑 proposal.md + specs/            │
│  5. 验证     openspec validate xxx                │
│  6. 实现     /opsx:apply                          │
│  7. 归档     /opsx:archive                        │
│                                                 │
│  核心思想：先想清楚（文档），再动手干（代码）           │
│  关键格式：## Why + ## What + ## ADDED Requirements│
│            + ### Requirement: xxx                 │
│            + #### Scenario: xxx                   │
│            + Given/When/Then                      │
│                                                 │
└─────────────────────────────────────────────────┘
```

---

## 常用资源链接

| 资源 | 地址 |
|------|------|
| GitHub | https://github.com/Fission-AI/OpenSpec |
| 快速入门 | https://openspec.pro/getting-started/ |
| npm 包 | https://www.npmjs.com/package/@fission-ai/openspec |
