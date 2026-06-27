---
name: first-time-setup
description: baoyu-article-illustrator 偏好设置首次设置流程
---

# 首次设置

## 概述

当未找到 EXTEND.md 时，引导用户完成偏好设置。

**⛔ 阻塞操作**：此设置必须在任何其他工作流步骤之前完成。不要：
- 询问参考图像
- 询问内容/文章
- 询问类型或风格偏好
- 继续内容分析

仅提出此设置流程中的问题，保存 EXTEND.md，然后继续。

## 设置流程

```
未找到 EXTEND.md
        │
        ▼
┌─────────────────────┐
│ AskUserQuestion     │
│（所有问题）          │
└─────────────────────┘
        │
        ▼
┌─────────────────────┐
│ 创建 EXTEND.md      │
└─────────────────────┘
        │
        ▼
    继续到步骤 1
```

## 问题

**语言**：使用用户的输入语言或首选语言提出所有问题。不要总是使用英语。

使用单次 AskUserQuestion 包含多个问题（AskUserQuestion 自动添加"其他"选项）：

### 问题 1：水印

```
header: "水印"
question: "生成插图的水印文字？输入你的水印内容（如姓名、@用户名）"
options:
  - label: "无水印（推荐）"
    description: "不添加水印，可在 EXTEND.md 中随时启用"
```

位置默认为右下角。

### 问题 2：首选风格

```
header: "风格"
question: "默认的插图风格偏好？或输入其他风格名称或自定义风格"
options:
  - label: "sketch-notes（推荐）"
    description: "暖色奶油纸，黑色手绘线条，柔和粉彩色块 — 教育信息图感。适合大多数文章。"
  - label: "无"
    description: "基于内容分析自动选择（无强信号时回退到 sketch-notes）"
  - label: "notion"
    description: "极简手绘线条艺术"
  - label: "warm"
    description: "友好、亲切、个人化"
```

### 问题 3：输出目录

```
header: "输出目录"
question: "为文件配图时，生成的插图保存到哪里？"
options:
  - label: "imgs-subdir（推荐）"
    description: "{article-dir}/imgs/ — 文章旁的子目录中存放图片"
  - label: "same-dir"
    description: "{article-dir}/ — 图片与文章文件并列"
  - label: "illustrations-subdir"
    description: "{article-dir}/illustrations/ — 单独的插图子目录"
  - label: "independent"
    description: "illustrations/{topic-slug}/ — 当前工作目录下的独立目录"
```

### 问题 4：保存位置

```
header: "保存"
question: "偏好设置保存到哪里？"
options:
  - label: "项目级"
    description: ".baoyu-skills/（仅限当前项目）"
  - label: "用户级"
    description: "~/.baoyu-skills/（所有项目）"
```

## 保存位置

| 选择 | 路径 | 作用域 |
|------|------|--------|
| 项目级 | `.baoyu-skills/baoyu-article-illustrator/EXTEND.md` | 当前项目 |
| 用户级 | `~/.baoyu-skills/baoyu-article-illustrator/EXTEND.md` | 所有项目 |

## 设置完成后

1. 如需要则创建目录
2. 写入带前置元数据的 EXTEND.md
3. 确认："偏好设置已保存到 [path]"
4. 继续到步骤 1

## EXTEND.md 模板

```yaml
---
version: 1
watermark:
  enabled: [true/false]
  content: "[用户输入或空]"
  position: bottom-right
  opacity: 0.7
preferred_style:
  name: [选择的风格或 null]
  description: ""
default_output_dir: imgs-subdir  # same-dir | imgs-subdir | illustrations-subdir | independent
language: null
preferred_image_backend: auto
generation_batch_size: 4
custom_styles: []
---
```

`preferred_image_backend: auto` 是内置默认值 — 首次设置不询问此项。SKILL.md 中的 `## 图像生成工具` 规则随后在可用时选择运行时原生工具（Codex `imagegen`、Hermes `image_generate` 等），并回退到已安装的后端。

`generation_batch_size: 4` 是批量渲染的内置默认值。当前用户请求可覆盖一次运行。

## 后续修改偏好设置

参见 `SKILL.md` 中的 `## 更改偏好设置` 章节获取常见编辑的规范列表（固定后端、更改默认值、重新触发设置）。完整格式：`preferences-schema.md`。
