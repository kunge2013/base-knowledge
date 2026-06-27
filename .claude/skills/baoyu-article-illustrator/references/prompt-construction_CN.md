# 提示词构建

## 提示词文件格式

每个提示词文件使用 YAML 前置元数据 + 内容：

```yaml
---
illustration_id: 01
type: infographic
style: blueprint
references:                    # ⚠️ 仅在文件确实存在于 references/ 目录时
  - ref_id: 01
    filename: 01-ref-diagram.png
    usage: direct              # direct | style | palette
---

[下方为类型特定模板内容...]
```

**⚠️ 关键 - 何时包含 `references` 字段**：

| 情况 | 操作 |
|------|------|
| 参考文件已保存到 `references/` | 包含在前置元数据中 ✓ |
| 风格口头提取（无文件） | 不要包含在前置元数据中，改为追加到提示词正文 |
| 前置元数据中有文件路径但文件不存在 | 错误 - 移除 references 字段 |

**参考使用类型**（仅当文件存在时）：

| 使用方式 | 描述 | 生成操作 |
|----------|------|----------|
| `direct` | 主要视觉参考 | 传递到 `--ref` 参数 |
| `style` | 仅风格特征 | 在提示词文本中描述风格 |
| `palette` | 提取调色板 | 在提示词中包含颜色 |

**如果没有参考文件但口头提取了风格/调色板**，直接追加到提示词正文：
```
COLORS（来自参考）：
- 主色：#E8756D 珊瑚色
- 辅色：#7ECFC0 薄荷色
...

STYLE（来自参考）：
- 干净线条，极少阴影
- 渐变背景
...
```

---

## 默认构图要求

**默认应用于所有提示词**：

| 要求 | 描述 |
|------|------|
| **干净构图** | 简洁布局，无视觉杂乱 |
| **留白** | 元素周围慷慨的留白和呼吸空间 |
| **无复杂背景** | 仅纯色或微妙渐变，避免繁忙纹理 |
| **居中或内容适配** | 主视觉元素居中或按内容需求定位 |
| **匹配图形** | 使用与内容主题一致的图形元素 |
| **突出核心信息** | 留白将注意力引向关键信息 |

**添加到所有提示词**：
> Clean composition with generous white space. Simple or no background. Main elements centered or positioned by content needs.

---

## 颜色规格规则

提示词中的颜色使用十六进制代码仅作为**渲染指导** — 它们告诉模型使用哪些颜色，而非显示什么文字。

**⚠️ 关键**：图像生成模型有时会将颜色名称和十六进制值渲染为图像中的可见文字标签（例如绘制 "Macaron Blue #A8D8EA" 作为标签）。必须防止这种情况。

