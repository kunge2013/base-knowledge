# 详细工作流程

## 步骤 1：预检查

### 1.0 检测并保存参考图像 ⚠️ 如果提供了图像则为必需

检查用户是否提供了参考图像。根据输入类型处理：

| 输入类型 | 操作 |
|----------|------|
| 提供了图像文件路径 | 复制到 `references/` 子目录 → 可使用 `--ref` |
| 对话中有图像（无路径） | **通过 AskUserQuestion 询问用户文件路径** |
| 用户无法提供路径 | 口头提取风格/调色板 → 追加到提示词中（前置元数据中不添加 references） |

**关键**：仅在文件已实际保存到 `references/` 目录时才将 `references` 添加到提示词前置元数据中。

**如果用户提供了文件路径**：
1. 复制到 `references/NN-ref-{slug}.png`
2. 创建描述文件：`references/NN-ref-{slug}.md`
3. 在继续之前验证文件存在

**如果用户无法提供路径**（口头提取）：
1. 视觉分析图像，提取：颜色、风格、构图
2. 创建 `references/extracted-style.md` 包含提取的信息
3. 不要将 `references` 添加到提示词前置元数据
4. 而是将提取的风格/颜色直接追加到提示词文本中

**描述文件格式**（仅在文件已保存时）：
```yaml
---
ref_id: NN
filename: NN-ref-{slug}.png
---
[用户的描述或自动生成的描述]
```

**验证**（仅针对已保存的文件）：
```
参考图像已保存：
- 01-ref-{slug}.png ✓（可使用 --ref）
- 02-ref-{slug}.png ✓（可使用 --ref）
```

**或对于提取的风格**：
```
参考风格已提取（无文件）：
- 颜色：#E8756D 珊瑚色, #7ECFC0 薄荷色...
- 风格：极简扁平矢量, 干净线条...
→ 将追加到提示词文本中（非 --ref）
```

---

### 1.1 确定输入类型

| 输入 | 输出目录 | 下一步 |
|------|----------|--------|
| 文件路径 | EXTEND.md 的 `default_output_dir`（默认：`imgs-subdir`）。如未配置，在 1.2 中确认。 | → 1.2 |
| 粘贴内容 | `illustrations/{topic-slug}/` | → 1.4 |

**粘贴内容的备份规则**：如果目标目录中已存在 `source.md`，在保存前重命名为 `source-backup-YYYYMMDD-HHMMSS.md`。

### 1.2-1.4 配置（仅文件路径输入）

检查偏好设置和现有状态，然后在一次 AskUserQuestion 调用中提出所有需要的问题（最多 4 个问题）。

**要包含的问题**（如果偏好设置已存在或不适用则跳过）：

| 问题 | 何时提问 | 选项 |
|------|----------|------|
| 输出目录 | EXTEND.md 中没有 `default_output_dir` | `{article-dir}/imgs/`（推荐）、`{article-dir}/`、`{article-dir}/illustrations/`、`illustrations/{topic-slug}/` |
| 现有图像 | 目标目录有 `.png/.jpg/.webp` 文件 | `supplement`（补充）、`overwrite`（覆盖）、`regenerate`（重新生成） |
| 文章更新 | 始终（文件路径输入） | `update`（更新）、`copy`（复制） |

**偏好设置值**（如已配置则跳过询问）：

| `default_output_dir` | 路径 |
|----------------------|------|
| `same-dir` | `{article-dir}/` |
| `imgs-subdir` | `{article-dir}/imgs/` |
| `illustrations-subdir` | `{article-dir}/illustrations/` |
| `independent` | `illustrations/{topic-slug}/` |

### 1.5 加载偏好设置（EXTEND.md）⛔ 阻塞操作

**关键**：如果未找到 EXTEND.md，必须在任何其他问题或步骤之前完成首次设置。不要继续处理参考图像，不要询问内容，不要询问类型/风格 — 仅先完成偏好设置。

