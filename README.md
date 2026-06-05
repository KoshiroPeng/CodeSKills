# CodeSKills

CodeSKills 是一个面向 Codex、ChatGPT、Cursor 等编码助手的本地技能集合。仓库中的每个技能都用独立目录维护，核心入口通常是 `SKILL.md`，部分技能还包含 `agents/openai.yaml`、`references/`、`scripts/` 或独立说明文档。

当前仓库包含 7 个技能：

- `code-review`
- `code-simplifier`
- `code-slim-refactor`
- `iterative-module-refactor-docs`
- `legacy-refactor-assistant`
- `obsidian-vault`
- `worklog-skill`

## 仓库结构

```text
CodeSKills/
|-- code-review/
|   `-- SKILL.md
|-- code-simplifier/
|   |-- SKILL.md
|   `-- agents/openai.yaml
|-- code-slim-refactor/
|   |-- SKILL.md
|   |-- agents/openai.yaml
|   `-- references/*.md
|-- iterative-module-refactor-docs/
|   |-- SKILL.md
|   |-- agents/openai.yaml
|   |-- references/*.md
|   `-- scripts/update_refactor_index.py
|-- legacy-refactor-assistant/
|   |-- README.md
|   |-- SKILL.md
|   |-- agents/openai.yaml
|   `-- references/refactor-checklists.md
|-- obsidian-vault/
|   `-- SKILL.md
|-- worklog-skill/
|   |-- SKILL.md
|   `-- agents/openai.yaml
|-- .playwright-cli/
|   `-- page-2026-04-14T10-34-07-739Z.yml
`-- README.md
```

## 技能概览

### 1. `code-review`

用途：

- 对 GitHub Pull Request 执行结构化代码审查。
- 使用 `gh` 收集 PR 信息，而不是依赖网页浏览。
- 过滤低置信度问题，只输出高置信度、可行动的审查发现。
- 要求每个问题都带有具体文件、行号和链接。

适合触发的表达：

- `review this PR`
- `PR review`
- `pull request audit`

### 2. `code-simplifier`

用途：

- 在不改变行为的前提下精简和整理已有代码。
- 保持输入输出、副作用、公开 API、数据格式和错误语义不变。
- 优先处理用户指定文件、当前 diff 或最近修改过的局部代码。
- 减少冗余、降低嵌套、改善命名和控制流。

适合触发的表达：

- `simplify the code`
- `cleanup without changing behavior`
- `refactor for readability only`

### 3. `code-slim-refactor`

用途：

- 执行有边界的收敛式重构，减少结构复杂度。
- 保护当前后端契约、响应语义和断言标准。
- 支持 `quick` 与 `strict` 两种模式。
- 在测试与后端契约可能不一致时，使用 contract-mismatch gate 区分 `backend_regression` 和 `stale_tests`。

适合触发的表达：

- `code slim`
- `slim refactor`
- `structured simplification pass`
- `收敛重构`
- `精简重构`

### 4. `iterative-module-refactor-docs`

用途：

- 按服务边界逐轮执行模块重构。
- 每一轮只处理一个服务，并维护持久化重构文档。
- 使用 `docs/refactor/refactor-index.md` 记录服务队列、状态和提交历史。
- 每轮需要更新 `technical.md`、`task-brief.md`、`rationale.md` 和 `refactor-index.md`，并完成一次 git commit。

辅助脚本：

- `iterative-module-refactor-docs/scripts/update_refactor_index.py`

适合触发的表达：

- `iterative refactor by service`
- `multi-round refactor with docs`
- `incremental module refactor`

### 5. `legacy-refactor-assistant`

用途：

- 帮助理解、保护和逐步迁移陌生遗留系统。
- 优先识别入口、依赖、数据读写、副作用和隐藏业务规则。
- 在修改前建立保护网，例如 API 回归测试、golden-master 测试和 characterization tests。
- 先用 facade 或 adapter 包裹旧逻辑，再逐步迁移到新架构。

适合触发的表达：

- `refactor legacy code`
- `understand old source code`
- `migrate legacy system`
- `safe refactoring`

### 6. `obsidian-vault`

用途：

- 搜索、创建和整理 Obsidian 笔记库。
- 支持 `[[wikilinks]]`、索引笔记和反向链接检查。
- 优先识别当前工作区是否就是 vault，避免把机器相关路径写死到命令中。
- 倾向于通过补链接和补索引改善导航，而不是一开始就大规模移动文件。

适合触发的表达：

- `整理 Obsidian 笔记`
- `搜索笔记`
- `创建索引笔记`
- `补充 wikilinks`

### 7. `worklog-skill`

用途：

- 处理内部工时和日报相关流程。
- 当用户要求填写日报时，必须先完成 Zentao 侧操作并验证，再进入日报系统。
- 使用专用浏览器会话保持两个系统互不干扰。
- 文档中的账号、密码和内部系统信息应按安全规范维护，避免在公开位置暴露真实凭据。

适合触发的表达：

- `填写日报`
- `填日报`
- `fill daily report`

## 快速使用

在支持技能调用的环境中，可以用技能名触发：

```text
Use $code-review on PR #123
Use $code-simplifier for files changed in latest commit
Use $code-slim-refactor with mode=quick on module X
Use $iterative-module-refactor-docs to refactor one service per round
Use $legacy-refactor-assistant to analyze this legacy module
Use $obsidian-vault to organize my notes
Use $worklog-skill to fill daily report
```

## 维护规范

新增技能时，建议至少提供：

- `SKILL.md`：说明技能名称、触发条件、工作流和输出要求。
- `agents/openai.yaml`：可选，用于维护界面展示名、简短描述和默认提示词。
- `references/`：可选，用于放置流程清单、模板、示例或长文档。
- `scripts/`：可选，用于放置可复用的辅助脚本。

维护时请注意：

- README 中的技能数量、目录结构和概览应与实际仓库保持一致。
- 不要在公开文档中写入真实账号、密码、token、密钥或敏感内部信息。
- 技能说明应优先写清楚适用场景、边界、验证方式和安全约束。
- 修改脚本后应至少执行语法检查或 dry-run；如果 dry-run 会写文件，需要在脚本文档中说明或修正副作用。
- 新增或调整技能后，建议补充一个最小可运行的触发示例。

## 设计原则

- 先保护现有行为，再改善结构。
- 优先做小步、可验证、可回滚的修改。
- 对真实系统、生产数据和内部凭据保持谨慎。
- 技能文档要服务于实际执行，而不是只描述理想流程。
