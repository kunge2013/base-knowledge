# `codex-imagegen` 封装器调用

仅当 [图像生成工具](../SKILL.md#图像生成工具) 规则解析为 `codex-imagegen` 时加载此参考文档 — 即当前运行时没有暴露原生 `imagegen` 技能，但 `codex` CLI 在 `PATH` 上且有活跃的 `codex login`。

## 首选路径：通过 `baoyu-image-gen` 路由

如果 `baoyu-image-gen` 技能在此运行时可用，**始终**通过它调用而非直接调用封装器。它以统一方式处理所有提供者的重试/缓存/批量/EXTEND.md 偏好设置。

```bash
${BUN_X} <baoyu-image-gen-base>/scripts/main.ts \
  --provider codex-cli \
  --image <绝对路径_output> \
  --promptfiles <绝对路径_prompts/NN-{type}-{slug}.md> \
  --ar <比例> \
  [--ref <绝对路径_file>]...
```

解析 `<baoyu-image-gen-base>` 的方式与解析任何兄弟技能相同 — 通过运行时的技能注册表（`Skill` 工具、插件市场或 `$HOME/.baoyu-skills/baoyu-image-gen/`）。

## 回退：直接调用封装器

仅当 `baoyu-image-gen` 未安装在当前运行时时使用。在运行时发现封装器位置 — 不要从此技能硬编码 `../../packages/...`：

1. **遵循显式覆盖**：如果 `$BAOYU_CODEX_IMAGEGEN_BIN` 已设置且指向真实文件，使用该路径。它可能是 `.ts`（用 `bun <path>` 启动）或 `.sh`/二进制文件（直接启动）。
2. **搜索插件根目录**：从此技能目录向上遍历，查找 `packages/baoyu-codex-imagegen/src/main.ts`。如果找到，那就是封装器。用 `bun` 启动。
3. **最后手段**：告知用户 `codex-imagegen` 在此运行时不可用，询问是否安装 `baoyu-skills` 插件（或设置 `BAOYU_CODEX_IMAGEGEN_BIN`）还是选择其他后端。

找到后，调用形式为：

```bash
bun <WRAPPER>/main.ts \
  --image <绝对路径_output> \
  --prompt-file <绝对路径_prompts/NN-{type}-{slug}.md> \
  --aspect <比例> \
  [--ref <绝对路径_file>]... \
  [--timeout <ms>] \
  [--cache-dir ~/.cache/baoyu-codex-imagegen] \
  [--log-file <绝对路径_jsonl_log_path>]
```

如果缺少 `bun`，`npx -y bun <WRAPPER>/main.ts ...` 作为回退。

## 参数说明

- **所有文件系统输入** 为相对路径时会根据 `process.cwd()` 自动解析，但智能体应传递绝对路径以防止 cwd 漂移。
- **`--timeout`** 每次 `codex exec` 尝试默认为 `300000`（5 分钟）。在慢速网络或大型提示词时提高（如 `--timeout 600000` 为 10 分钟）。
- **`--cache-dir`** 默认关闭。启用后可跳过相同提示词+宽高比+参考的重复生成。
- **认证**：封装器使用用户的 Codex 订阅 — 不会读取或发送 `OPENAI_API_KEY`。

## Stdout 合约

单行 JSON：

- 成功：`{"status":"ok","path":"...","bytes":N,"elapsed_seconds":N,"thread_id":"...","attempts":N,"cached":bool,...}`
- 失败：`{"status":"error","path":"...","bytes":0,"error":"...","error_kind":"..."}`

`error_kind` 值：`codex_not_installed`、`invalid_args`、`prompt_file_missing`、`spawn_failed`、`timeout`、`no_image_gen_tool_use`、`output_missing`、`invalid_png`、`agent_refused`、`lock_busy`。

对于可重试的错误（timeout、spawn_failed、no_image_gen_tool_use、output_missing、invalid_png、agent_refused），询问用户是否重试或回退到其他后端。

## 批量语义

- Codex `image_gen` 每次调用返回**一张图像**（仅 `n=1`）。多图任务必须每张图像分发一次封装器调用。
- 封装器不接受 `--sessionId` 标志。链/场景一致性必须来自 `--ref` 参考图像。
- `--size` 和 `--quality` 被静默忽略 — Codex 从 `--aspect` 决定像素尺寸。