```bash
# macOS, Linux, WSL, Git Bash
test -f .baoyu-skills/baoyu-article-illustrator/EXTEND.md && echo "project"
test -f "${XDG_CONFIG_HOME:-$HOME/.config}/baoyu-skills/baoyu-article-illustrator/EXTEND.md" && echo "xdg"
test -f "$HOME/.baoyu-skills/baoyu-article-illustrator/EXTEND.md" && echo "user"
```

```powershell
# PowerShell (Windows)
if (Test-Path .baoyu-skills/baoyu-article-illustrator/EXTEND.md) { "project" }
$xdg = if ($env:XDG_CONFIG_HOME) { $env:XDG_CONFIG_HOME } else { "$HOME/.config" }
if (Test-Path "$xdg/baoyu-skills/baoyu-article-illustrator/EXTEND.md") { "xdg" }
if (Test-Path "$HOME/.baoyu-skills/baoyu-article-illustrator/EXTEND.md") { "user" }
```

| 结果 | 操作 |
|------|------|
| 找到 | 读取、解析、显示摘要 → 继续 |
| 未找到 | ⛔ **阻塞**：仅运行首次设置（[config/first-time-setup.md](config/first-time-setup.md)）→ 完成并保存 EXTEND.md → 然后继续 |

**支持**：水印 | 首选类型/风格 | 自定义风格 | 语言 | 输出目录

---

## 步骤 2：设置与分析

### 2.1 分析内容

| 分析项 | 描述 |
|--------|------|
| 内容类型 | 技术 / 教程 / 方法论 / 叙事 |
| 插图目的 | 信息传达 / 可视化 / 想象 |
| 核心论点 | 2-5 个要可视化的要点 |
| 视觉机会 | 插图能增加价值的位置 |
| 推荐类型 | 基于内容信号和目的 |
| 推荐密度 | 基于长度和复杂度 |

### 2.2 提取核心论点

- 主要论题
- 读者需要的关键概念
- 对比/比较
- 提出的框架/模型

**关键**：如果文章使用隐喻（如"电锯切西瓜"），不要字面图示。要可视化**底层概念**。

### 2.3 识别位置

**需要插图的**：
- 核心论点（必需）
- 抽象概念
- 数据对比
- 流程、工作流

**不需要插图的**：
- 字面隐喻
- 装饰性场景
- 通用插图

### 2.4 分析参考图像（如果在步骤 1.0 中提供）

对每张参考图像：

| 分析项 | 描述 |
|--------|------|
| 视觉特征 | 风格、颜色、构图 |
| 内容/主题 | 参考图像描绘的内容 |
| 适合位置 | 哪些章节与此参考匹配 |
| 风格匹配 | 哪些插图类型/风格对齐 |
| 使用建议 | `direct` / `style` / `palette` |

| 使用方式 | 何时使用 |
|----------|----------|
| `direct` | 参考图像与期望输出高度接近 |
| `style` | 仅提取视觉风格特征 |
| `palette` | 仅提取配色方案 |

---

## 步骤 3：确认设置 ⚠️

**不要跳过。** 使用一次 AskUserQuestion 调用，最多 4 个问题。**Q1、Q2、Q3 全部必填。**

### Q1：预设或类型 ⚠️ 必填

基于步骤 2 的内容分析，首先推荐一个预设（同时设定类型和风格）。查阅 [style-presets.md](style-presets.md) 的"内容类型 → 预设推荐"表格。

- [推荐预设] — [简述：类型 + 风格 + 原因]（推荐）
- [备选预设] — [简述]
- 或手动选择类型：infographic / scene / flowchart / comparison / framework / timeline / mixed

**默认**：如果步骤 2 未发现强内容信号，推荐预设必须为 `hand-drawn-edu`（infographic + sketch-notes + macaron — 暖色奶油纸，黑色手绘线条，柔和粉彩色块）。这是通用回退选项。

**如果用户选择了预设 → 跳过 Q3**（类型和风格都已确定）。
**如果用户选择了类型 → Q3 为必填。**

