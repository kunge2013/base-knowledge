# 风格参考

## 核心风格

用于快速选择的简化风格层级：

| 核心风格 | 映射到 | 最适用于 |
|----------|--------|----------|
| `hand-drawn` | sketch-notes | **默认。** 暖色奶油纸，黑色手绘线条，粉彩色块 — 教育信息图、概念解释、入门引导、通用知识文章 |
| `vector` | vector-illustration | 知识文章、教程、技术内容 |
| `minimal-flat` | notion | 通用、知识分享、SaaS |
| `sci-fi` | blueprint | AI、前沿技术、系统设计 |
| `editorial` | editorial | 流程、数据、新闻 |
| `scene` | warm/watercolor | 叙事、情感、生活方式 |
| `poster` | screen-print | 观点、社论、文化、电影感 |

大多数情况下使用核心风格。**当未检测到强内容信号时，默认为 `hand-drawn`（→ sketch-notes）。** 查看下方完整风格画廊获取更精细的控制。

---

## 风格画廊

| 风格 | 描述 | 最适用于 |
|------|------|----------|
| `vector-illustration` | 干净的扁平矢量艺术，大胆形状 | 知识文章、教程、技术内容 |
| `notion` | 极简手绘线条艺术 | 知识分享、SaaS、生产力 |
| `elegant` | 精致、有品位 | 商务、思想领袖 |
| `warm` | 友好、亲切 | 个人成长、生活方式、教育 |
| `minimal` | 超简洁、禅意 | 哲学、极简主义、核心概念 |
| `blueprint` | 技术示意图 | 架构、系统设计、工程 |
| `watercolor` | 柔和艺术感，自然温暖 | 生活方式、旅行、创意 |
| `editorial` | 杂志风格信息图 | 技术解释、新闻 |
| `scientific` | 学术精确图表 | 生物、化学、技术研究 |
| `chalkboard` | 课堂粉笔画风格 | 教育、教学、解释 |
| `fantasy-animation` | 吉卜力/迪士尼风手绘 | 故事书、魔幻、情感 |
| `flat` | 现代大胆几何形状 | 现代数字、当代 |
| `flat-doodle` | 可爱扁平，粗轮廓 | 可爱、友好、亲切 |
| `intuition-machine` | 做旧纸张的技术简报 | 技术简报、学术 |
| `nature` | 有机大地风插图 | 环保、健康 |
| `pixel-art` | 复古 8-bit 游戏美学 | 游戏、复古技术 |
| `playful` | 异想天开的粉彩涂鸦 | 有趣、休闲、教育 |
| `retro` | 80/90 年代霓虹几何 | 80/90 年代怀旧、大胆 |
| `sketch` | 原始铅笔笔记本风格 | 头脑风暴、创意探索 |
| `screen-print` | 大胆海报艺术，半调纹理，限色 | 观点、社论、文化、电影感 |
| `sketch-notes` | 柔和手绘暖色笔记 | 教育、暖色笔记 |
| `ink-notes` | 纯白纸上黑色墨水，稀疏语义重点色，手写字母（类似 Mike Rohde 的视觉笔记） | 前后对比文章、技术宣言、框架类比 |
| `vintage` | 做旧羊皮纸历史感 | 历史、传承 |

完整规格：`references/styles/<style>.md`

## 类型 × 风格兼容性矩阵

| | sketch-notes | vector-illustration | notion | warm | minimal | blueprint | watercolor | elegant | editorial | scientific | screen-print |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| infographic | ✓✓ | ✓✓ | ✓✓ | ✓ | ✓✓ | ✓✓ | ✓ | ✓✓ | ✓✓ | ✓✓ | ✓ |
| scene | ✗ | ✓ | ✓ | ✓✓ | ✓ | ✗ | ✓✓ | ✓ | ✓ | ✗ | ✓✓ |
| flowchart | ✓✓ | ✓✓ | ✓✓ | ✓ | ✓ | ✓✓ | ✗ | ✓ | ✓✓ | ✓ | ✗ |
| comparison | ✓✓ | ✓✓ | ✓✓ | ✓ | ✓✓ | ✓ | ✓ | ✓✓ | ✓✓ | ✓ | ✓ |
| framework | ✓✓ | ✓✓ | ✓✓ | ✓ | ✓✓ | ✓✓ | ✗ | ✓✓ | ✓ | ✓✓ | ✓ |
| timeline | ✓ | ✓ | ✓✓ | ✓ | ✓ | ✓ | ✓✓ | ✓✓ | ✓✓ | ✓ | ✓ |

✓✓ = 强烈推荐 | ✓ = 兼容 | ✗ = 不推荐

## 按类型自动选择

当没有内容信号强匹配时，`sketch-notes` 是所有图表类型的默认首选。仅当步骤 2 中的内容分析发现明确信号（技术/数据/叙事/观点）时才用另一种首选覆盖。

| 类型 | 首选风格 | 备选风格 |
|------|----------|----------|
| infographic | sketch-notes | vector-illustration, notion, blueprint, editorial |
| scene | warm | watercolor, elegant |
| flowchart | sketch-notes | vector-illustration, notion, blueprint |
| comparison | sketch-notes | vector-illustration, notion, elegant |
| framework | sketch-notes | blueprint, vector-illustration, notion |
| timeline | elegant | sketch-notes, warm, editorial |

## 按内容信号自动选择

