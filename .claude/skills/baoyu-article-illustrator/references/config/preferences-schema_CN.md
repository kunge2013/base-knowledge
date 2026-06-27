---
name: preferences-schema
description: baoyu-article-illustrator 用户偏好设置的 EXTEND.md YAML 格式
---

# 偏好设置格式

## 完整格式

```yaml
---
version: 1

watermark:
  enabled: false
  content: ""
  position: bottom-right  # bottom-right|bottom-left|bottom-center|top-right

preferred_style:
  name: null              # 内置或自定义风格名
  description: ""         # 覆盖/备注

preferred_palette: null   # 内置调色板名（macaron|warm|neon）或 null

language: null            # zh|en|ja|ko|auto

default_output_dir: null  # same-dir|illustrations-subdir|independent

preferred_image_backend: auto  # auto|ask|<backend-id>

generation_batch_size: 4       # 1-8，当后端/运行时支持批量或并行生成时使用

custom_styles:
  - name: my-style
    description: "风格描述"
    color_palette:
      primary: ["#1E3A5F", "#4A90D9"]
      background: "#F5F7FA"
      accents: ["#00B4D8", "#48CAE4"]
    visual_elements: "干净线条，几何形状"
    typography: "现代无衬线体"
    best_for: "商务，教育"
---
```

## 字段参考

| 字段 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `version` | int | 1 | 格式版本 |
| `watermark.enabled` | bool | false | 启用水印 |
| `watermark.content` | string | "" | 水印文字（@用户名或自定义） |
| `watermark.position` | enum | bottom-right | 图像上的位置 |
| `preferred_style.name` | string | null | 风格名或 null |
| `preferred_style.description` | string | "" | 自定义备注/覆盖 |
| `preferred_palette` | string | null | 调色板覆盖（macaron、warm、neon 或 null） |
| `language` | string | null | 输出语言（null = 自动检测） |
| `default_output_dir` | enum | null | 输出目录偏好（null = 每次询问） |
| `preferred_image_backend` | string | `auto` | 图像后端选择。`auto` = 优先使用运行时原生工具，回退到唯一已安装的后端，多个非原生后端时询问。`ask` = 每次运行都确认。`<backend-id>`（如 `codex-imagegen`、`baoyu-image-gen`、`image_generate`）= 可用时固定此后端；不可用时回退到 `auto`。缺省 = `auto`。解析逻辑在 `SKILL.md` 的 `## 图像生成工具` 章节中有文档说明。 |
| `generation_batch_size` | int | 4 | 当后端支持原生批量或运行时可发出并行生成调用时，每批分发的图像数。无效值限制在 1-8。当前用户请求覆盖此值。 |
| `custom_styles` | array | [] | 用户自定义风格 |

## 位置选项

| 值 | 描述 |
|----|------|
| `bottom-right` | 右下角（默认，最常见） |
| `bottom-left` | 左下角 |
| `bottom-center` | 底部居中 |
| `top-right` | 右上角 |

## 输出目录选项

| 值 | 描述 |
|----|------|
| `same-dir` | 与文章同一目录 |
| `illustrations-subdir` | `{article-dir}/illustrations/` 子目录 |
| `independent` | 当前工作目录下的 `illustrations/{topic-slug}/` |

## 自定义风格字段

| 字段 | 必需 | 描述 |
|------|------|------|
| `name` | 是 | 唯一风格标识符（kebab-case） |
| `description` | 是 | 风格传达的效果 |
| `color_palette.primary` | 否 | 主色（数组） |
| `color_palette.background` | 否 | 背景色 |
| `color_palette.accents` | 否 | 强调色（数组） |
| `visual_elements` | 否 | 装饰元素 |
| `typography` | 否 | 字体/字母风格 |
| `best_for` | 否 | 推荐的内容类型 |

## 示例：最小偏好设置

```yaml
---
version: 1
watermark:
  enabled: true
  content: "@myusername"
preferred_style:
  name: notion
---
```

## 示例：完整偏好设置

```yaml
---
version: 1
watermark:
  enabled: true
  content: "@myaccount"
  position: bottom-right

preferred_style:
  name: notion
  description: "技术文章的干净插图"

language: zh

preferred_image_backend: codex-imagegen

generation_batch_size: 4

custom_styles:
  - name: corporate
    description: "专业 B2B 风格"
    color_palette:
      primary: ["#1E3A5F", "#4A90D9"]
      background: "#F5F7FA"
      accents: ["#00B4D8", "#48CAE4"]
    visual_elements: "干净线条，微妙渐变，几何形状"
    typography: "现代无衬线体，专业"
    best_for: "商务，SaaS，企业"
---
```
