---
name: "OPSX: Apply"
description: 实施 OpenSpec 变更中的任务（实验性）
category: Workflow
tags: [workflow, artifacts, experimental]
---

实施 OpenSpec 变更中的任务。

**输入**：可选地指定变更名称（例如 `/opsx:apply add-auth`）。如果省略，检查是否可以从对话上下文中推断。如果表述模糊或不明确，必须提示选择可用变更。

**步骤**

1. **选择变更**

   如果提供了名称，直接使用。否则：
   - 如果用户提到过某个变更，从对话上下文中推断
   - 如果只有一个活跃变更，自动选择
   - 如果存在歧义，运行 `openspec list --json` 获取可用变更列表，并使用 **AskUserQuestion 工具** 让用户选择

   始终声明："Using change: <name>" 以及如何覆盖（例如 `/opsx:apply <other>`）。

2. **检查状态以理解 schema**
   ```bash
   openspec status --change "<name>" --json
   ```
   解析 JSON 理解：
   - `schemaName`：使用的工作流（例如 "spec-driven"）
   - 哪个制品包含任务（spec-driven 通常是 "tasks"，其他 schema 需检查状态）

3. **获取 apply 指令**

   ```bash
   openspec instructions apply --change "<name>" --json
   ```

   返回内容：
   - `contextFiles`：制品 ID → 具体文件路径数组（因 schema 而异）
   - 进度（总数、已完成、剩余）
   - 任务列表及状态
   - 基于当前状态的动态指令

   **处理状态：**
   - 如果 `state: "blocked"`（缺少制品）：显示消息，建议使用 `/opsx:continue`
   - 如果 `state: "all_done"`：祝贺，建议归档
   - 否则：继续实施

4. **读取上下文文件**

   读取 apply 指令输出中 `contextFiles` 下列出的每个文件路径。
   文件取决于使用的 schema：
   - **spec-driven**：proposal、specs、design、tasks
   - 其他 schema：遵循 CLI 输出的 contextFiles

5. **展示当前进度**

   显示：
   - 使用的 schema
   - 进度："N/M tasks complete"
   - 剩余任务概览
   - CLI 返回的动态指令

6. **实施任务（循环直到完成或被阻塞）**

   对每个待完成任务：
   - 显示正在处理的任务
   - 执行所需的代码变更
   - 保持变更最小化且聚焦
   - 在任务文件中标记完成：`- [ ]` → `- [x]`
   - 继续下一个任务

   **暂停条件：**
   - 任务不清晰 → 请求澄清
   - 实施中发现设计问题 → 建议更新制品
   - 遇到错误或阻塞 → 报告并等待指导
   - 用户中断

7. **完成或暂停时展示状态**

   显示：
   - 本次会话中完成的任务
   - 总体进度："N/M tasks complete"
   - 如果全部完成：建议归档
   - 如果暂停：解释原因并等待指导

**实施中的输出**

```
## Implementing: <change-name> (schema: <schema-name>)

Working on task 3/7: <task description>
[...implementation happening...]
✓ Task complete

Working on task 4/7: <task description>
[...implementation happening...]
✓ Task complete
```

**完成时的输出**

```
## Implementation Complete

**Change:** <change-name>
**Schema:** <schema-name>
**Progress:** 7/7 tasks complete ✓

### Completed This Session
- [x] Task 1
- [x] Task 2
...

All tasks complete! You can archive this change with `/opsx:archive`.
```

**暂停时的输出（遇到问题）**

```
## Implementation Paused

**Change:** <change-name>
**Schema:** <schema-name>
**Progress:** 4/7 tasks complete

### Issue Encountered
<description of the issue>

**Options:**
1. <option 1>
2. <option 2>
3. Other approach

What would you like to do?
```

**约束**
- 持续执行任务直到完成或被阻塞
- 开始前始终读取上下文文件（来自 apply 指令输出）
- 如果任务不清晰，暂停并询问后再实施
- 如果实施中发现问题，暂停并建议更新制品
- 代码变更保持最小化且限定在任务范围内
- 完成每个任务后立即更新任务复选框
- 遇到错误、阻塞或不清晰的需求时暂停——不要猜测
- 使用 CLI 输出的 contextFiles，不要假设具体的文件名

**流体工作流集成**

本技能支持"对变更执行操作"模式：

- **随时可调用**：在所有制品完成之前（如果 tasks 已存在）、部分实施之后、与其他操作交叉使用
- **允许更新制品**：如果实施中发现设计问题，建议更新制品——不是阶段锁定的，可以灵活工作