### Q2：密度 ⚠️ 必填 - 不要跳过
- minimal (1-2) - 仅核心概念
- balanced (3-5) - 主要章节
- per-section - 每个章节/段落至少 1 张（推荐）
- rich (6+) - 全面覆盖

### Q3：风格 ⚠️ 必填（如果在 Q1 中选择了预设则跳过）

如果 EXTEND.md 有 `preferred_style`：
- [自定义风格名 + 简述]（推荐）
- [最兼容的核心风格 1]
- [最兼容的核心风格 2]
- 其他（查看完整风格画廊）

如果没有 `preferred_style`（优先展示核心风格）：
- [最兼容的核心风格]（推荐）
- [其他兼容核心风格 1]
- [其他兼容核心风格 2]
- 其他（查看完整风格画廊）

**核心风格**（简化选择）：

| 核心风格 | 映射到 | 最适用于 |
|----------|--------|----------|
| `hand-drawn` | sketch-notes | **默认。** 暖色奶油纸，黑色手绘线条，粉彩色块 — 教育信息图、概念解释、入门引导、通用知识文章 |
| `minimal-flat` | notion | 通用、知识分享、SaaS |
| `sci-fi` | blueprint | AI、前沿技术、系统设计 |
| `editorial` | editorial | 流程、数据、新闻 |
| `scene` | warm/watercolor | 叙事、情感、生活方式 |
| `poster` | screen-print | 观点、社论、文化、电影感 |

**默认推荐**：当步骤 2 未发现强内容信号时，在 Q1 中推荐 **`hand-drawn-edu`** 预设（→ infographic + sketch-notes + macaron）作为首选。当用户手动选择了类型但没有 preferred_style 时，在 Q3 中首先推荐 `sketch-notes`。

风格选择基于类型 × 风格兼容性矩阵（styles.md）。
**在步骤 5.1 中**，读取 `styles/<style>.md` 获取视觉元素和渲染规则。

### Q4：调色板（可选）

如果预设未指定调色板，且用户可能受益于调色板覆盖，提供可用调色板：

- 默认（使用风格内置颜色）（推荐）
- `macaron` — 暖色奶油底上的柔和粉彩色块
- `warm` — 暖色大地色调，无冷色
- `neon` — 深色背景上的鲜艳霓虹色

**跳过条件**：预设已确定调色板，或 EXTEND.md 中设置了 `preferred_palette`。

