# 风格预设

`--preset X` 展开为类型 + 风格 + 可选调色板的组合。用户可覆盖任何维度。

## 默认预设

当内容分析未发现强信号时（通用知识文章、混合主题帖子、无明确数据/对比/叙事线索），在步骤 3 Q1 中推荐 **`hand-drawn-edu`** 作为首选。它是温暖、友好的教育信息图默认选项 — 适合大多数文章且通用可读。

## 按类别

### 技术与工程

| --preset | 类型 | 风格 | 调色板 | 最适用于 |
|----------|------|------|--------|----------|
| `tech-explainer` | `infographic` | `blueprint` | — | API 文档、系统指标、技术深入分析 |
| `system-design` | `framework` | `blueprint` | — | 架构图、系统设计 |
| `architecture` | `framework` | `vector-illustration` | — | 组件关系、模块结构 |
| `science-paper` | `infographic` | `scientific` | — | 研究发现、实验结果、学术 |

### 知识与教育

| --preset | 类型 | 风格 | 调色板 | 最适用于 |
|----------|------|------|--------|----------|
| `knowledge-base` | `infographic` | `vector-illustration` | — | 概念解释、教程、怎么做 |
| `saas-guide` | `infographic` | `notion` | — | 产品指南、SaaS 文档、工具演练 |
| `tutorial` | `flowchart` | `vector-illustration` | — | 分步教程、安装指南 |
| `process-flow` | `flowchart` | `notion` | — | 工作流文档、入门引导流程 |
| `warm-knowledge` | `infographic` | `vector-illustration` | `warm` | 产品展示、团队介绍、功能卡片、品牌内容 |
| `edu-visual` | `infographic` | `vector-illustration` | `macaron` | 知识总结、概念解释、教育文章 |
| `hand-drawn-edu` | `infographic` | `sketch-notes` | `macaron` | **默认预设。** 手绘教育信息图 — 暖色奶油纸，黑色线条，粉彩色块。适合单页解释、概念总结、入门引导、通用知识文章 |
| `hand-drawn-edu-flow` | `flowchart` | `sketch-notes` | `macaron` | 手绘流程解释 — 同样温暖教育风格的分步工作流 |
| `hand-drawn-edu-compare` | `comparison` | `sketch-notes` | `macaron` | 温暖教育风格的手绘并排对比 |
| `ink-notes-compare` | `comparison` | `ink-notes` | `mono-ink` | 前后对比文章、传统 vs 新、操作系统风格对比、思维转变叙事 |
| `ink-notes-flow` | `flowchart` | `ink-notes` | `mono-ink` | 专业流程解释、职场管线、手绘技术演练 |
| `ink-notes-framework` | `framework` | `ink-notes` | `mono-ink` | 系统类比、指挥中心图、架构即隐喻、技术宣言 |

### 数据与分析

| --preset | 类型 | 风格 | 调色板 | 最适用于 |
|----------|------|------|--------|----------|
| `data-report` | `infographic` | `editorial` | — | 数据新闻、指标报告、仪表板 |
| `versus` | `comparison` | `vector-illustration` | — | 技术对比、框架竞赛 |
| `business-compare` | `comparison` | `elegant` | — | 产品评估、策略选项 |

### 叙事与创意

| --preset | 类型 | 风格 | 调色板 | 最适用于 |
|----------|------|------|--------|----------|
| `storytelling` | `scene` | `warm` | — | 个人随笔、反思、成长故事 |
| `lifestyle` | `scene` | `watercolor` | — | 旅行、健康、生活方式、创意 |
| `history` | `timeline` | `elegant` | — | 历史概览、里程碑 |
| `evolution` | `timeline` | `warm` | — | 进程叙事、成长旅程 |

### 社论与观点

| --preset | 类型 | 风格 | 调色板 | 最适用于 |
|----------|------|------|--------|----------|
| `opinion-piece` | `scene` | `screen-print` | — | 评论、社论、批评随笔 |
| `editorial-poster` | `comparison` | `screen-print` | — | 辩论、对立观点 |
| `cinematic` | `scene` | `screen-print` | — | 戏剧性叙事、文化随笔 |

## 内容类型 → 预设推荐

在步骤 3 中使用此表，基于步骤 2 的内容分析推荐预设：

| 内容类型（步骤 2） | 首选预设 | 备选 |
|--------------------|----------|------|
| **通用/无强信号** | `hand-drawn-edu` | `edu-visual`, `knowledge-base` |
| 教育/知识 | `hand-drawn-edu` | `edu-visual`, `knowledge-base`, `tutorial` |
| 教程 | `hand-drawn-edu-flow` | `tutorial`, `process-flow`, `hand-drawn-edu` |
| SaaS/产品 | `hand-drawn-edu` | `saas-guide`, `knowledge-base`, `process-flow`, `warm-knowledge` |
| 技术 | `tech-explainer` | `system-design`, `architecture`, `hand-drawn-edu` |
| 方法论/框架 | `system-design` | `architecture`, `process-flow` |
| 数据/指标 | `data-report` | `versus`, `tech-explainer` |
| 对比/评测 | `versus` | `business-compare`, `hand-drawn-edu-compare`, `editorial-poster`, `ink-notes-compare` |
| 宣言/思维转变/专业视觉笔记 | `ink-notes-compare` | `ink-notes-framework`, `ink-notes-flow` |
| 叙事/个人 | `storytelling` | `lifestyle`, `evolution` |
| 观点/社论 | `opinion-piece` | `cinematic`, `editorial-poster` |
| 历史/时间线 | `history` | `evolution` |
| 学术/研究 | `science-paper` | `tech-explainer`, `data-report` |

## 覆盖示例

- `--preset tech-explainer --style notion` = infographic 类型配 notion 风格
- `--preset storytelling --type timeline` = timeline 类型配 warm 风格

显式 `--type`/`--style` 标志始终覆盖预设值。