**添加到所有包含 COLORS 章节的提示词**：
> Color values (#hex) and color names are rendering guidance only — do NOT display color names, hex codes, or palette labels as visible text in the image.

---

## 角色渲染

描绘人物时：

| 指南 | 描述 |
|------|------|
| **风格** | 简化的卡通剪影或象征性表达 |
| **避免** | 写实人物、详细面部 |
| **多样性** | 展示多人时体型多样 |
| **情感** | 通过姿态和简单手势表达 |

**添加到所有含人物形象的提示词**：
> Human figures: simplified stylized silhouettes or symbolic representations, not photorealistic.

---

## 插图中的文字

| 元素 | 指南 |
|------|------|
| **大小** | 大号、突出、一目了然 |
| **风格** | 首选手写字体增加温暖感 |
| **内容** | 仅简洁关键词和核心概念 |
| **语言** | 匹配文章语言 |

**添加到含文字的提示词**：
> Text should be large and prominent with handwritten-style fonts. Keep minimal, focus on keywords.

---

## 原则

好的提示词必须包含：

1. **布局结构优先**：描述构图、区域、流动方向
2. **具体数据/标签**：使用文章中的实际数字、术语
3. **视觉关系**：元素如何连接
4. **语义颜色**：基于含义的颜色选择（红=警告，绿=高效）
5. **风格特征**：线条处理、纹理、氛围
6. **宽高比**：以比例和复杂度级别结尾

## 类型特定模板

### 信息图（Infographic）

```
[标题] - Data Visualization

Layout: [grid/radial/hierarchical]

ZONES:
- Zone 1: [具体数值的数据点]
- Zone 2: [带指标的对比]
- Zone 3: [总结/结论]

LABELS: [文章中的具体数字、百分比、术语]
COLORS: [语义颜色映射]
STYLE: [风格特征]
ASPECT: 16:9
```

**Infographic + sketch-notes + macaron 调色板**（默认 / `hand-drawn-edu` 预设）：
```
Single-page hand-drawn educational infographic in a clean presentation style.
Warm cream paper background, black hand-drawn lines with slight wobble, soft
pastel color blocks. Feels simple, friendly, and easy to understand at a glance.
Diagram-style visuals ONLY — no realistic or photographic images.

PALETTE: macaron — soft pastel blocks on warm cream
COLORS: Warm Cream background (#F5F0E8); Black (#1A1A1A) for ALL lines, text,
        arrows, and doodles; section fills in Light Blue (#A8D8EA), Mint Green
        (#B5E5CF), Lavender (#D5C6E0), Peach (#FFD5C2); Coral Red (#E8655A)
        sparingly for one or two emphasis points only.

LAYOUT (top → bottom):
- TOP: Bold hand-lettered title, oversized, slightly wobbly, with an optional
       decorative underline or small doodle.
- MIDDLE: 2–6 rounded-rectangle info boxes arranged in a clean grid, row, or
          radial pattern. Each box = one section, one pastel fill color, one
          simple icon or sketchy cartoon element, one short keyword/phrase.
          Hand-drawn arrows connect related zones.
- BOTTOM: One short hand-lettered takeaway sentence summarizing the main idea.

ELEMENTS: Rounded info boxes with clear sectioning, wavy/straight hand-drawn
          arrows with small inline labels, simple icons and sketchy cartoon
          elements (stick figures, tools, objects), small doodle decorations
          (stars, sparkles, underlines, dots, asterisks) used sparingly.

STYLE: Minimal, well-organized, airy. Color fills don't completely fill
       outlines (slight "hand-painted" overshoot). ALL text hand-lettered —
       no computer fonts. Short labels and keywords only, never long
       paragraphs. Generous white space between sections.
```

**Infographic + vector-illustration**：
```
Flat vector illustration infographic. Clean black outlines on all elements.
COLORS: Cream background (#F5F0E6), Coral Red (#E07A5F), Mint Green (#81B29A), Mustard Yellow (#F2CC8F)
ELEMENTS: Geometric simplified icons, no gradients, playful decorative elements (dots, stars)
```

**Infographic + vector-illustration + warm 调色板**：
```
Flat vector illustration infographic. Clean black outlines on all elements.
PALETTE OVERRIDE (warm): Warm-only color palette, no cool colors.
COLORS: Soft Peach background (#FFECD2), Warm Orange (#ED8936),
        Terracotta (#C05621), Golden Yellow (#F6AD55), Deep Brown (#744210)
ELEMENTS: Geometric simplified icons, no gradients, rounded corners,
          modular card layout, consistent icon style
```

### 场景（Scene）

```
[标题] - Atmospheric Scene

FOCAL POINT: [主体]
ATMOSPHERE: [光线、氛围、环境]
MOOD: [要传达的情感]
COLOR TEMPERATURE: [warm/cool/neutral]
STYLE: [风格特征]
ASPECT: 16:9
```

### 流程图（Flowchart）

```
[标题] - Process Flow

Layout: [left-right/top-down/circular]

STEPS:
1. [步骤名] - [简述]
2. [步骤名] - [简述]
...

CONNECTIONS: [箭头类型、决策点]
STYLE: [风格特征]
ASPECT: 16:9
```

**Flowchart + vector-illustration**：
```
Flat vector flowchart with bold arrows and geometric step containers.
COLORS: Cream background (#F5F0E6), steps in Coral/Mint/Mustard, black outlines
ELEMENTS: Rounded rectangles, thick arrows, simple icons per step
```

**Flowchart + sketch-notes + macaron 调色板**：
```
Hand-drawn educational flowchart on warm cream paper. Slight wobble on all lines.
PALETTE: macaron — soft pastel color blocks
COLORS: Warm Cream background (#F5F0E8), zone fills in Macaron Blue (#A8D8EA),
        Lavender (#D5C6E0), Mint (#B5E5CF), Coral Red (#E8655A) for emphasis
ELEMENTS: Rounded cards with dashed/solid borders, wavy hand-drawn arrows with labels,
          simple stick-figure characters, doodle decorations (stars, underlines)
STYLE: Color fills don't completely fill outlines, hand-drawn lettering, generous white space
```

**Flowchart + ink-notes + mono-ink 调色板**：
```
Professional hand-drawn visual-note flowchart on pure white. Black ink line work
with slight wobble, à la Mike Rohde sketchnoting.
PALETTE: mono-ink — black ink dominant, sparse semantic accents
COLORS: Pure White background (#FFFFFF), Near Black (#1A1A1A) for all lines,
        text, and figures; Coral Red (#E8655A) only for risk/emphasis,
        Muted Teal (#5FA8A8) only for positive/solution states
ELEMENTS: Left-to-right stage boxes with rounded-rect frames, wavy hand-drawn
          arrows between stages, simple stick-figure characters with role
          labels above (e.g., "ML Engineer", "Team Lead"), dashed-border box
          for future/empty stage, small doodle icons per stage
STYLE: Hand-lettered titles (bold, oversized), handwritten stage labels and
        annotations, generous white space, bottom tagline summarizing takeaway
```

### 对比（Comparison）

```
[标题] - Comparison View

LEFT SIDE - [选项 A]：
- [要点 1]
- [要点 2]

RIGHT SIDE - [选项 B]：
- [要点 1]
- [要点 2]

DIVIDER: [视觉分隔符]
STYLE: [风格特征]
ASPECT: 16:9
```

**Comparison + vector-illustration**：
```
Flat vector comparison with split layout. Clear visual separation.
COLORS: Left side Coral (#E07A5F), Right side Mint (#81B29A), cream background
ELEMENTS: Bold icons, black outlines, centered divider line
```

**Comparison + vector-illustration + warm 调色板**：
```
Flat vector comparison with split layout. Clear visual separation.
PALETTE OVERRIDE (warm): Warm-only color palette, no cool colors.
COLORS: Left side Warm Orange (#ED8936), Right side Terracotta (#C05621),
        Soft Peach background (#FFECD2), Deep Brown (#744210) accents
ELEMENTS: Bold icons, black outlines, centered divider line
```

**Comparison + ink-notes + mono-ink 调色板**（前后对比、传统 vs 新）：
```
Professional hand-drawn sketchnote comparison on pure white. Black ink line work
with slight wobble, à la Mike Rohde sketchnoting.
PALETTE: mono-ink — black ink dominant, sparse semantic accents
COLORS: Pure White background (#FFFFFF), Near Black (#1A1A1A) for all outlines,
        text, figures, arrows; Coral Red (#E8655A) reserved for risks/gaps
        (left/Before side); Muted Teal (#5FA8A8) reserved for positives
        (right/After side). Color accents under 10% of canvas.
LAYOUT: Left | Right split with vertical hand-drawn divider. Hand-lettered
        "Before" label (top-left) and "After" label (top-right).
LEFT SIDE: Stick figure(s) with role label above, speech bubble showing the
           pain point, bulleted pain-point list in handwritten text.
RIGHT SIDE: Stick figure(s) showing the new state, bulleted improvement list,
            small positive-action icons.
BRIDGE: Curved hand-drawn "mindset shift" arrow bridging left → right with
        small inline label describing the shift.
BOTTOM: Single-line hand-lettered tagline summarizing the takeaway.
STYLE: Hand-lettered headings (bold, oversized), handwritten body annotations,
        generous white space, no computer fonts, no gradients, no shadows.
```

### 框架（Framework）

```
[标题] - Conceptual Framework

STRUCTURE: [hierarchical/network/matrix]

NODES:
- [概念 1] - [角色]
- [概念 2] - [角色]

RELATIONSHIPS: [节点如何连接]
STYLE: [风格特征]
ASPECT: 16:9
```

**Framework + vector-illustration**：
```
Flat vector framework diagram with geometric nodes and bold connectors.
COLORS: Cream background (#F5F0E6), nodes in Coral/Mint/Mustard/Blue, black outlines
ELEMENTS: Rounded rectangles or circles for nodes, thick connecting lines
```

**Framework + vector-illustration + warm 调色板**：
```
Flat vector framework diagram with geometric nodes and bold connectors.
PALETTE OVERRIDE (warm): Warm-only color palette, no cool colors.
COLORS: Soft Peach background (#FFECD2), nodes in Warm Orange (#ED8936),
        Terracotta (#C05621), Golden Yellow (#F6AD55), black outlines
ELEMENTS: Rounded rectangles or circles for nodes, thick connecting lines
```

**Framework + ink-notes + mono-ink 调色板**（指挥中心、操作系统类比）：
```
Professional hand-drawn sketchnote framework on pure white. Black ink line work
with slight wobble, à la Mike Rohde sketchnoting.
PALETTE: mono-ink — black ink dominant, sparse semantic accents
COLORS: Pure White background (#FFFFFF), Near Black (#1A1A1A) for all lines,
        text, figures; Dusty Lavender (#9B8AB5) for neutral category tags only;
        Coral Red (#E8655A) for emphasis sparingly. Color accents under 10%.
STRUCTURE: Central rounded-rectangle frame as "the system" with hand-lettered
           title inside. Inner layer of labeled sub-components (node labels
           above each). Outer layer of feeder arrows from stick-figure
           operators/users with role labels.
ELEMENTS: Stick figures at the edges with role tags ("Team Lead", "Operator"),
          wavy hand-drawn connector arrows with small inline labels, small
          doodle icons per component, dashed-border placeholder(s) for
          future/empty capabilities.
BOTTOM: Single-line hand-lettered tagline.
STYLE: Hand-lettered headings, handwritten annotations, generous white space,
        no computer fonts, no gradients.
```

### 时间线（Timeline）

```
[标题] - Chronological View

DIRECTION: [horizontal/vertical]

EVENTS:
- [日期/时期 1]：[里程碑]
- [日期/时期 2]：[里程碑]

MARKERS: [视觉标记]
STYLE: [风格特征]
ASPECT: 16:9
```

### Screen-Print 风格覆盖

当 `style: screen-print` 时，用以下内容替换标准风格指令：

```
Screen print / silkscreen poster art. Flat color blocks, NO gradients.
COLORS: 2-5 colors maximum. [从风格调色板或双色调配对中选择]
TEXTURE: Halftone dot patterns, slight color layer misregistration, paper grain
COMPOSITION: Bold silhouettes, geometric framing, negative space as storytelling element
FIGURES: Silhouettes only, no detailed faces, stencil-cut edges
TYPOGRAPHY: Bold condensed sans-serif integrated into composition (not overlaid)
```

**Scene + screen-print**：
```
Conceptual poster scene. Single symbolic focal point, NOT literal illustration.
COLORS: Duotone pair (e.g., Burnt Orange #E8751A + Deep Teal #0A6E6E) on Off-Black #121212
COMPOSITION: Centered silhouette or geometric frame, 60%+ negative space
TEXTURE: Halftone dots, paper grain, slight print misregistration
```

**Comparison + screen-print**：
```
Split poster composition. Each side dominated by one color from duotone pair.
LEFT: [Color A] side with silhouette/icon for [Option A]
RIGHT: [Color B] side with silhouette/icon for [Option B]
DIVIDER: Geometric shape or negative space boundary
TEXTURE: Halftone transitions between sides
```

---

## 调色板覆盖

当指定了调色板（通过 `--palette` 或预设）时，它覆盖风格的默认颜色：

1. 读取风格文件 → 获取渲染规则（视觉元素、风格规则、线条处理）
2. 读取调色板文件（`palettes/<palette>.md`）→ 获取颜色 + 背景
3. 调色板颜色**替换**提示词中风格的默认调色板
4. 调色板背景**替换**风格的背景色（保留风格的纹理描述）
5. 构建提示词：风格渲染指令 + 调色板颜色

**提示词前置元数据** 在指定调色板时包含：
```yaml
---
illustration_id: 01
type: infographic
style: vector-illustration
palette: macaron
---
```

**示例**：`vector-illustration` + `macaron` 调色板：
```
Flat vector illustration infographic. Clean black outlines on all elements.
PALETTE: macaron — soft pastel color blocks
COLORS: Warm Cream background (#F5F0E8), Macaron Blue (#A8D8EA), Mint (#B5E5CF),
        Lavender (#D5C6E0), Peach (#FFD5C2), Coral Red (#E8655A) for emphasis
ELEMENTS: Geometric simplified icons, no gradients, playful decorative elements
```

当未指定调色板时，照旧使用风格内置的调色板。

---

## 应避免的内容

- 模糊描述（"一张好看的图"）
- 字面隐喻插图
- 缺少具体标签/注释
- 通用装饰元素

## 水印集成

如果偏好设置中启用了水印，追加：

```
Include a subtle watermark "[内容]" positioned at [位置].
```
