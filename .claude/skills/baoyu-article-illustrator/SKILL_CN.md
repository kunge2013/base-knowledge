---
name: baoyu-article-illustrator
description: 分析文章结构，识别需要视觉辅助的位置，使用类型 × 风格 × 调色板三维方法生成插图。当用户要求"为文章配图"、"添加图片"、"生成文章插图"或 "illustrate article" 时使用。
version: 1.117.4
metadata:
  openclaw:
    homepage: https://github.com/JimLiu/baoyu-skills#baoyu-article-illustrator
---

# 文章配图工具

分析文章，识别插图位置，使用类型 × 风格 × 调色板一致性生成图片。

## 用户输入工具

当此技能需要向用户提问时，遵循以下工具选择规则（按优先级排序）：

1. **优先使用内置用户输入工具** — 即当前智能体运行时暴露的工具，例如 `AskUserQuestion`、`request_user_input`、`clarify`、`ask_user` 或任何等效工具。
2. **回退方案**：如果没有此类工具，输出带编号的纯文本消息，请用户回复所选编号/答案。
3. **批量处理**：如果工具支持单次调用多个问题，将所有适用问题合并为一次调用；如果仅支持单个问题，按优先级逐一提问。

下文中的 `AskUserQuestion` 引用为示例 — 在其他运行时请替换为本地等效工具。

## 图像生成工具

当此技能需要渲染图像时，按以下顺序确定后端：

1. **当前请求覆盖** — 如果用户在当前消息中指定了特定后端，则使用它。
2. **已保存偏好** — 如果 `EXTEND.md` 将 `preferred_image_backend` 设置为当前可用的后端，则使用它。
3. **自动选择**（当偏好为 `auto`、未设置，或固定的后端不可用时）：
   - **Codex (`imagegen`)** — 首先检查你的可用技能/工具清单。如果列出了名为 `imagegen` 的技能，说明你在 Codex 中运行，必须使用它：通过 `Skill` 工具调用，传入 `skill: "imagegen"`，提供已保存提示词文件的内容（加上输出路径和宽高比，按 Codex `imagegen` 自身参数要求）。Codex `imagegen` 是该运行时的官方光栅后端，优先级高于任何非原生技能（如 `baoyu-image-gen`），除非用户已明确固定不同的 `preferred_image_backend`。
   - **Codex via `codex exec` (`codex-imagegen`)** — 如果当前运行时没有暴露原生 `imagegen` 技能，但 `codex` CLI 在 `PATH` 上且有活跃的 `codex login`，通过 `baoyu-image-gen --provider codex-cli`（首选）路由，或者 — 如果 baoyu-image-gen 不可用 — 直接调用捆绑的封装器。详细信息、参数和运行时发现流程在 [references/codex-imagegen.md](references/codex-imagegen.md) 中 — 仅在选择此分支时加载该文件。
   - **Cursor (`GenerateImage`)** — 如果运行时暴露了原生 `GenerateImage` 工具，说明你在 Cursor 中运行，其优先级与 Codex `imagegen` 相同，高于任何非原生技能。两个硬限制：(a) 它没有宽高比参数 — 在传入 `description` 的提示词文本中明确声明目标宽高比/尺寸；(b) 它不接受输出目录 — 它保存到工具管理的位置，因此生成后将文件复制/移动到技能期望的输出路径（如 `outputs/.../NN-xxx.png`）。参考图像放入 `reference_image_paths`。
   - **其他运行时原生工具** — 如果运行时暴露了不同的原生图像工具（如 Hermes `image_generate`），以同样方式使用。
   - 否则，如果恰好安装了一个非原生后端（如 `baoyu-image-gen`），使用它。
   - 否则（多个非原生后端且无运行时原生工具），向用户询问一次 — 与任何其他初始问题批量处理。
4. **如果没有可用后端**，告知用户并询问如何继续。

**⛔ 绝不用 SVG、HTML、canvas 或其他代码渲染替代光栅图像生成。** Codex `imagegen` 自身描述说明它应在"输出应为位图资源而非仓库原生代码或矢量"时使用。如果无法通过步骤 3 解析光栅后端，回退到步骤 4 并询问用户 — **不要**静默输出 SVG、写入内联 `<svg>` 标记或生成 HTML/CSS 图形作为替代。即使文章/章节看起来像"图表类"也适用此规则：调用此规则的消费者技能已经决定需要的是光栅图像。

