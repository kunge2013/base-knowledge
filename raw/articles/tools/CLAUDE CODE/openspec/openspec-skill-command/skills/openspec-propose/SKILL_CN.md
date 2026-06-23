---
name: openspec-propose
description: 一步到位地提出新变更提案并生成所有制品。适用于用户想快速描述要构建的内容，并获取包含 design、specs 和 tasks 的完整提案，随时准备实施。
license: MIT
compatibility: 需要 openspec CLI。
metadata:
  author: openspec
  version: "1.0"
  generatedBy: "1.3.1"
---

提出新变更提案——创建变更并一步生成所有制品。

我将创建一个包含以下制品的变更：
- proposal.md（做什么 & 为什么）
- design.md（怎么做）
- tasks.md（实施步骤）

准备好实施后，运行 `/opsx:apply`

---

**输入**：用户的请求应包含变更名称（kebab-case）或对要构建内容的描述。

**步骤**

1. **如果输入不清晰，询问用户想构建什么**

   使用 **AskUserQuestion 工具**（开放式，无预设选项）询问：
   > "你想做什么变更？描述一下你想构建或修复的内容。"

   从用户的描述中派生出 kebab-case 名称（例如 "add user authentication" → `add-user-auth`）。

   **重要提示**：在不理解用户想构建什么之前，不要继续。

2. **创建变更目录**
   ```bash
   openspec new change "<name>"
   ```
   这将在 `openspec/changes/<name>/` 下创建一个带 `.openspec.yaml` 的变更脚手架。

3. **获取制品构建顺序**
   ```bash
   openspec status --change "<name>" --json
   ```
   解析 JSON 获取：
   - `applyRequires`：实施前需要的制品 ID 数组（例如 `["tasks"]`）
   - `artifacts`：所有制品的列表，包含状态和依赖关系

4. **按顺序创建制品，直到可进入 apply 阶段**

   使用 **TodoWrite 工具**跟踪制品进度。

   按依赖顺序遍历制品（没有未满足依赖的制品优先）：

   a. **对于每个 `ready` 的制品（依赖已满足）**：
      - 获取指令：
        ```bash
        openspec instructions <artifact-id> --change "<name>" --json
        ```
      - 指令 JSON 包含：
        - `context`：项目背景（对你的约束——不要写入输出文件）
        - `rules`：制品特定规则（对你的约束——不要写入输出文件）
        - `template`：用于输出文件的结构
        - `instruction`：该制品类型的 schema 级指导
        - `outputPath`：制品的写入路径
        - `dependencies`：已完成的制品，供你读取上下文
      - 读取任何已完成的依赖文件以获取上下文
      - 使用 `template` 作为结构创建制品文件
      - 将 `context` 和 `rules` 作为约束应用——但不要将它们复制到文件中
      - 显示简要进度："Created <artifact-id>"

   b. **继续直到所有 `applyRequires` 制品完成**
      - 每次创建制品后，重新运行 `openspec status --change "<name>" --json`
      - 检查 `applyRequires` 中的每个制品 ID 在 artifacts 数组中是否都有 `status: "done"`
      - 当所有 `applyRequires` 制品都完成时停止

   c. **如果某个制品需要用户输入**（上下文不清晰）：
      - 使用 **AskUserQuestion 工具** 澄清
      - 然后继续创建

5. **展示最终状态**
   ```bash
   openspec status --change "<name>"
   ```

**输出**

完成所有制品后，总结：
- 变更名称和位置
- 已创建的制品列表及简要描述
- 就绪状态："All artifacts created! Ready for implementation."
- 提示："Run `/opsx:apply` or ask me to implement to start working on the tasks."

**制品创建指南**

- 对每个制品类型，遵循 `openspec instructions` 中的 `instruction` 字段
- Schema 定义了每个制品应包含的内容——遵循它
- 在创建新制品前，读取依赖制品获取上下文
- 使用 `template` 作为输出文件的结构——填入各个部分
- **重要提示**：`context` 和 `rules` 是对**你**的约束，不是文件内容
  - 不要将 `<context>`、`<rules>`、`<project_context>` 块复制到制品中
  - 它们指导你写什么，但绝不应出现在输出文件中

**约束**
- 创建实施所需的所有制品（由 schema 的 `apply.requires` 定义）
- 创建新制品前始终读取依赖制品
- 如果上下文严重不清晰，询问用户——但优先做合理决策以保持推进
- 如果同名的变更已存在，询问用户是想继续还是创建新的
- 写入后验证每个制品文件存在，再继续下一个
