---
name: "OPSX: Archive"
description: 归档实验性工作流中已完成的变更
category: Workflow
tags: [workflow, archive, experimental]
---

归档实验性工作流中已完成的变更。

**输入**：在 `/opsx:archive` 后可选地指定变更名称（例如 `/opsx:archive add-auth`）。如果省略，检查是否可以从对话上下文中推断。如果表述模糊或不明确，必须提示选择可用变更。

**步骤**

1. **如果未提供变更名称，提示选择**

   运行 `openspec list --json` 获取可用变更列表。使用 **AskUserQuestion 工具** 让用户选择。

   只显示活跃的变更（不包括已归档的）。
   如果有，显示每个变更使用的 schema。

   **重要提示**：不要猜测或自动选择变更。始终让用户自己选择。

2. **检查制品完成状态**

   运行 `openspec status --change "<name>" --json` 检查制品完成情况。

   解析 JSON 理解：
   - `schemaName`：使用的工作流
   - `artifacts`：制品列表及其状态（`done` 或其他）

   **如果有制品不是 `done`：**
   - 显示未完成的制品列表作为警告
   - 提示用户确认是否继续
   - 用户确认后继续

3. **检查任务完成状态**

   读取任务文件（通常是 `tasks.md`）检查未完成任务。

   统计标记为 `- [ ]`（未完成）与 `- [x]`（已完成）的任务数。

   **如果发现未完成任务：**
   - 显示警告，说明未完成任务数量
   - 提示用户确认是否继续
   - 用户确认后继续

   **如果没有任务文件**：无任务相关警告，继续执行。

4. **评估 delta spec 同步状态**

   检查 `openspec/changes/<name>/specs/` 下是否存在 delta spec。如果不存在，直接进入归档，不提示同步。

   **如果存在 delta spec：**
   - 将每个 delta spec 与 `openspec/specs/<capability>/spec.md` 中对应的主 spec 进行比较
   - 确定将应用的变更类型（新增、修改、删除、重命名）
   - 在提示前展示合并后的摘要

   **提示选项：**
   - 如果有变更需要同步："Sync now (recommended)"、"Archive without syncing"
   - 如果已同步："Archive now"、"Sync anyway"、"Cancel"

   如果用户选择同步，使用 Task 工具（subagent_type: "general-purpose"，prompt: "Use Skill tool to invoke openspec-sync-specs for change '<name>'。Delta spec 分析：<包含分析后的 delta spec 摘要>"）。无论选择如何，都继续归档。

5. **执行归档**

   如果归档目录不存在，创建它：
   ```bash
   mkdir -p openspec/changes/archive
   ```

   使用当前日期生成目标名称：`YYYY-MM-DD-<change-name>`

   **检查目标是否已存在：**
   - 如果已存在：报错，建议重命名现有归档或使用不同日期
   - 如果不存在：将变更目录移动到归档目录

   ```bash
   mv openspec/changes/<name> openspec/changes/archive/YYYY-MM-DD-<name>
   ```

6. **展示摘要**

   显示归档完成摘要，包括：
   - 变更名称
   - 使用的 schema
   - 归档位置
   - spec 同步状态（已同步 / 跳过同步 / 无 delta spec）
   - 任何警告说明（未完成的制品/任务）

**成功时的输出**

```
## Archive Complete

**Change:** <change-name>
**Schema:** <schema-name>
**Archived to:** openspec/changes/archive/YYYY-MM-DD-<name>/
**Specs:** ✓ Synced to main specs

All artifacts complete. All tasks complete.
```

**成功时的输出（无 Delta Spec）**

```
## Archive Complete

**Change:** <change-name>
**Schema:** <schema-name>
**Archived to:** openspec/changes/archive/YYYY-MM-DD-<name>/
**Specs:** No delta specs

All artifacts complete. All tasks complete.
```

**成功但有警告的输出**

```
## Archive Complete (with warnings)

**Change:** <change-name>
**Schema:** <schema-name>
**Archived to:** openspec/changes/archive/YYYY-MM-DD-<name>/
**Specs:** Sync skipped (user chose to skip)

**Warnings:**
- Archived with 2 incomplete artifacts
- Archived with 3 incomplete tasks
- Delta spec sync was skipped (user chose to skip)

Review the archive if this was not intentional.
```

**失败时的输出（归档已存在）**

```
## Archive Failed

**Change:** <change-name>
**Target:** openspec/changes/archive/YYYY-MM-DD-<name>/

Target archive directory already exists.

**Options:**
1. Rename the existing archive
2. Delete the existing archive if it's a duplicate
3. Wait until a different date to archive
```

**约束**
- 如果未提供变更名称，始终提示用户选择
- 使用制品图（`openspec status --json`）进行完成检查
- 警告不阻止归档——仅通知和确认
- 移动到归档时保留 `.openspec.yaml`（随目录一起移动）
- 清晰展示发生了什么
- 如果请求了同步，使用 Skill 工具调用 `openspec-sync-specs`（agent 驱动）
- 如果存在 delta spec，始终运行同步评估并在提示前展示合并摘要