**⛔ 绝不通过涂画已生成位图来修复渲染文字。** 不要使用 ImageMagick、Pillow、Canvas、SVG、HTML/CSS、OCR 脚本或任何其他程序化覆盖来覆盖、重写、擦除、描边或替换已生成插图中的标签、标题或任何其他文字。如果文字有误或不清晰，请从修正后的提示词重新生成，用更少或不含图内文字重新绘制，或询问用户保留哪个不完美的候选图。

设置 `preferred_image_backend: ask` 会强制每次运行都触发步骤 3 的提示，无论可用后端如何。用户通过下方的"更改偏好设置"章节更改固定后端。

**提示词文件要求（硬性）**：在调用任何后端之前，将每张图像的完整最终提示词写入 `prompts/` 下的独立文件（命名：`NN-{type}-[slug].md`）。后端接收提示词文件（或其内容）；该文件是可复现性记录，允许切换后端而无需重新生成提示词。

上文中的具体工具名称（`imagegen`、`GenerateImage`、`image_generate`、`baoyu-image-gen`）为示例 — 在相同规则下替换为本地等效工具。

## 批量生成策略

当本次运行的所有提示词文件都已保存并验证后，默认批量生成图像。

优先级顺序：

1. 如果所选后端存在原生批量/多任务接口，则使用它。每个任务必须保持自己的提示词文件、输出路径、宽高比和直接参考图像。
2. 如果没有原生批量接口但运行时可以发出并行工具调用，每次最多分发 `generation_batch_size` 张图像。默认值：`4`。当前消息中的显式用户请求（如 `--batch-size 4` 或"并行4张一起生成"）覆盖 EXTEND.md。
3. 如果原生批量和并行工具调用都不可用，则顺序生成。

规则：

- 在该批次的所有提示词文件存在于磁盘之前，绝不开始第一个批次。
- 失败项目重试一次，不重新生成成功的项目。
- 不要仅为了并行化图像渲染而使用子智能体。仅在需要单独的提示词迭代或创意探索时使用子智能体。

## 确认策略

默认行为：**生成前确认**。

- 将显式技能调用、文件路径、匹配的信号/预设和 `EXTEND.md` 默认值仅视为**推荐输入**。它们均不授权跳过确认。
- 在用户完成步骤 3 之前，**不要**开始步骤 4 或更后的步骤。
- 仅当当前请求明确表示跳过时才跳过确认，例如："直接生成"、"不用确认"、"跳过确认"、"按默认出图"或等效措辞。
- 如果确认被显式跳过，在生成前的下一次面向用户的更新中声明假定的类型/密度/风格/调色板/语言/后端。

## 参考图像

用户可通过 `--ref <files...>` 或在对话中提供文件路径/粘贴图像来提供参考图像。参考图像为特定插图指导风格、调色板、构图或主题。

完整的检测、存储和处理规则在 [references/workflow.md](references/workflow.md)（步骤 1.0 保存到 `references/NN-ref-{slug}.{ext}`；步骤 5.3 处理每个插图的使用方式 `direct | style | palette`）。当所选后端支持批量输入时，每个提示词文件 `references:` 前置元数据中的 `direct` 用途条目应传播到其批量载荷中，以便后端可以传递它们（例如 `baoyu-image-gen` 接受每个任务的 `ref`）。

## 三维体系

| 维度 | 控制项 | 示例 |
|------|--------|------|
| **类型** | 信息结构 | 信息图、场景、流程图、对比、框架、时间线 |
| **风格** | 渲染方式 | notion、warm、minimal、blueprint、watercolor、elegant |
| **调色板** | 配色方案（可选） | macaron、warm、neon — 覆盖风格的默认颜色 |

自由组合：`--type infographic --style vector-illustration --palette macaron`

或使用预设：`--preset edu-visual` → 一个标志包含类型 + 风格 + 调色板。参见 [风格预设](references/style-presets.md)。

## 类型

| 类型 | 最适用于 |
|------|----------|
| `infographic` | 数据、指标、技术性内容 |
| `scene` | 叙事、情感性内容 |
| `flowchart` | 流程、工作流 |
| `comparison` | 并排对比、选项 |
| `framework` | 模型、架构 |
| `timeline` | 历史、演进 |

## 风格

参见 [references/styles.md](references/styles.md) 了解核心风格、完整画廊和类型 × 风格兼容性。

## 工作流程

