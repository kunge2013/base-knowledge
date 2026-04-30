---
title: design-system Skill 深度分析
date: 2026-04-30
last_updated: 2026-04-30
tags: [ecc, design-system, skill-analysis, frontend]
sources: [["raw/articles/llm/skills/ecc/1.design-system.md", "1.design-system"]]
---

## 概述

`design-system` 是 ECC (Everything Claude Code) 生态中的一个前端技能，核心功能有三：

1. **从零生成设计系统** — 扫描代码库，自动提取视觉模式，生成一致的设计令牌和文档
2. **视觉审计** — 在 10 个维度上对 UI 进行量化评分，定位具体问题
3. **AI 廉价设计检测** — 识别 AI 生成代码中常见的视觉烂味道

该技能适用于 CSS/Tailwind/styled-components 等主流样式方案。

---

## 使用时机

| 场景           | 说明                       | 推荐模式                      |
| ------------ | ------------------------ | ------------------------- |
| 新项目启动        | 项目需要一套统一的设计规范，从零开始       | Mode 1: Generate          |
| 视觉一致性审计      | 现有项目样式混乱，需要系统性排查         | Mode 2: Visual Audit      |
| 重新设计前        | 改版前需要了解现有的视觉资产和问题        | Mode 1 + Mode 2           |
| UI 有异样但不知原因  | 界面看起来"不对劲"，但无法精确定位       | Mode 2: Visual Audit      |
| 审查样式 PR      | 审核涉及 UI 改动的 Pull Request | Mode 2: Visual Audit      |
| 怀疑 AI 生成的 UI | 项目使用了 AI 生成的前端代码，担心质量    | Mode 3: AI Slop Detection |

---

## 三种模式详解

### Mode 1: Generate Design System（生成设计系统）

#### 做什么

自动扫描项目中的现有样式代码，提取视觉模式，结合竞品分析，生成一套完整的设计系统。

#### 工作流程

```
步骤 1: 扫描样式代码
  └─ 分析 CSS / Tailwind / styled-components 中的现有模式

步骤 2: 提取视觉令牌
  ├─ 颜色（colors）
  ├─ 排版（typography）
  ├─ 间距（spacing）
  ├─ 圆角（border-radius）
  ├─ 阴影（shadows）
  └─ 断点（breakpoints）

步骤 3: 竞品分析
  └─ 通过浏览器 MCP 研究 3 个竞品网站获取灵感

步骤 4: 生成设计令牌
  └─ 输出 JSON 格式 + CSS 自定义属性（Custom Properties）

步骤 5: 生成设计文档
  └─ DESIGN.md，每个决策附带理由说明

步骤 6: 生成预览页面
  └─ 交互式 HTML 预览，自包含无依赖
```

#### 输出产物

| 文件 | 内容 |
|------|------|
| `DESIGN.md` | 设计系统文档，包含每个决策的理由 |
| `design-tokens.json` | 设计令牌的 JSON 定义 |
| `design-preview.html` | 可交互的 HTML 预览页面（无外部依赖） |

#### 使用示例

```bash
# 为 SaaS 应用生成极简风格设计系统，使用大地色系
/design-system generate --style minimal --palette earth-tones
```

#### 适用参数

- `--style`: 设计风格（如 minimal、bold、playful 等）
- `--palette`: 配色方案（如 earth-tones、ocean、monochrome 等）

---

### Mode 2: Visual Audit（视觉审计）

#### 做什么

对 UI 进行 10 个维度的量化评分（每个维度 0-10 分），并给出具体示例和修复建议。

#### 审计维度

| #   | 维度        | 评分重点                                 | 常见问题                      |
| --- | --------- | ------------------------------------ | ------------------------- |
| 1   | **颜色一致性** | 是否使用统一调色板                            | 散落各处的随机 hex 值             |
| 2   | **排版层次**  | h1 > h2 > h3 > body > caption 层级是否清晰 | 标题大小混乱、缺乏对比               |
| 3   | **间距节奏**  | 是否使用一致的间距刻度                          | 随意使用 7px、13px 等非标准值       |
| 4   | **组件一致性** | 相似元素是否看起来一致                          | 同一个按钮在不同页面样式不同            |
| 5   | **响应式行为** | 各断点下是否流畅                             | 特定宽度下布局崩坏                 |
| 6   | **暗色模式**  | 暗色主题是否完整                             | 只有部分组件适配了暗色模式             |
| 7   | **动画**    | 动画是否有明确目的                            | 为动而动、过度使用                 |
| 8   | **可访问性**  | 对比度、焦点状态、触摸目标                        | 对比度不足、缺少 focus 样式         |
| 9   | **信息密度**  | 页面布局是否恰当                             | 信息过载或过于稀疏                 |
| 10  | **打磨程度**  | 细节状态是否完善                             | 缺少 hover、loading、empty 状态 |