参见 [styles.md](styles.md#palette-gallery) 中的调色板画廊和 `palettes/<palette>.md` 中的完整规格。

### Q5：图像文字语言 ⚠️ 文章语言 ≠ EXTEND.md `language` 时为必填

从内容检测文章语言。如果与 EXTEND.md 的 `language` 设置不同，必须询问：
- 文章语言（匹配文章内容）（推荐）
- EXTEND.md 语言（用户的通用偏好）

**仅在以下情况跳过**：文章语言与 EXTEND.md 的 `language` 匹配，或 EXTEND.md 没有 `language` 设置。

### 显示参考使用（如果在步骤 1.0 中检测到参考图像）

在向用户展示大纲预览时，显示参考分配：

```
参考图像：
| 参考 | 文件名 | 推荐使用方式 |
|------|--------|--------------|
| 01 | 01-ref-diagram.png | direct → 插图 1, 3 |
| 02 | 02-ref-chart.png | palette → 插图 2 |
```

---

## 步骤 4：生成大纲

保存为 `{output-dir}/outline.md`（以下所有路径相对于步骤 1.1/1.2 确定的输出目录）：

```yaml
---
type: infographic
density: balanced
style: blueprint
image_count: 4
references:                    # 仅在提供了参考图像时
  - ref_id: 01
    filename: 01-ref-diagram.png
    description: "展示系统架构的技术图"
  - ref_id: 02
    filename: 02-ref-chart.png
    description: "品牌调色板的颜色图表"
---

## Illustration 1

**Position**: [章节] / [段落]
**Purpose**: [为什么有帮助]
**Visual Content**: [展示什么]
**Type Application**: [类型如何应用]
**References**: [01]                    # 可选：列出使用的 ref_id
**Reference Usage**: direct             # direct | style | palette
**Filename**: 01-infographic-concept-name.png

## Illustration 2
...
```

**要求**：
- 每个位置由内容需求证明
- 类型一致应用
- 风格在描述中体现
- 数量匹配密度
- 参考图像基于步骤 2.4 的分析分配

---

## 步骤 5：生成图像

### 5.1 创建提示词 ⛔ 阻塞操作

**每个插图在生成开始前必须有已保存的提示词文件。不要跳过此步骤。**

对大纲中的每个插图：

1. **创建提示词文件**：`{output-dir}/prompts/NN-{type}-{slug}.md`
2. **包含 YAML 前置元数据**：
   ```yaml
   ---
   illustration_id: 01
   type: infographic
   style: custom-flat-vector
   ---
   ```
3. **加载风格规格**：读取 `styles/<style>.md` 获取视觉元素、风格规则和渲染指南
4. **加载调色板规格**（如果指定了调色板）：读取 `palettes/<palette>.md` 获取颜色和背景。调色板颜色**替换**风格的默认调色板。如果未指定调色板，使用风格内置颜色。
5. **遵循类型特定模板** 来自 [prompt-construction.md](prompt-construction.md)，使用风格的渲染 + 调色板（或风格默认）的颜色
6. **提示词质量要求**（全部必需）：
   - `Layout`：描述整体构图（网格 / 放射 / 层次 / 左右 / 上下）
   - `ZONES`：描述每个视觉区域的具体内容，而非模糊描述
   - `LABELS`：使用**文章中的实际数字、术语、指标、引用** — 而非通用占位符
   - `COLORS`：指定调色板（或风格默认）中的十六进制代码及语义含义
   - `STYLE`：按风格规则描述线条处理、纹理、氛围、角色渲染
   - `ASPECT`：指定比例（如 `16:9`）
7. **应用默认值**：构图要求、角色渲染、文字指南、水印
8. **备份规则**：如果提示词文件已存在，重命名为 `prompts/NN-{type}-{slug}-backup-YYYYMMDD-HHMMSS.md`

**验证** ⛔：在进入 5.2 之前，确认所有提示词文件存在：
```
提示词文件：
- prompts/01-infographic-overview.md ✓
- prompts/02-infographic-distillation.md ✓
...
```

**不要**在未先保存提示词文件的情况下向 `--prompt` 传递临时内联文本。生成命令应使用 `--promptfiles prompts/NN-{type}-{slug}.md` 或读取已保存文件的内容用于 `--prompt`。

**执行选择**：
- 如果多个插图已有保存的提示词文件且任务现在是纯粹生成，默认使用批量生成。
- 优先使用所选后端的原生批量/多任务接口（如可用）。
- 如果后端没有原生批量接口但运行时可以发出并行工具调用，每次分发最多 `generation_batch_size` 个任务。默认：`4`。当前用户请求覆盖 EXTEND.md。
- 仅在后端批量和运行时并行调用都不可用时才顺序生成。
- 仅在每个插图仍需要在生成前进行单独的提示词重写、风格探索或其他逐图推理时使用子智能体。不要仅为了并行化渲染而使用子智能体。

**关键 - 前置元数据中的参考图像**：
- 仅在文件确实存在于 `references/` 目录中时添加 `references` 字段
- 如果风格/调色板是口头提取的（无文件），改为追加信息到提示词正文
- 写入前置元数据前验证：`test -f references/NN-ref-{slug}.png`

### 5.2 选择生成技能

遵循 `SKILL.md` 顶部的 `## 图像生成工具` 规则。具体来说：

- 如果 `imagegen` 在你的可用技能列表中（Codex），使用它 — 通过 `Skill` 工具调用，传入 `skill: "imagegen"`。
- 否则如果 EXTEND.md 固定的后端可用，使用它。
- 否则如果恰好安装了一个非原生后端，使用它。
- 否则，询问用户。

**不要生成 SVG、HTML 或任何代码矢量作为光栅图像的替代品。** 如果无法解析光栅后端，询问用户如何继续。

### 5.3 处理参考图像 ⚠️ 如果步骤 1.0 中保存了参考图像则为必需

**如果用户提供了参考图像则不要跳过。** 对每个有参考的插图：

1. **首先验证文件存在**：
   ```bash
   test -f references/NN-ref-{slug}.png && echo "exists" || echo "MISSING"
   ```
   - 如果文件缺失但在前置元数据中 → 错误，修复前置元数据或移除 references 字段
   - 如果文件存在 → 继续处理

2. 读取提示词前置元数据获取参考信息
3. 根据使用类型处理：

| 使用方式 | 操作 | 示例 |
|----------|------|------|
| `direct` | 将参考路径添加到 `--ref` 参数 | `--ref references/01-ref-brand.png` |
| `style` | 分析参考，将风格特征追加到提示词 | "风格：干净线条，渐变背景..." |
| `palette` | 从参考提取颜色，追加到提示词 | "颜色：#E8756D 珊瑚色, #7ECFC0 薄荷色..." |

4. 检查图像生成技能能力：

| 技能是否支持 `--ref` | 操作 |
|----------------------|------|
| 是（如使用 Google 的 baoyu-image-gen） | 通过 `--ref` 传递参考图像 |
| 否 | 转换为文字描述，追加到提示词 |

**验证**：生成前确认参考处理：
```
参考处理：
- 插图 1：使用 01-ref-brand.png（direct）✓
- 插图 2：从 02-ref-style.png 提取调色板 ✓
```

### 5.4 应用水印（如已启用）

添加：`在 [位置] 包含一个微妙的水印 "[内容]"。`

### 5.5 生成

1. 从已保存的提示词文件构建生成任务列表：
   - `prompt_file`：`{output-dir}/prompts/NN-{type}-{slug}.md`
   - `output_file`：`{output-dir}/NN-{type}-{slug}.png`
   - `aspect_ratio`：来自提示词前置元数据或提示词正文
   - `refs`：仅来自提示词前置元数据的已验证 `direct` 参考
2. **备份规则**：分发任务前，如果输出图像已存在，重命名为 `NN-{type}-{slug}-backup-YYYYMMDD-HHMMSS.{ext}`。
3. 批量分发任务：
   - 原生批量后端：发送所有符合条件的任务，或如果后端有实际限制则按 `generation_batch_size` 分块。
   - 运行时并行调用：同时发出最多 `generation_batch_size` 个图像调用，然后继续下一块。
   - 顺序回退：逐个处理任务。
4. 每个任务完成后记录："已生成 X/N：文件名"。
5. 失败时：从相同的已保存提示词文件重试一次失败的任务。保留成功的输出并继续。

---

## 步骤 6：收尾

### 6.1 更新文章

在对应段落后插入，使用相对于文章文件的路径：

| `default_output_dir` | 插入路径 |
|----------------------|----------|
| `imgs-subdir` | `![description](imgs/NN-{type}-{slug}.png)` |
| `same-dir` | `![description](NN-{type}-{slug}.png)` |
| `illustrations-subdir` | `![description](illustrations/NN-{type}-{slug}.png)` |
| `independent` | `![description](illustrations/{topic-slug}/NN-{type}-{slug}.png)`（相对于 cwd） |

Alt 文字：用文章语言的简洁描述。

### 6.2 输出摘要

```
文章配图完成！

文章：[path]
类型：[type] | 密度：[level] | 风格：[style]
位置：[directory]
图像：X/N 已生成

位置：
- 01-xxx.png → "[章节]" 之后
- 02-yyy.png → "[章节]" 之后

[如有失败]
失败：
- NN-zzz.png：[原因]
```