```
- [ ] 步骤 1：预检查（EXTEND.md、参考图像、配置）
- [ ] 步骤 2：分析内容
- [ ] 步骤 3：确认设置（AskUserQuestion）
- [ ] 步骤 4：生成大纲
- [ ] 步骤 5：生成图像
- [ ] 步骤 6：收尾
```

### 步骤 1：预检查

**1.5 加载偏好设置（EXTEND.md）⛔ 阻塞操作**

按优先级顺序检查 EXTEND.md — 找到的第一个为准：

| 优先级 | 路径 | 作用域 |
|--------|------|--------|
| 1 | `.baoyu-skills/baoyu-article-illustrator/EXTEND.md` | 项目级 |
| 2 | `${XDG_CONFIG_HOME:-$HOME/.config}/baoyu-skills/baoyu-article-illustrator/EXTEND.md` | XDG |
| 3 | `$HOME/.baoyu-skills/baoyu-article-illustrator/EXTEND.md` | 用户级 |

| 结果 | 操作 |
|------|------|
| 找到 | 读取、解析、显示摘要 |
| 未找到 | ⛔ 运行 [首次设置](references/config/first-time-setup.md) |

完整流程：[references/workflow.md](references/workflow.md#step-1-pre-check)

### 步骤 2：分析

| 分析项 | 输出 |
|--------|------|
| 内容类型 | 技术 / 教程 / 方法论 / 叙事 |
| 目的 | 信息传达 / 可视化 / 想象 |
| 核心论点 | 2-5 个要可视化的要点 |
| 位置 | 插图能增加价值的地方 |

**关键**：隐喻 → 可视化底层概念，而非字面图像。

完整流程：[references/workflow.md](references/workflow.md#step-2-setup--analyze)

### 步骤 3：确认设置 ⚠️

**硬性关卡**：此步骤按[确认策略](#确认策略)为强制执行 — 在用户确认（或在当前请求中以"直接生成"/等效措辞显式选择退出）之前，步骤 4+ 不能开始。

**一次 AskUserQuestion，最多 4 个问题。Q1-Q2 必填。Q3 必填除非选择了预设。**

| 问题 | 选项 |
|------|------|
| **Q1：预设或类型** | [推荐预设]、[备选预设]，或手动选择：infographic、scene、flowchart、comparison、framework、timeline、mixed |
| **Q2：密度** | minimal (1-2)、balanced (3-5)、per-section（推荐）、rich (6+) |
| **Q3：风格** | [推荐]、minimal-flat、sci-fi、hand-drawn、editorial、scene、poster、其他 — **如果选择了预设则跳过** |
| Q4：调色板 | 默认（风格颜色）、macaron、warm、neon — **如果预设包含调色板或已设置 preferred_palette 则跳过** |
| Q5：语言 | 当文章语言 ≠ EXTEND.md 设置时 |

完整流程：[references/workflow.md](references/workflow.md#step-3-confirm-settings-)

### 步骤 4：生成大纲

保存 `outline.md`，包含前置元数据（type、density、style、palette、image_count）和条目：

```yaml
## Illustration 1
**Position**: [章节/段落]
**Purpose**: [原因]
**Visual Content**: [内容]
**Filename**: 01-infographic-concept-name.png
```

完整模板：[references/workflow.md](references/workflow.md#step-4-generate-outline)

### 步骤 5：生成图像

⛔ **阻塞：提示词文件必须在任何图像生成之前保存。** 这是硬性要求，无论选择哪个后端 — 提示词文件是可复现性记录。

1. 为每个插图创建提示词文件，按 [references/prompt-construction.md](references/prompt-construction.md)
2. 保存到 `prompts/NN-{type}-{slug}.md`，包含 YAML 前置元数据
3. 提示词**必须**使用类型特定模板，包含结构化章节（ZONES / LABELS / COLORS / STYLE / ASPECT）
4. LABELS **必须**包含文章特定数据：实际数字、术语、指标、引用
5. **不要**在未先保存提示词文件的情况下向 `--prompt` 传递临时内联提示词
6. 按顶部的 `## 图像生成工具` 规则选择后端：使用任何可用的；如有多个，向用户询问一次。每次会话在任何生成之前做一次。
   - **`codex-imagegen` 调用**：当规则解析为 `codex-imagegen` 时，参见 [references/codex-imagegen.md](references/codex-imagegen.md) 了解调用合约（首选 `baoyu-image-gen --provider codex-cli` 路径、运行时封装器发现、参数说明、stdout 格式、批量语义）。
7. **执行策略**：按 `## 批量生成策略` 批量生成：后端原生批量优先，运行时并行工具调用其次，顺序执行仅作为回退。默认批量大小为 4，除非 EXTEND.md 或当前请求覆盖。
8. 按提示词前置元数据处理参考图像（`direct`/`style`/`palette`）
9. 如果 EXTEND.md 启用了水印则应用
10. 从已保存的提示词文件生成；失败时重试一次

完整流程：[references/workflow.md](references/workflow.md#step-5-generate-images)

### 步骤 6：收尾

在段落后插入 `![description]({relative-path}/NN-{type}-{slug}.png)`。路径根据输出目录设置相对于文章文件计算。

```
文章配图完成！
文章：[path] | 类型：[type] | 密度：[level] | 风格：[style] | 调色板：[palette or default]
图像：X/N 已生成
```

## 输出目录

输出目录由 EXTEND.md 中的 `default_output_dir` 决定（在首次设置时配置）：

| `default_output_dir` | 输出路径 | Markdown 插入路径 |
|----------------------|----------|-------------------|
| `imgs-subdir`（默认） | `{article-dir}/imgs/` | `imgs/NN-{type}-{slug}.png` |
| `same-dir` | `{article-dir}/` | `NN-{type}-{slug}.png` |
| `illustrations-subdir` | `{article-dir}/illustrations/` | `illustrations/NN-{type}-{slug}.png` |
| `independent` | `illustrations/{topic-slug}/` | `illustrations/{topic-slug}/NN-{type}-{slug}.png`（相对于 cwd） |

所有辅助文件（大纲、提示词）保存在输出目录内：

```
{output-dir}/
├── outline.md
├── prompts/
│   └── NN-{type}-{slug}.md
└── NN-{type}-{slug}.png
```

当输入为**粘贴内容**（无文件路径）时，始终使用 `illustrations/{topic-slug}/`，并在旁边保存 `source-{slug}.{ext}`。

**Slug**：2-4 个单词，kebab-case。**冲突**：追加 `-YYYYMMDD-HHMMSS`。

## 修改

| 操作 | 步骤 |
|------|------|
| 编辑 | 更新提示词 → 重新生成 → 更新引用 |
| 添加 | 确定位置 → 提示词 → 生成 → 更新大纲 → 插入 |
| 删除 | 删除文件 → 移除引用 → 更新大纲 |

文字修正策略：

- 如果任何渲染文字（标签、标题等）拼写错误、乱码、难以阅读或视觉效果差，不要用代码修补位图。
- 对于文字修正的重新生成，写入新的提示词文件和新的输出路径，以便保留有缺陷的候选图供对比。
- 后期处理仅限于裁剪、调整大小、压缩或不改变文字或主要构图的格式转换。

## 参考文档

| 文件 | 内容 |
|------|------|
| [references/workflow.md](references/workflow.md) | 详细流程 |
| [references/usage.md](references/usage.md) | 命令语法 |
| [references/styles.md](references/styles.md) | 风格画廊 + 调色板画廊 |
| [references/style-presets.md](references/style-presets.md) | 预设快捷方式（类型 + 风格 + 调色板） |
| [references/prompt-construction.md](references/prompt-construction.md) | 提示词模板 |
| [references/config/first-time-setup.md](references/config/first-time-setup.md) | 首次设置 |

## 更改偏好设置

EXTEND.md 位于步骤 1.5 中列出的第一个匹配路径。三种更改方式：

- **直接编辑** — 打开 EXTEND.md 并更改字段。完整格式：`references/config/preferences-schema.md`。
- **交互式重新配置** — 删除 EXTEND.md（或说"重新配置 baoyu-article-illustrator 偏好设置"/"reconfigure baoyu-article-illustrator preferences"）。下次运行将重新触发首次设置。
- **常见单行编辑**：
  - `preferred_image_backend: auto` — 默认值；运行时原生工具优先，回退到唯一已安装的后端，仅在有多个非原生后端时询问。
  - `preferred_image_backend: codex-imagegen` — 固定为 Codex 内置。
  - `preferred_image_backend: baoyu-image-gen` — 固定为 baoyu-image-gen 技能。
  - `preferred_image_backend: ask` — 每次运行确认后端。
  - `generation_batch_size: 4` — 当运行时支持并行生成调用时默认并发渲染的图像数量。
  - `preferred_type: infographic`、`preferred_style: notion`、`preferred_palette: macaron`、`language: zh`。
  - `default_output_dir: imgs-subdir` — 相对于文章写入生成图像的位置。