| 内容信号 | 推荐类型 | 推荐风格 |
|----------|----------|----------|
| **（无强信号/通用文章）** | **infographic** | **sketch-notes** |
| 知识、概念、教程、学习、指南、入门 | infographic | sketch-notes, vector-illustration, notion |
| 生产力、SaaS、工具、应用、软件 | infographic | sketch-notes, notion, vector-illustration |
| 怎么做、步骤、工作流、流程、教程 | flowchart | sketch-notes, vector-illustration, notion |
| API、指标、数据、对比、数字 | infographic | blueprint, vector-illustration |
| 技术、AI、编程、开发、代码 | infographic | vector-illustration, blueprint, sketch-notes |
| 框架、模型、架构、原则 | framework | blueprint, vector-illustration, sketch-notes |
| vs、优缺点、前后对比、替代方案 | comparison | vector-illustration, notion, sketch-notes |
| 宣言、思维转变、职场、操作系统、白板、专业视觉笔记 | comparison / framework | ink-notes |
| 故事、情感、旅程、体验、个人 | scene | warm, watercolor |
| 历史、时间线、进程、演进 | timeline | elegant, warm |
| 商业、专业、策略、企业 | framework | elegant |
| 观点、社论、文化、哲学、电影感、戏剧性、海报 | scene | screen-print |
| 生物、化学、医学、科学 | infographic | scientific |
| 解释、新闻、杂志、调查 | infographic | editorial |

## 按类型的风格特征

### infographic + sketch-notes（默认）
- 暖色奶油纸背景，黑色手绘线条带微微抖动
- 2-6 个圆角粉彩信息框（浅蓝 / 薄荷 / 薰衣草 / 蜜桃）
- 顶部大胆手写标题
- 短关键词标签，简单图标，小涂鸦（星星、下划线、闪光）
- 底部一行手写总结句
- 通透、极简、图表风格 — 绝不写实
- 适合单页教育解释和概念总结

### infographic + vector-illustration
- 干净的扁平矢量形状，大胆几何形式
- 鲜艳但和谐的配色
- 清晰的视觉层次，带图标和标签
- 现代、专业、高可读性
- 适合知识文章和教程

### flowchart + vector-illustration
- 大胆箭头和连接线
- 清晰的步骤容器带图标
- 干净的进程流动
- 高对比度提高可读性

### comparison + vector-illustration
- 分割布局，清晰的视觉分隔
- 每侧大胆的图标
- 颜色编码区分
- 一目了然的对比

### framework + vector-illustration
- 几何节点表示
- 清晰的层次结构
- 大胆连接线
- 现代系统图美学

### infographic + blueprint
- 技术精度，示意图线条
- 网格布局，清晰分区
- 等宽字体标签，数据为重
- 蓝/白配色方案

### infographic + notion
- 手绘感，亲切
- 柔和图标，圆角元素
- 中性调色板，干净背景
- 适合 SaaS/生产力

### scene + warm
- 金色时光照明，温馨氛围
- 柔和渐变，自然纹理
- 温暖、个人化的感觉
- 适合故事叙述

### scene + watercolor
- 艺术、绘画效果
- 柔和边缘，颜色晕染
- 梦幻、创意氛围
- 适合生活方式/旅行

### flowchart + notion
- 清晰步骤指示器
- 简单箭头连接
- 极少装饰
- 聚焦流程清晰度

### flowchart + blueprint
- 技术精度
- 详细连接点
- 工程美学
- 适合复杂系统

### comparison + elegant
- 精致分隔线
- 平衡的排版
- 专业外观
- 商务对比

### framework + blueprint
- 精确节点连接
- 层次清晰
- 系统架构感
- 技术框架

### timeline + elegant
- 精致的标记
- 讲究的排版
- 历史厚重感
- 专业演示

### timeline + warm
- 友好的进程感
- 有机流动
- 个人旅程感
- 成长叙事

### scene + screen-print
- 大胆剪影，象征性构图
- 2-5 种带半调纹理的扁平色
- 图底反转（负空间讲述次要故事）
- 复古海报美学，概念性而非字面
- 适合观点文章和文化评论

### comparison + screen-print
- 分割双色调构图（每侧一种颜色）
- 大胆几何分隔
- 象征图标优于细节渲染
- 高对比度，即时视觉冲击

### framework + screen-print
- 模板切割边缘的几何节点表示
- 限色编码（每个概念层级一种颜色）
- 干净的剪影图标
- 海报风格层次，大胆排版

---

## 调色板画廊

调色板覆盖风格的默认颜色。任何风格可与任何调色板组合：`--style vector-illustration --palette macaron`。

| 调色板 | 描述 | 最适用于 |
|--------|------|----------|
| `macaron` | 暖色奶油底上的柔和粉彩色块（蓝、薄荷、薰衣草、蜜桃） | 教育、知识、教程 |
| `warm` | 暖色大地色调（橙、赤陶、金）在柔和蜜桃底上，无冷色 | 品牌、产品、生活方式 |
| `neon` | 深紫背景上的鲜艳霓虹色（粉、青、黄） | 游戏、复古、流行文化 |
| `mono-ink` | 纯白纸上的黑色墨水，稀疏语义重点色（珊瑚红、柔和蓝绿、灰薰衣草） | 专业视觉笔记、前后对比、宣言 |

完整规格：`references/palettes/<palette>.md`

当未指定调色板时，使用风格内置的调色板。

## 调色板覆盖规则

1. 读取风格文件 → 渲染规则（视觉元素、风格规则）
2. 读取调色板文件 → 颜色 + 背景
3. 调色板颜色**替换**风格的默认调色板
4. 调色板背景**替换**风格的默认背景色
5. 风格的纹理描述保持不变
