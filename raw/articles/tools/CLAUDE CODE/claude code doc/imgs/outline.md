---
type: infographic
density: per-section
style: sketch-notes
palette: macaron
image_count: 6
---

## Illustration 1

**Position**: Section 1 (背景：为什么需要多层配置？) — after the company handbook analogy
**Purpose**: Visualize the analogy of layered rules (company handbook → department spec → personal memo) and the "nearest wins" principle
**Visual Content**: Three stacked layers (公司手册/部门规范/个人备忘) with proximity arrows showing the closest one wins. Include the messaging tool example (钉钉→飞书→微信→最终用微信).
**Type Application**: Infographic with layered zones showing priority from far to near
**Filename**: 01-infographic-layered-rules-analogy.png

## Illustration 2

**Position**: Section 2 (核心结论：最近原则) — after the priority ranking
**Purpose**: Visualize the two-dimensional priority system: distance (子目录>父目录) and type (.local.md > .md)
**Visual Content**: A 2D coordinate diagram with vertical axis = priority (low→high), showing 4 items: /CLAUDE.md (lowest) → /CLAUDE.local.md → /foo/CLAUDE.md → /foo/CLAUDE.local.md (highest). Two labeled arrows: "维度一：类型" and "维度二：距离"
**Type Application**: Infographic showing the priority hierarchy as a clear visual ranking
**Filename**: 02-infographic-priority-dimensions.png

## Illustration 3

**Position**: Section 3 (加载机制详解) — after scanning path explanation
**Purpose**: Show the scanning direction (root → cwd) and which directories get scanned vs ignored
**Visual Content**: A directory tree with a highlighted path from project root to working directory. Directories on the path marked with ✅, directories off the path (sibling dirs) marked with ❌. Arrow showing scan direction.
**Type Application**: Infographic with tree structure showing included/excluded paths
**Filename**: 03-infographic-scanning-mechanism.png

## Illustration 4

**Position**: Section 4 (四种场景图解) — after scenario 2 showing the full override chain
**Purpose**: Visualize the override chain npm→yarn→cnpm→pnpm with clear layering
**Visual Content**: A horizontal chain/pipeline showing 4 files being loaded in order, each overriding the previous. Labels: npm(最远) → yarn(近) → cnpm(更近) → pnpm(最近/最终生效). Color coding from light to dark showing priority increasing.
**Type Application**: Infographic showing the override chain as a connected sequence
**Filename**: 04-infographic-override-chain.png

## Illustration 5

**Position**: Section 6 (实际场景最佳实践) — after scenario B (Monorepo)
**Purpose**: Show how different working directories in a monorepo automatically load different configurations
**Visual Content**: A monorepo tree structure with root/frontend/backend branches. Each branch has its own config loaded (showing accumulated config per branch). Arrows showing which configs are active when working in each directory.
**Type Application**: Infographic showing monorepo config isolation per module
**Filename**: 05-infographic-monorepo-config.png

## Illustration 6

**Position**: Section 7 (文件分工速查表) — after the responsibility table
**Purpose**: Summarize the 4 file types, their purposes, git status, and priority in one visual
**Visual Content**: Four cards arranged in ascending priority order: 根/CLAUDE.md (团队规范, ✅git, 最低), 根/CLAUDE.local.md (个人习惯, ❌git), 子目录/CLAUDE.md (模块技术栈, ✅git), 子目录/CLAUDE.local.md (模块调试, ❌git, 最高). Each card color-coded by priority.
**Type Application**: Infographic with card-based layout showing file responsibilities
**Filename**: 06-infographic-file-responsibilities.png