#### 每个维度的输出格式

- **评分**（0-10）
- **具体示例**：代码中实际存在问题的位置
- **修复建议**：精确到 `file:line` 的修复方案

#### 使用示例

```bash
# 审计本地开发中的 UI，检查多个页面
/design-system audit --url http://localhost:3000 --pages / /pricing /docs
```

#### 适用参数

- `--url`: 目标网站 URL
- `--pages`: 需要审计的页面路径列表

---

### Mode 3: AI Slop Detection（AI 廉价设计检测）

#### 做什么

识别 AI 生成代码中常见的视觉烂味道（"AI slop"）。这些模式在 AI 生成的前端代码中极其泛滥，会导致产品缺乏个性、视觉廉价。

#### 检测清单

| 烂味道        | 描述                    |
| ---------- | --------------------- |
| 滥用渐变       | 到处都是渐变效果，缺乏节制         |
| 紫蓝默认色      | 所有东西都是紫色到蓝色的渐变        |
| 无目的的玻璃拟态   | 乱用 glassmorphism 卡片效果 |
| 不该圆角的地方    | 所有元素都加了圆角，包括不该加的      |
| 滚动动画过度     | 滚动触发的动画过多过频           |
| 通用 Hero 区域 | 居中标题 + 渐变背景，千篇一律      |
| 无个性的字体     | 默认无衬线字体栈，毫无品牌感        |

#### 使用示例

```bash
# 检查项目中的 AI 廉价设计
/design-system slop-check
```

---

## 实际使用策略

### 新项目从 0 到 1

```
/design-system generate --style <风格> --palette <配色>
```

1. 在脚手架完成后立即运行
2. 生成的 `design-tokens.json` 作为项目样式配置的基础
3. `DESIGN.md` 作为团队设计规范文档
4. `design-preview.html` 用于向团队成员展示设计效果

### 现有项目审计

```
/design-system audit --url <URL> --pages <页面列表>
```

1. 优先审计核心页面（首页、定价页、文档页）
2. 根据 10 个维度评分结果，优先修复低分项
3. 每个问题都有精确的文件和行号，可直接定位

### AI 生成代码质量控制

```
/design-system slop-check
```

1. 在使用 AI 工具（Cursor、v0、Bolt）生成前端代码后立即运行
2. 针对检测到的烂味道逐一修复
3. 作为 CI/CD 流程中的质量门禁（配合人工审核）

### 综合使用流程

对于一次完整的视觉改版或审计，推荐的组合流程：

```
Step 1: slop-check     → 先排除 AI 廉价设计问题
Step 2: visual audit   → 全面了解 10 个维度的现状
Step 3: generate       → 基于审计结果生成新的设计系统
Step 4: 逐页替换样式    → 按 audit 报告的优先级修复
```

---

## 与其他 ECC 技能的协同

| 技能 | 协同方式 |
|------|----------|
| `frontend-design` | design-system 生成规范，frontend-design 基于规范创建具体界面 |
| `code-review` | 审查 PR 时结合 design-system 的规范检查样式一致性 |
| `design-system` 自身 | 可作为 PR 审核的一部分，自动检查样式改动是否符合设计系统 |

---

## 局限性

- **竞品分析依赖浏览器 MCP**：需要配置浏览器 MCP 才能自动研究竞品网站
- **设计决策仍需人工判断**：AI 生成的设计令牌和方案需要设计师或前端负责人审核
- **主要关注视觉层**：不涉及交互设计、信息架构等更广泛的设计范畴
- **评分是启发式的**：10 个维度的评分基于模式匹配，不代表绝对正确

---

## 参考

- 原始来源：[[raw/articles/llm/skills/ecc/1.design-system.md|1.design-system]]
- 相关技能：[[concepts/ecc-skill-index|ECC 技能索引]]（待创建）
