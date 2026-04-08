---
title: "Karpathy's LLM Wiki: The Complete Guide to His Idea File"
source: "https://antigravity.codes/zh/blog/karpathy-llm-wiki-idea-file"
author:
  - "[[Antigravity.codes]]"
published:
created: 2026-04-08
description: "Karpathy shared his LLM Wiki idea file as a GitHub gist. We break down every concept, tool, and technique — with implementation examples and code."
tags:
  - "clippings"
---
2026年4月3日，OpenAI联合创始人、特斯拉前人工智能负责人、以及“氛围编码”概念的提出者Andrej Karpathy发布了一条题为 **“LLM知识库”** 的推文，描述了他现在如何使用LLM（逻辑逻辑模型）构建个人知识维基，而不仅仅是生成代码。这条推文迅速走红。第二天，他又发布了一条新内容：一份 **“创意文件”** ——一个GitHub gist，详细阐述了该概念背后的完整架构、理念和工具。我们在 [第一篇文章](https://antigravity.codes/zh/blog/karpathy-llm-knowledge-bases) 中报道了这条推文。本文将深入探讨后续内容——包括每个字、每个工具和每个实现细节。

获取有关人工智能、LLM 和开发者工具的最新信息

每周都会发布新的 MCP 服务器、模型更新和类似这样的指南。

### 🎬观看视频分析

![](https://www.youtube.com/watch?v=aGXTV5MTqDY)

喜欢阅读？请继续向下滚动查看包含代码示例的完整图文指南。

## 1\. 病毒式传播时刻

原推文描述了 Karpathy 将代币的使用方式从代码转向知识 **。** 他概述了一个系统，其中原始源文档（文章、论文、代码库、数据集、图像）被放入一个

```
raw/
```
目录中，然后 LLM 会逐步将它们“编译”成一个结构化的 wiki——一个
```
.md
```
包含摘要、反向链接和概念文章的相互链接文件的集合。

这条推文迅速走红。卡帕西本人也承认了这一点： **“哇，这条推文火爆全网！”** 于是他做了一件很有意思的事——他没有直接分享代码或应用程序，而是分享了一个 *创意文件* 。

随后的推文链接到了一个名为 **“LLM Wiki”** 的 GitHub gist，这是一份编写好的文档，从概念方面描述了模式、架构、操作和工具

阅读完整摘要

Karpathy 的完整方案文件可在此处获取： [gist.github.com/karpathy/442a6bf555914893e9891c11519de94f](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) 。您可以直接复制并粘贴到您的 LLM 代理中以开始使用。

## 2\. 创意档案：经纪人时代的新格式

**卡帕西提出了一个他称之为“创意档案”的** 概念 。他的原话是：

卡帕西的定义

“创意文件的概念是，在如今LLM代理时代，分享具体的代码/应用程序的意义/必要性降低了，你只需分享想法，然后对方的代理会根据你的具体需求进行定制和构建。”

这是一个微妙却意义深远的转变。传统上，当开发者构建出有用的工具时，他们会分享 *实现方式* ：GitHub 代码库、npm 包或 Docker 镜像。接收者克隆、配置并运行它。但在如今人人都能访问 LLM 代理（例如 Claude Code、OpenAI Codex、OpenCode、Cursor 等）的世界里，分享 *理念* 可能比分享代码更有价值。

为什么？因为这个理念具有可移植性。代码则具有针对性。Karpathy 在 macOS 上使用 Obsidian 和 Claude Code。你可能在 Linux 上使用 VS Code 和 OpenAI Codex。共享的 GitHub 代码库需要 fork、修改和调试。而共享的理念文件只需复制粘贴到你的代理程序中， **你的代理程序就会构建一个完全符合你当前配置的定制版本** 。

卡帕西表示，其要点“有意保持一定的抽象/模糊性，因为可以从很多方面进行探讨。” 这并非缺陷，而是设计使然。文档的最后一行明确指出： **“本文档的唯一作用是传达模式。其余部分由您的法学硕士（LLM）自行理解。”**

他还提到，该要点设有“讨论”选项卡，人们可以在这里“调整想法或贡献自己的想法”，从而将其变成一个协作式的创意空间。这是一种新型的开源——并非开源代码，而是 **开源理念** ，旨在由人工智能代理进行解读和实例化。

### 如何使用创意文件

Karpathy表示，你可以 **“把这个交给你的经纪人，他们可以帮你搭建一个专属的LLM维基，并指导你如何使用。”** 实际上，这意味着：

1. 复制 gist 内容（完整
	```
	llm-wiki.md
	```
	文件）
2. 将其粘贴到您的 LLM 代理的上下文中（Claude Code、Codex、OpenCode 或任何代理 IDE）。
3. 告诉代理人：“根据这份关于\[你的主题\]的想法文件，创建一个LLM Wiki”。
4. 代理将创建目录结构，编写模式文件，并指导您完成首次数据摄取。

译文：将想法文件定位你的 Agent  
  
\# 在 Claude Code、OpenCode 或任何 Agent-First IDE 中：  
  
\> 这是来自 Karpathy 构建关于  
\> LLM Wiki 的想法文件。我想为 \[机器学习  
\> 研究 / 竞品分析 / 读书笔记 / 等\] 构建一个。  
\>  
\> \[此处粘贴完整的要点内容\]  
\>  
\> 请设置目录结构，创建  
\>架构文件（CLAUDE.md 或AGENTS.md），并引导我  
\>完成第一个  

## 3\. 核心理念：维基百科胜过 RAG

本文的核心在于比较目前大多数人使用LLM处理文档的方式与Karpathy提出的方法。让我们来详细分析一下。

### RAG问题

Karpathy 写道： **“大多数人对 LLM 和文档的体验就像 RAG：你上传一组文件，LLM 在查询时检索相关数据块，并生成答案。”**

RAG（检索增强生成）是连接学习型学习模型 (LLM) 和私有数据的主要模式。NotebookLM 、ChatGPT 文件上传以及 **大多数** 企业级 AI 工具都采用这种工作方式。用户上传文档。当用户提出问题时，系统会搜索相关的数据块，将其输入 LLM，并生成答案。

正如卡帕西所指出的那样，问题在于： **“法学硕士课程要求学生针对每个问题从零开始重新发现知识。没有知识积累的过程。”**

如果问一个需要综合五份文件的问题，RAG系统每次都必须查找并拼凑相关的片段。明天再问同样的问题，它又得重复一遍。这样一来，信息就无法积累，也无法形成任何整体。

### 维基解决方案

Karpathy 的替代方案是： **“LLM 不是在查询时直接从原始文档中检索信息，而是逐步构建和维护一个持久的 wiki——一个结构化的、相互链接的 markdown 文件集合，它位于你和原始资源之间。”**

当您添加新来源时，LLM 不仅仅是将其编入索引以便日后检索。它还会读取该来源，提取关键信息，并将 **其整合到现有的维基中** ——更新实体页面，修订主题摘要，指出新数据与旧说法相矛盾的地方，加强或质疑不断发展的综合分析。

关键在于： **“知识库只需编译一次，然后保持最新状态，无需每次查询都重新推导。”**

| 方面 | 传统布艺 | LLM Wiki |
| --- | --- | --- |
| **知识加工过程** | 查询时（针对每个问题） | 在摄取时（每个来源一次） |
| **交叉引用** | 根据查询临时发现 | 预先构建和维护 |
| **矛盾** | 可能不会被察觉 | 在食物过程中被标记 |
| **知识积累** | 无 — 补贴查询都从零开始 | 随着每个来源和查询不断详细 |
| **输出格式** | 聊天回复（瞬间性） | 持久化Markdown文件（持久性） |
| **谁来维护** | 系统（黑盒） | LLM（透明、可编辑） |
| **人类的角色** | 上传并查询 | 策展、探索与提问 |
| **效果** | NotebookLM、ChatGPT 上传 | Karpathy 的 LLM Wiki 模式 |

### 复利效应

Karpathy反复强调这一点： **“Wiki是一种持久的、具有复利效应的产物。”** 交叉引用已经存在。矛盾点已被标记。综合内容已经反映了你读过的一切。你添加的每一个来源、提出的每一个问题，都让Wiki变得更加丰富。

### 人机协作的分工

Karpathy对工作流的描述： **“你从不（或很少）编写Wiki - LLM负责编写和维护所有内容。你负责寻找来源、探索并提出正确的问题。LLM承担所有的繁重工作 - 总结、交叉引用、归档和记录。”**

他的日常配置： **“我一边打开LLM代理，另一边打开Obsidian。LLM根据我们的对话进行编辑，我实时浏览结果——点击链接、查看关系图谱、阅读更新后面的页面。”**

接下来是一个长达整个系统的类比： **“Obsidian 是 IDE；LLM 是程序员；Wiki 是代码库。”**

## 4\. 三层架构

Karpathy 定义了三种不同的体系。每一层都有明确的使用者和用途。

### 第一层：raw

**Karpathy 写道：** “你挑选的源文件集合。文章、论文、图像、数据文件。这些是不可修改的——LLM只读取它们，表格修改。这是你的事实来源。”

这个

```
raw/
```
目录是神圣不可侵犯的。LLM 可以读取其中的任何内容，但绝不能读取。这至关重要，因为这意味着你始终拥有原始来源进行重新读取。如果 LLM 在 Wiki 中犯了错误，你可以再次原始来源并封装。

原始来源目录示例  
  
raw/  
articles/  
2026-03-attention-is-all-you-need-revisited.md  
2026-04-scaling-laws-update.md  
papers/  
transformer-architecture-v2.pdf  
mixture-of-experts-survey.pdf  
repos/  
llama-3-readme.md  
vllm-architecture-notes.md  
data/  
benchmark-results.model  
\-comparison.json  
images/  
transformer-diagram.png  
scaling-curves.png  
assets/  
\# Downloaded images from clipped articles  

### 第二层：wiki

**Karpathy 写道：** “这是一个由 LLM 生成的 Markdown 文件目录。内容包括摘要、实体页面、概念页面、比较、概述和综合。LLM 完全掌控这一层。它创建页面，在新资源到来时更新页面，维护交叉引用，并确保所有内容的一致性。你阅读它，LLM 生成它。”

维基目录示例  
  
wiki/  
index.md \# 所有页面的主目录  
log.md \# 按时间顺序排列的活动记录  
overview.md \# 高级综合  
概念/  
attention-mechanism.md  
mixture-of-experts.md  
scaling-laws.md  
tokenization.md  
entities/  
openai.md  
anthropic.md  
google-deepmind.md  
sources/  
summary-attention-revisited.md  
summary-scaling-update.md  
comparisons/  
gpt4-vs-claude-vs-gemini.md  
rag-vs-finetuning.md  

核心意见：Wiki 位于你和原始数据 **之间** 。你不再通过阅读原始论文来回答问题 — 而是阅读 Wiki。Wiki 经过了初步消化、交叉引用和综合汇总。它就像一个研究助手在阅读完所有内容并为你整理后的示意图。

### 第三层：Schema

**Karpathy 写道：** “一份文档（例如 Claude Code 的 CLAUDE.md 或 Codex 的 AGENTS.md），用于告知 LLM Wiki 的结构、规范，以及食品资料、回答问题或维护 Wiki 时应遵循的流程。这是关键的配置文件 — 它让 LLM 成为一个守纪律的 Wiki 维护者，而不是普通的聊天机器人。”

Schema 是最重要的部分。没有它，LLM 只是一个偶然能访问文件的聊天机器人。有了它，LLM 就会变成一个 **系统化的 Wiki 维护者** 能够在不同的会话中遵循一致的规则。

Karpathy补充道： **“当你逐渐摸索出适合自己领域的方案时，你和LLM会共同推动它的进展。”** 模式不是静态的。你可以从基础版本开始，随着页面对结构、frontmatter字段和工作流程的深入了解，不断对其进行优化。

Schema 示例：CLAUDE.md（适用于 Claude Code）  
  
\# LLM Wiki Schema  
  
\## 项目结构  
\- \`raw/\` — 不可变修改的源文档。严禁。  
\- \`wiki/\` — LLM 生成的 Wiki。你拥有完整的文档。  
\- \`wiki/index.md\` — 主目录。每次食物时更新。  
\- \`wiki/log.md\` — 包含增量的活动日志。  
  
\## 页面规范  
每个 Wiki 页面必须包含 YAML 其相应内容frontmatter：  
\`\`\`  
\---  
title: 页面标题  
类型: 概念 |实体|来源摘要 |比较  
来源：\[引用的原始/文件列表\]  
相关：\[链接的 Wiki 页面列表\]  
创建：YYYY-MM-DD  
更新：YYYY-MM-DD  
置信度：高 |中等| low  
\---  
\`\`\`  
  
##食物工作流  
当我说“摄取\[文件名\]”时：  
1.读取raw/中的源文件  
2\. 与我讨论核心要点  
3。 在 wiki/sources/ 中创建/更新摘要页面  
4。 更新wiki/index.md  
5\. 更新所有相关的概念和实体页面  
6\. 在 wiki/log.md 中追加一条记录## 当我提问时  
  
查询工作流程： 1\. 阅读 wiki/index.md 以查找相关页面 2\. 阅读这些页面 3。 综合答案并附上\[\[wiki-link\]\]引用 4。 如果答案有价值，建议将其归档为 一个新的 wiki 页面 \## Lint 工作流程 当我说“lint”时： 1\. 检查页面之间是否存在矛盾 2\. 检查页面之间是否存在矛盾。 找到没有入站链接的隔离页面 3。 订单已提及但进口独立页面的概念 4。 检查被新来源取代的陈旧情况 5。 建议下一步要调研的问题  
  

如果你正在使用 **OpenAI Codex** ，同样的 schema 将存入

```
AGENTS.md
```
。如果你正在使用 **OpenCode** ，将会存入
```
OPENCODE.md
```
。内容是相同的 — 只是文件名会根据读取它的代理而变化。

为什么架构很重要

如果 schema 没有，与 LLM 的每次会话都零开始。LLM 不了解你的约定、页面格式或工作流程。最终你不得不反复解释一切。Schema 是持久化记忆 — 它跨会话承载知识并确保一致性。这就意味着通用的 LLM 变成了 **你的** wiki 维护者。

## 5\. 操作：摄取、查询、Lint

Karpathy 定义了三个核心操作。每个都有明确的触发条件、处理流程和输出结果。

### 操作1：摄取

**Karpathy 写道：** “你将一个新来源放入原始集合中，并让 LLM 处理它。一个示例流程：LLM 阅读来源，与你讨论核心要点，在 wiki 中编写摘要页面，更新索引，更新整个 wiki 中相关的实体和概念页面，并在日志中追加一条记录。单个来源可能会涉及 10-15 个 wiki 页面。”

这是最重要的操作。单次摄取不仅仅是创建一个新页面 - 它会波及整个维基。如果你摄取了一篇关于新变压器变体的论文，法学硕士可能会：

- 为该论文创建一个新的摘要页面
- 使用新变体更新“注意力机制”概念页面
- 如果论文包含新的基准测试，则更新“Scaling Laws”页面
- 更新论文作者所属机构的实体页面
- 如果论文针对已知模型进行了基准测试，则更新对比页面
- 从引用新内容的现有页面中添加链接
- 使用新页面更新索引
- 在活动日志中记录导入 (ingest)

Karpathy补充了一个个人偏好： **“我更喜欢一次导入一个来源并保持参与——我会阅读摘要、检查更新，并引导LLM重点关注哪些内容。但你也可以在黎明监督的情况下批量导入多个来源。”**

导入会话示例  
  
\# 你将一篇新文章放入 raw/ 目录  
  
\> 我刚刚在 raw/articles/ 中添加了一篇新文章  
\> 2026-04-mixture-of-experts-efficiency.md  
\> 请导入。  
  
\# LLM 读取它，然后回复：  
  
论文的核心要点：  
1\. MoE 模型在相同质量下实现了 4 倍的货物  
2\. 路由效率比 Switch Transformer 提高了 23%  
3\. 与我们 wiki 中关于稠密模型（密集模型）的说法相矛盾：  
即在 10B 参数以下总是更高效  
  
我将执行以下操作：  
\- 更新 wiki/sources/summary-moe-efficiency-2026.md  
\- 更新 wiki/concepts/mixture-of-experts.md  
\- 更新wiki/concepts/scaling-laws.md (新增基准测试)  
\- 在 wiki/concepts/dense-vs-sparse.md 中标记矛盾点  
\- 更新 wiki/index.md  
\- 追加到 wiki/log.md  
  
是否继续？  

### 操作2：查询（Query）

**Karpathy 写道：** “你针对 wiki 提出的问题。LLM 会搜索相关页面，阅读并综合出标注引用的答案。根据问题的不同，答案可以采取不同的形式——Markdown 页面、对比表、幻灯片 (Marp)、图表 (matplotlib) 或蜡烛 (canvas)。”

但关于查询最重要的意见是： **“优秀的答案可以作为新页面归档回维基中。”** 你要求的对比、分析或发现的关联——这些都是宝贵的，不应该在聊天记录中消失。 **“这样，你的探索就会像导入的来源一样，在知识库中产生复利效应。”**

这就是复利循环：来源被导入wiki，查询产生新的意见，而最好的意见被归档回wiki页面。Wiki的增长不仅来自外部来源，还来自你自己的探索。

带归档功能的示例  
  
\>对比我们所有来源中  
\>MoE模型的路由策略。哪种方法具有最佳的效率/  
\>质量权衡？  
  
#LLM读取wiki/concepts/mixture-of-experts.md，  
#wiki/sources/summary-moe-\*.md，并生成分析  
  
\[LLM生成填充表格的详细对比\]  
  
\>太棒了。将其归档为wiki页面。  
  
#LLM创建查询页面。 wiki/comparisons/moe-routing-strategies.md  
\# 更新index.md，从相关页面添加链接  

### 操作3：Lint

**Karpathy写道：** “定期让LLM对wiki进行健康检查。寻找：页面之间的矛盾、被新来源取代的陈旧中继、没有入站链接的隔离页面、提及但缺少独立页面的重要概念、缺失的交叉引用，以及可以通过网络搜索填补的数据空白。”

他补充道： **“法学硕士专业建议需要新问题和需要寻找新来源。这使得维基在生长过程中保持健康。”**

示例 LINT 输出  
  
\> 检查 wiki。Wiki  
  
健康报告（2026-04-04）：  
  
矛盾之处（2）：  
\- concepts/dense-vs-sparse.md 声称  
在 100 亿以下时密集型大于稀疏型，但 sources/summary-moe-efficiency.md  
显示的结果相反。建议：更新并添加细微差别。-  
entities/openai.md 指出 GPT-5 有 2000 亿个参数，  
但 sources/summary-gpt5-leak.md 显示有 3000 亿个参数。  
  
孤立页面 (3)：  
\- concepts/tokenization.md（无外部链接）  
\- sources/summary-old-bert-paper.md（无参考文献）  
\- comparisons/old-gpu-benchmark.md（已过时）  
  
缺失页面 (4)：  
\- “RLHF” 被提及 12 次，无概念页面  
\- “Constitutional AI” 被提及 8 次，无页面  
\- “KV Cache” 在 5 个来源中被引用，无页面  
\- “Speculative Decoding” 被提及 3 次，无页面  
  
建议调查：  
\- 2025 年后推理优化方面没有相关来源  
\- Meta AI 的实体页面内容稀少（仅有 1 个来源）  
\- “Scaling Laws” 页面已 3 周未更新  

## 6\. 索引和日志记录

Karpathy定义了两个特殊文件，它们对于LLM如何浏览wiki至关重要。这两个文件用途不同，但都非常重要。

### index.md：内容目录

**Karpathy 写道：** “index.md 是面向内容的。它是一个维基百科所有内容的目录——每个页面都包含一个链接、一行摘要，以及可选的元数据，例如日期或来源数量。它按类别（实体、概念、来源等）组织。LLM 会在每次数据导入时更新它。”

index.md 的关键在于它如何取代 RAG： **“在回答查询时，LLM 首先读取索引以查找相关页面，然后深入查看这些页面。这种方法在中等规模（约 100 个源，约数百个页面）下效果出奇地好，并且避免了对基于嵌入的 RAG 基础设施的需求。”**

这是一个极具实用性的发现。大多数人认为知识检索需要向量数据库和嵌入管道。Karpathy 指出：在中等规模下，一个维护良好的索引文件就足够了。LLM 读取索引（几千个词元），识别相关页面，然后直接读取这些页面。

示例: wiki/index.md  
  
\# Wiki Index  
  
\## Concepts  
\- \[\[attention-mechanism\]\] — 自注意力、多头  
注意力及其变体 (12 个来源)  
\- \[\[mixture-of-experts\]\] — 稀疏 MoE 架构，  
路由策略 (8 个来源)  
\- \[\[scaling-laws\]\] — Chinchilla、Kaplan 拓扑  
计算训练 (15 个来源)  
\- \[\[tokenization\]\] — BPE、SentencePiece、tiktoken  
(3 个来源)  
  
\## 实体  
\- \[\[openai\]\] — GPT 系列，组织历史  
(20 个来源)  
\- \[\[anthropic\]\] — Claude 系列，pat AI  
(14 个来源)  
\- \[\[google-deepmind\]\] — Gemini, PaLM, AlphaFold  
(18 个来源)  
  
\## 来源摘要  
\- \[\[summary-attention-revisited\]\] — 2026-03-15  
\- \[\[summary-moe-efficiency\]\] — 2026-04-01  
\- \[\[summary-scaling-update\]\] — 2026-04-02  
  
\## 对比  
\- \[\[moe-routing-strategies\]\] — 归档自 2026-04-04  
\- \[\[rag-vs-finetuning\]\] — 权衡与使用场景  

### log.md: 活动时间线

**Karpathy 写道：** “log.md 是按时间顺序排列的。它是一个重复的记录，记录了发生的事件和时间——包括摄取、查询、lint 检查。”

他分享了一个实用技巧： **“如果每个条目都以一致的导出开头（例如**

```
## [2026-04-02] ingest | 文章标题
```
**：），那么日志就可以通过简单的unix工具进行解析——
```
grep "^## [" log.md | tail -5
```
即可获取最后5条记录。”**

示例：wiki/log.md  
  
\# 活动日志  
  
\## \[2026-04-04\] 摄取 | MoE 效率文章  
来源：raw/articles/2026-04-mixture-of-experts-efficiency.md  
已创建页面：sources/summary-moe-efficiency.md  
已更新页面：concepts/mixture-of-experts.md,  
concepts/scaling-laws.md,concepts/dense-vs-sparse.md  
注意：与下面的密集与稀疏主张相矛盾10B 参数。  
已标记以供审核。  
  
\## \[2026-04-04\] 查询 | MoE 路由策略对比  
问题：对比 MoE 模型中的路由策略  
已读页面：concepts/mixture-of-experts.md，3 份源码摘要  
输出：存档为 Comparisons/moe-routing-strategies.md  
  
\## \[2026-04-04\] lint | 每周健康检查  
发现矛盾建议点：2  
隔离页面：3  
补充页面：4  
建议调查项：3  
  
\## \[2026-04-03\]缩放法则  
来源：raw/articles/2026-04-scaling-laws-update.md  
创建的页面：sources/summary-scaling-update.md  
更新的页面：concepts/scaling-laws.md、entities/openai.md  

日志还能帮助LLM了解最近的操作。当您启动新会话时，LLM可以读取最近的几条日志条目，以了解wiki的当前状态。

## 7\. 工具栈

Karpathy 在要点中提到了几个具体的工具。以下是每个工具的功能以及它们如何融入工作流程。

### qmd：Markdown 本地搜索

**Karpathy 写道：** “ [qmd](https://github.com/tobi/qmd) 是一个不错的选择：它是一个本地 Markdown 文件搜索引擎，支持混合 BM25/矢量搜索和 LLM 重排序，所有操作都在设备端完成。它既有命令行界面 (CLI)（因此 LLM 可以通过 shell 调用它），也有 MCP 服务器（因此 LLM 可以将其用作原生工具）。”

**qmd** 由 Shopify 首席执行官 Tobi Lutke 开发。它的设计初衷正是为了满足 Karpathy 所描述的使用场景：搜索 Markdown 文件集合。它结合了三种搜索策略：

- **BM25全文检索** ——关键词匹配（快速、精确）
- **向量语义搜索** ——基于语义的匹配（查找相关概念）
- **LLM重新排名** ——LLM根据相关性（最高质量）对结果进行评分

所有操作均通过 GGUF 模型在本地运行

```
node-llama-cpp
```
。无需调用云端 API。数据不会离开您的计算机。

开始使用 QMD  
  
\# 全局安装 qmd  
npm install -g @tobilu/qmd  
  
\# 将你的 wiki 添加为集合  
qmd collection add./wiki --name my-research  
  
\# 关键字搜索 (BM25)  
qmd search "mixture of Expert Routing"  
  
\# 语义搜索 (向量)  
qmd vsearch "稀疏模型如何处理效率" #  
  
混合搜索与 LLM 重排序（质量最佳）  
qmd query "权衡是什么of top-k vs Expert-choice Routing"  
  
\# JSON 输出，用于通过管道传输给 LLM 代理  
qmd 查询 "缩放法则" --json  
  
\# 将 qmd 作为 MCP 服务器启动，提供 Claude Code 等使用  
qmd mcp  

Karpathy 指出，在小规模下，

```
index.md
```
文件足以用于导航。 **当 wiki 的增长超出索引所能处理的范围时，qmd 就会变得非常有用** ——这种情况通常发生在你有数百个页面，且索引本身严重，无法在单个窗口中读取时。

### Obsidian Web Clipper

**Karpathy 写道：** “Obsidian Web Clipper 是一款浏览器扩展，可将网页文章转换为 markdown。对于快速将素材存入你的原始集合非常有用。”

此 [Web Clipper](https://obsidian.md/clipper) 适用于Chrome、Firefox、Safari、Edge

- 将 HTML 转换为简洁的 Markdown 格式
- 添加 YAML 前置元数据（作者、日期、来源 URL、标签）
- 保留格式、代码块和图像
- 直接保存到您的 Obsidian 保险库（您的
	```
	raw/
	```
	目录）

它还支持 **模板** ——您可以为文章、食谱、学术论文或任何其他内容类型定义不同的剪辑格式。这使得内容导入过程更加一致和可预测。

### 将图像下载到本地

Karpathy针对图片给出了一个具体技巧： **“在Obsidian设置→文件和链接中，将‘附件文件夹路径’设置为一个固定目录（例如**

```
raw/assets/
```
**）。然后在设置→热键中，搜索‘下载’，找到‘下载当前文件的附件’，并将其绑定到一个热键（例如Ctrl+Shift+D）。”**

剪辑文章后，按下快捷键，所有图片都会下载到本地磁盘。这有什么意义呢？因为它 **“让LLM可以直接查看和引用图片，而不是依赖可能失效的URL”。**

他还指出了一个当前的限制： **“LLM 无法一次性原生读取带有内联图像的 Markdown——解决方法是让 LLM 先读取文本，然后单独查看部分或全部引用的图像，以获取更多上下文信息。”**

### Obsidian 的图形视图

**Karpathy 写道：** “Obsidian 的图形视图是查看 wiki 结构的最佳方式——哪些内容与哪些内容相连，哪些页面是中心页面，哪些页面是孤立页面。”

图表视图将所有 wiki 页面呈现为节点并全部

```
[[wiki-links]]
```
作为边。中心页面（如具有大量连接的核心概念）显示为大节点。孤立页面（没有链接）则单独显示。这使您能够仔细观察知识储备的密集程度以及存在的空白。

### Marp：Markdown 幻灯片

**Karpathy 写道：** “Marp 是一种基于 Markdown 的幻灯片格式。Obsidian 有相应的插件。它非常适合直接从 wiki 内容生成演示文稿。”

[Marp](https://marp.app/) 让你能用纯Markdown编写的演示文稿。你可以使用

```
---
```
（分割水平线）来分隔幻灯片。它支持主题、图片语法、数学公式排版，并可导出为HTML、PDF和PowerPoint。

MARP 幻灯片示例（由 LLM 来自 wiki 生成）  
  
\---  
marp: true  
theme: default  
\---  
  
\# 混合专家模型 (MoE)：核心发现  
  
自研究 wiki 中的 8 个来源  
  
\---  
  
\## 路由策略对比  
  
| 策略| 吞吐量 | 质量 |  
|----------|------------|---------|  
|前 K | 2.1 倍 |基线|  
|专家之选| 3.4 倍 | +2% |  
|哈希 | 4.0 倍 | -1% |  
  
\---  
  
\## 核心洞察  
  
选择专家路由在模型参数超过10B时，  
提供了最佳的质量/效率权衡。  
  
来源：wiki/comparisons/moe-routing-strategies.md  

### Dataview：查询你的Frontmatter

**Karpathy 写道：** “Dataview 是一个 Obsidian 插件，可以对页面 frontmatter 执行查询。如果你的 LLM 为 wiki 页面添加了 YAML frontmatter（如标签、日期、来源统计），Dataview 可以生成动态表格和列表。”

[Dataview](https://blacksmithgu.github.io/obsidian-dataview/) 将你的库 (vault) 视为数据库。如果你的 wiki 页面如下包含 frontmatter：

```
type: concept
```
,
```
sources: [file1, file2]
```
,
```
confidence: high
```
，那么 Dataview 允许你使用类 SQL 语言进行查询：

DATAVIEW 查询示例  
  
\# 列出所有标记来源统计的概念页面 \`  
\`\`dataview  
TABLE length(sources) AS "来源数量",confidence FROM "wiki/concepts" SORT length(sources) DESC \`\`\` \# 查找过去一周内更新的页面 \`\`\`dataview LIST FROM "wiki" WHERE Updated >= date(today) - dur(7 days) SORT Updated DESC \`\`\` \# 更新需要审核的低置信度页面 \`\`\`dataview TABLE标题，来源 来自“wiki” ，其中confidence =“low” SORT file.name ASC \`\`\`  
  

### Git：知识的版本控制

**Karpathy 写道：** “这个 wiki 只是一个由 markdown 文件组成的 git 仓库。你可以免费获得版本历史、分支管理和协作功能。”

这一点简单，实则强大。因为整个wiki只是一个目录中的纯markdown文件，你可以：

- ```
	git log
	```
	查看 wiki 随时间演进的过程
- ```
	git diff
	```
	查看每次摄取中具体发生了哪些变化
- ```
	git revert
	```
	回滚错误的编译
- ```
	git branch
	```
	探索不同的组织结构
- ```
	git blame
	```
	终止特定断言的添加时间
- 使用 GitHub/GitLab 通过拉取请求进行团队协作

| 工具 | 在 LLM Wiki 中的角色 | 是否必选？ |
| --- | --- | --- |
| **黑曜石** | 用于浏览 wiki 的 IDE / 查看器 | 推荐（任何降价查看器） |
| **Obsidian Web Clipper** | 采集：将网页文章剪藏为 Markdown | 推荐网页来源 |
| **qmd** | 适用于大型Wiki的搜索引擎 | 任选（小规模使用index.md即可） |
| **马普** | 输出：来自 Wiki 生成幻灯片 | 任选 |
| **数据视图** | 查询 frontmatter 以构建仪表板 | 任选 |
| **Git** | Wiki 的版本控制 | 推荐 |
| **LLM代理人** | Wiki 维护者（Claude Code、Codex 等） | 必选 |

## 8\. Karpathy列举的使用场景

Gist推出了此模式适用的五个具体场景。让我们结合实现细节逐一查看。

### 个人知识库

**卡帕蒂写道：** “追踪你自己的目标、健康、心理、自我提升——归档日记、文章、播客笔记，并随着时间的推移开始构建关于你自己的构成图景。”

实现：创建一个个人Wiki，包含目标、健康指标、阅读笔记和反思等板块。采集日志记录、阅读的文章、播客校正文本。LLM会为重复出现的主题（如“睡眠质量”、“锻炼习惯”、“职业目标”）构建概念页面，并将跨时间维度将它们关联起来。你可以提出类似这样的问题：“过去3个月里，我的精力水平提出了怎样的规律？”

### 研究

**Karpathy 写道：** “在数周或数月内深入研究某个主题——阅读论文、文章、报告，并逐步构建一个包含不断演进的论点的综合性 Wiki。”

这是 Karpathy 的主要使用场景。他的研究 Wiki 针对单个 ML 研究主题拥有约 100 篇文章和约 40 万字。该 Wiki 构建了一个不断演进的论点，并随着每个新来源的加入而不断完善。

### 读书

**Karpathy 写道：** “边读边归档每个章节，为角色、主题、情节线索以及它们之间的关联构建页面。读完后，你就拥有了一个内容丰富的位置 Wiki。”

他举了一个危险的例子： **“想想那些粉丝维基，比如 [托尔金网关](https://tolkiengateway.net/wiki/Main_Page) ——成千上万个相互关联的页面，涵盖了角色、地点、事件、语言，由志愿者社区历经多年建立。你可以在阅读时优先构建类似的东西，由 LLM 负责所有的交叉引用和维护工作。”**

想象一下在读 *《战争与和平》* 。 每读完一章，你就采集你的笔记。LLM负责维护角色页面（追踪他们在各章节中的发展）、主题页面（连接重复出现的想法）以及时间线页面。到最后，你将拥有一个相当美文学分析的个人角色Wiki。

### 企业/团队

**Karpathy 写道：** “一个由 LLM 维护的内部 Wiki，数据源自 Slack 讨论串、统计会议、项目文档、客户电话。可能还需要人工参与（人在循环中）来审核更新。Wiki 能够保持最新状态，是因为 LLM 承担了团队中没人愿意做的维护工作。”

这是企业版。数据源是内部的：Slack导出、会议录音（回放）、项目文档、客户通话记录、CRM数据。Wiki汇集了决策日志、项目时间线、客户分析和团队知识。在更新正式成为Wiki的一部分之前，会由人工（人机交互）进行审核。

### 其他所有内容

**卡帕蒂写道：** “竞争分析、尽职调查、旅行规划、课程笔记、兴趣深挖——任何你需要随时间积累知识并希望其井村分布零散分布的场景。”

模式是通用的：如果你正在从多个渠道持续收集信息并希望将其整理，那么LLM Wiki就派上用场了。我们在 [上一篇](https://antigravity.codes/zh/blog/karpathy-llm-knowledge-bases) 中报道了竞争情报、法律合规、学术文献综述等方面的详细文章实现。

## 9\. 分步实现指南

以下是遵循Karpathy架构，从零开始构建一个可运行的LLM Wiki的完整方法。

### 第1步：设置目录结构

终端  
  
mkdir -p my-research/raw/articles  
mkdir -p my-research/raw/papers  
mkdir -p my-research/raw/repos  
mkdir -p my-research/raw/assets  
mkdir -p my-research/wiki/concepts  
mkdir -p my-research/wiki/entities  
mkdir -p my-research/wiki/sources  
mkdir -p my-research/wiki/comparisons  
touch my-research/wiki/index.md  
touch my-research/wiki/log.md  
touch my-research/wiki/overview.md  
  
\# 初始化 git  
cd my-research && git init  
  
\# 在 Obsidian 中作为库（vault）打开  

### 第2步：创建Schema文件

在项目根目录下创建一个

```
CLAUDE.md
```
（适用于 Claude Code）、
```
AGENTS.md
```
（适用于 Codex）或对应的 schema 文件。使用上面第 4 节中的示例 schema 作为起点，并根据您的领域进行自定义。

### 第3步：配置黑曜石

1. **安装Obsidian** 作为
	```
	my-research/
	```
	库（vault）打开
2. **安装 Web Clipper** 浏览器扩展
3. → 设置文件与链接 → 将“附件默认放置路径”设置为
	```
	raw/assets
	```
4. 设置 → 快捷键 → 为“下载当前文件的附件” 绑定快捷键
	```
	Ctrl+Shift+D
	```
5. **安装 Marp Slides 插件** （任选，用于演示）
6. **安装Dataview插件** （可选，用于frontmatter查询）

### 第4步：导入你的第一个来源

1. 使用Web Clipper 剪藏网页文章 → 保存至
	```
	raw/articles/
	```
2. 单击
	```
	Ctrl+Shift+D
	```
	将图片下载到本地
3. 打开你的LLM代理（Claude Code、Codex、OpenCode 等）
4. 告诉它：“Ingest raw/articles/\[文件名\].md”
5. 审阅摘要、指导重点，并批准维基更新
6. 在 Obsidian 中查看 wiki——浏览新页面，查看图表视图
7. 犯罪：
	```
	git add . && git commit -m “ingest: [article title]”
	```

### 第五步：逐步积累

对每个新来源重复导入流程。导入 10-20 个来源后，开始查询 wiki。导入 50 个以上来源后，考虑添加 **qmd** 进行搜索。每周运行代码检查。

十源测试

先从10个关于某个主题的资料来源入手，把它们全部吸收。然后向维基提出一个需要综合多个资料来源的问题。如果结构化的维基能让你获得单独阅读这些资料来源无法获得的见解，那么这个系统就有效。之后再逐步扩展。

### 步骤 6：完善模式

在使用维基的过程中，你会发现哪些方法有效，哪些无效。相应地更新架构（CLAUDE.md / AGENTS.md）。或许你需要一种新的页面类型。或许你的前置元数据需要更多字段。或许你的数据导入流程应该包含一个你之前没有预料到的步骤。Karpathy 说： **“你和 LLM 会随着时间的推移共同改进它。”**

## 10\. Memex连接（1945）

卡帕西最后用一段历史联系总结了要点，使整个观点更加清晰明了：

卡帕西的话

“这个想法在精神上与范内瓦·布什的Memex（1945）有关——Memex是一个个人化的、精心维护的知识库，文档之间存在关联。布什的设想比后来的网络更接近于此：私密的、主动维护的，文档之间的关联与文档本身同样重要。他未能解决的问题是谁来维护。LLM项目解决了这个问题。”

1945年， 麻省理工学院工程师、美国科学研究与发展办公室主任 **范内瓦尔·布什在** *《大西洋月刊》* 上发表了一篇题为 [《我们如何思考》](https://www.theatlantic.com/magazine/archive/1945/07/as-we-may-think/303881/) 的文章。他描述了一种名为 **Memex** （内存+索引）的假想设备：一台桌面大小的机器，个人可以将所有书籍、记录和通信内容存储在缩微胶片上，快速搜索并创建 **关联路径** 。

布什的核心指令是，人类思维的运作方式是 **联想** ，而不是字母顺序。分层归档系统（如图书馆目录）迫使您进入严格的类别。 Memex 可以让你通过知识创建自己的路径——按照你自己的逻辑，将化学论文、经济学报告、历史论文联系起来。

他的名言： **“全新的百科全书形式即将出现，它们预置了贯穿其中的联想路径网。”**

Memex 直接的启发：

- **道格拉斯·恩格尔巴特** — 他在 1945 年阅读了布什的文章，“深受这一想法的影响”，并发明了计算机鼠标和个人计算的概念
- **特德·尼尔森** — 他在 1
- **蒂姆·伯纳斯-李** ——他于1989年开发的万维网在全球范围内实现了超文本技术

但正如卡帕西所观察到的，网络变得 *公开而混乱，* 而非 *私密且精心管理* 。布什设想的是某种个人化的东西——你的知识、你的关系、你的足迹。LLM Wiki 更接近于最初的愿景。它是私密的，由专业人员积极管理，文档之间的联系与文档本身同样重要。

布什在1945年未能解决的遗留问题： **谁来维护？** 创建关联路径、更新链接、保持所有内容的一致性——这些都是繁琐的手工工作。人们之所以放弃知识系统，是因为维护负担的增长速度超过了其价值的增长速度。正如卡帕西所写： **“LLM（法学硕士）不会感到厌倦，不会忘记更新交叉引用，而且一次就能处理15个文件。维基百科之所以能持续维护，是因为其维护成本几乎为零。”**

## 11\. 来自要点的社区想法

GitHub gist 中有一个讨论标签页，Karpathy 特别提到了这一点：“大家可以在讨论区修改想法或贡献自己的想法，这很棒。” 以下是一些来自社区的值得注意的贡献：

### .brain 文件夹模式

一位开发者分享了一个相关的模式：

```
.brain
```
在项目根目录创建一个文件夹，其中包含 Markdown 文件（
```
index.md
```
.brain、
```
architecture.md
```
.js
```
decisions.md
```
、.js、
```
changelog.md
```
.js
```
deployment.md
```
），作为 AI 会话间的持久内存。核心规则是： **“修改前读取.brain 文件，修改后更新.brain 文件，切勿将其提交到 Git。”** 这是 Karpathy 模式的轻量级版本——针对特定项目而非特定知识库。

### 通过 Gists 进行代理间通信

另一位贡献者描述了如何将 GitHub gists 设置为不同的 AI 智能体之间的通信渠道。在开发过程中，他们首先包含图形（SVG 格式）和上下的 gists，然后在不同的 AI 前端（Claude、Grok 等）之间传递。扩展了 Karpathy 的想法文件概念 — gists 不再是人与智能体之间的交互，而是 **智能体与智能体之间的通信** 。

### 追加与回顾笔记（The Append-and-Review Note）

一位社区成员指出，Karpathy 在 2025 年早些时候发布的博客文章“The Append and Review Note”（发表于 [karpathy.bearblog.dev](https://karpathy.bearblog.dev/) ），感觉它应该是这种模式的一部分。那篇文章描述了一个更简单的工作流程：一个仅附加的注释文件，会定期审查和重新组织。 LLM Wiki 是进化版本——LLM 自动进行审查和重组。

### 团队知识共享

社区提出的一个问题是：“如何与我的团队共享知识库？目前我们先创建一个 RAG，然后再创建一个 MCP 服务器。” 由于 wiki 只是一个 Git 仓库，所以最直接的答案是：将其推送到共享仓库。团队成员可以在 Obsidian 中浏览它，并且可以配置 LLM 代理以接受来自多个贡献者的更新。模式文件定义了规则；Git 负责处理协作。

## 12\. 这意味着什么

### “创意文件”作为一种新的开源格式

Karpathy或许无意间创造了一种人工智能时代分享想法的新模式。它不再分享代码（代码与具体实现密切相关），而是分享模式的结构化描述，这种描述旨在被LLM代理解读。代理会根据用户的环境、工具和偏好进行调整。这是一种 **开放的想法，** 而非开源。

### 这种模式为何会蔓延

Karpathy 解释了为什么由法学硕士维护的维基百科能够成功，而人工维护的维基百科却会失败： **“维护知识库最繁琐的部分不是阅读或思考，而是记账。更新交叉引用、保持摘要的时效性、记录新数据何时与旧说法相矛盾、以及确保数十个页面内容的一致性等等。人们放弃维基百科，是因为维护负担的增长速度超过了其价值的增长速度。法学硕士不会感到厌倦，不会忘记更新交叉引用，而且一次就能处理 15 个文件。”**

### 从 Karpathy 的推文到你的维基百科

要点最后明确呼吁采取行动： **“正确的使用方法是与您的LLM导师分享，并共同创建一个符合您需求的版本。这份文档的唯一作用是传达模式。您的LLM导师可以处理其余部分。”**

这就是关键所在。不要过度思考设置。不要等待别人开发出完美的工具。复制要点，粘贴到你的代理程序中，然后从一个主题和 10 个来源开始。LLM 会自动处理目录结构、页面格式和 frontmatter 结构。你只需提供来源和问题。维基百科会自动构建。

要点总结

Karpathy 的要点并非蓝图，而是一颗 **种子** 。你把它交给你的 LLM 导师，你们一起将其培育成适合你领域的专属内容。维基百科是一个持续更新、不断积累的资源，随着每个来源和每个问题的加入而日益丰富。LLM 导师负责所有记录工作，而你则负责思考。

## 13\. 所有资源和链接

本文及 Karpathy 的要点中提到的所有资源、工具和参考资料：

### Karpathy 的帖子

- [原推文：“LLM知识库”（2026年4月3日）](https://x.com/karpathy/status/2039805659525644595)
- [后续推文：“创意档案”（2026年4月4日）](https://x.com/karpathy/status/2040470801506541998)
- [GitHub Gist：LLM Wiki（完整方案文件）](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
- [Karpathy 的博客（bearblog）](https://karpathy.bearblog.dev/)

### 提及的工具

- [qmd](https://github.com/tobi/qmd) — 由 Tobi Lutke 开发的本地 Markdown 搜索引擎（BM25 + vector + LLM 重新排名）
- [Obsidian——](https://obsidian.md/) 基于 Markdown 的知识管理应用
- [Obsidian Web Clipper](https://obsidian.md/clipper) — 用于将网页文章剪辑成 Markdown 格式的浏览器扩展程序
- [Marp](https://marp.app/) — 基于 Markdown 的幻灯片框架（支持导出为 HTML、PDF、PowerPoint）
- [Dataview](https://blacksmithgu.github.io/obsidian-dataview/) — 用于查询页面 frontmatter 的 Obsidian 插件
- [托尔金网关](https://tolkiengateway.net/wiki/Main_Page) ——一个综合性互联维基的示例

### 概念与历史

- [“As We May Think”（诚如所思），作者 Vannevar Bush (1945)](https://www.theatlantic.com/magazine/archive/1945/07/as-we-may-think/303881/) — 《大西洋月刊》中描述 Memex 的文章
- [Memex（维基百科）](https://en.wikipedia.org/wiki/Memex) ——布什概念的历史与影响
- [Google NotebookLM](https://notebooklm.google/) — 基于 RAG 的研究工具（Karpathy 正在超越的方案）

### LLM代理平台（用于schema文件）

- **Claude Code** — 使用
	```
	CLAUDE.md
	```
	作为项目指令
- **OpenAI Codex** — 使用
	```
	AGENTS.md
	```
	作为项目指令
- **OpenCode** — 使用
	```
	OPENCODE.md
	```
	作为项目指令
- **Cursor、Windsurf 等** —各自拥有不同的schema文件规范

### 专题内容

- [第一部分：Karpathy的LLM知识库 — 后代码时代的AI工作流程](https://antigravity.codes/zh/blog/karpathy-llm-knowledge-bases) — 对最初走红推文的阅读
- **第二部分：论文** —深入探讨后续的要点和想法文件

### 相关指南

- [第一部分：Karpathy的LLM知识库](https://antigravity.codes/zh/blog/karpathy-llm-knowledge-bases) —原始推文拆解
- [2026 年 Vibe Coding：完整指南](https://antigravity.codes/zh/blog/vibe-coding-guide) — Karpathy AI 之旅的起点
- [AGENTS.md 指南](https://antigravity.codes/zh/blog/antigravity-agents-md-guide) —适用于 AI Agent 的跨工具架构文件
- [掌握Agent技能](https://antigravity.codes/zh/blog/mastering-agent-skills) —构建自动化维基编译技能
- [构建你自己的MCP服务器](https://antigravity.codes/zh/blog/build-custom-mcp-server-antigravity) —通过MCP将你的维基接入AI助手
- [智能体编排](https://antigravity.codes/zh/blog/antigravity-agent-orchestration-multi-agent) —适用于复杂知识工作流的多智能体配置

### 获取终极反重力秘籍

加入 5000 多名开发者的行列，获取我们独家 PDF 指南，掌握 Gemini 3 快捷键和代理工作流程。