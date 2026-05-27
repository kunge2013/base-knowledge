# OpenSpec 使用指南

> OpenSpec 是一个变更管理工具，帮助开发者从探索 → 提案 → 实现 → 归档的完整工作流。

---

## 目录结构

```
openspec/
├── config.yaml          # 项目配置（上下文、规则）
├── specs/               # 需求规格（长期）
│   └── <capability>/    # 按能力组织
│       └── spec.md      # 需求规格文档
├── changes/
│   ├── <change-name>/   # 当前活跃的变更
│   │   ├── .openspec.yaml    # 变更元数据
│   │   ├── proposal.md       # 做什么、为什么
│   │   ├── design.md         # 怎么实现（技术设计）
│   │   ├── tasks.md          # 任务清单（勾选式）
│   │   └── specs/            # delta specs（临时规格修改）
│   └── archive/         # 已完成的变更
│       └── YYYY-MM-DD-<name>/  # 归档目录
```

---

## 四个核心技能

| 技能               | 命令                         | 别名              | 用途          | 阶段  |
| ---------------- | -------------------------- | --------------- | ----------- | --- |
| openspec-explore | `/openspec-explore`        | `/opsx:explore` | 探索问题、思考、可视化 | 思考  |
| openspec-propose | `/openspec-propose`        | `/opsx:propose` | 创建变更提案      | 规划  |
| openspec-apply   | `/openspec-apply-change`   | `/opsx:apply`   | 实现任务清单      | 编码  |
| openspec-archive | `/openspec-archive-change` | `/opsx:archive` | 归档变更、同步规格   | 完成  |

---

## 工作流程

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   EXPLORE   │────▶│   PROPOSE   │────▶│    APPLY    │────▶│   ARCHIVE   │
│  探索思考   │     │  创建提案   │     │  实现代码   │     │  归档同步   │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
     ↓                   ↓                   ↓                   ↓
  只思考              生成文档             按任务编码            移动到archive
  不写代码            proposal             勾选完成             同步specs
                      design               - [x] ✓
                      tasks
```

### 流程特点

- **非线性**：可随时回到上一阶段，更新文档
- **灵活迭代**：实现中发现问题可更新 design/tasks
- **任务驱动**：每个任务明确、可勾选、逐步完成

---

## 各文件详解

### 1. config.yaml - 项目配置

```yaml
schema: spec-driven

# 项目上下文（生成 artifacts 时注入）
context: |
  Tech stack: TypeScript, React, Node.js
  We use conventional commits
  Domain: e-commerce platform

# 自定义规则
rules:
  proposal:
    - Keep proposals under 500 words
    - Always include a "Non-goals" section
  tasks:
    - Break tasks into chunks of max 2 hours
```

**用途**：
- `context`：告诉 AI 项目背景，生成更贴合的文档
- `rules`：针对特定 artifacts 的约束规则

---

### 2. proposal.md - 变更提案

**内容结构**：
- 概述：要做什么
- 动机：为什么做
- 范围：包含什么
- 非目标：明确不做什么
- 约束：限制条件

**作用**：定义变更的边界和意图，为后续设计和任务提供方向。

---

### 3. design.md - 技术设计

**内容结构**：
- 实现方案
- 架构决策
- API 设计
- 数据模型
- 技术选择及理由
- 风险评估

**作用**：指导实现的具体技术方案，解决"怎么做"的问题。

---

### 4. tasks.md - 任务清单

**格式**：
```markdown
## Tasks

- [ ] Task 1: 描述...
- [ ] Task 2: 描述...
- [x] Task 3: 描述... (已完成)
```

**作用**：
- 逐项执行实现
- 完成后勾选 `- [ ]` → `- [x]`
- 追踪进度

---

### 5. specs/ - 长期规格

**组织方式**：
```
openspec/specs/
├── auth/
│   └── spec.md      # 认证能力规格
├── billing/
│   └── spec.md      # 计费能力规格
└── user-management/
│   └── spec.md      # 用户管理规格
```

**用途**：
- 存放长期不变的需求规格
- 归档时 delta specs 合并到这里
- 作为未来变更的参考

---

### 6. changes/<name>/specs/ - Delta Specs

**作用**：
- 变更过程中临时修改的规格
- 归档时合并到主 specs/
- 记录这次变更对需求规格的影响

---

## 使用示例

### 示例 1：新增功能

```bash
# 1. 探索问题空间，思考设计方案
/opsx:explore add-user-authentication

# 2. 一次性创建完整提案（proposal + design + tasks）
/opsx:propose add-user-auth

# 3. 开始按任务实现
/opsx:apply add-user-auth

# 4. 完成后归档
/opsx:archive add-user-auth
```

### 示例 2：修复 Bug

```bash
# 探索问题根源
/opsx:explore fix-payment-timeout

# 创建修复提案
/opsx:propose fix-payment-timeout

# 实现修复
/opsx:apply fix-payment-timeout

# 归档
/opsx:archive fix-payment-timeout
```

---

## CLI 命令参考

### 查看状态

```bash
# 列出所有变更
openspec list --json

# 查看单个变更状态
openspec status --change "<name>" --json

# 获取 artifact 构建指令
openspec instructions <artifact-id> --change "<name>" --json

# 获取 apply 指令
openspec instructions apply --change "<name>" --json
```

### 创建变更

```bash
# 创建新变更目录
openspec new change "<name>"
```

---

## 关键原则

### 1. Explore 不写代码

探索阶段只做：
- 思考问题
- 调查代码库
- 可视化架构
- 提出问题
- 比较方案

**不写应用代码**，但可以创建 OpenSpec artifacts（proposal/design/specs）。

### 2. Propose 需完整

必须生成所有 `applyRequires` 指定的 artifacts：
- proposal.md
- design.md
- tasks.md

全部完成后才能 apply。

### 3. 任务驱动实现

Apply 阶段：
- 逐个任务执行
- 完成后立即勾选 `- [x]`
- 遇到问题暂停，更新文档后继续
- 保持最小改动范围

### 4. 灵活迭代

流程非严格线性：
- 实现中发现设计问题 → 回去更新 design.md
- 发现新需求 → 更新 proposal 或 specs
- 任务拆分不合理 → 重构 tasks.md

---

## 常见问题

### Q: 变更名称用什么格式？

A: 使用 kebab-case，如：
- `add-user-auth`
- `fix-payment-timeout`
- `refactor-database-layer`

### Q: artifacts 顺序是什么？

A: 通过 `openspec status --json` 查看：
- `artifacts[].dependencies` 显示依赖关系
- 无 pending dependencies 的先创建
- 按依赖链依次完成

### Q: 归档时 specs 会怎样？

A:
- delta specs 合并到 `openspec/specs/<capability>/spec.md`
- 变更目录移动到 `openspec/changes/archive/YYYY-MM-DD-<name>/`
- 保留所有文档供未来参考

---

## 最佳实践

1. **探索充分再提案** - 不要急于创建 proposal，先理解问题
2. **提案写清楚边界** - 明确做什么、不做什么
3. **任务拆小** - 每个任务 1-2 小时可完成
4. **保持文档更新** - 实现中发现问题及时更新 design
5. **归档前检查** - 确认所有任务完成、specs 同步