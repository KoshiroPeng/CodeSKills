# CodeSKills

CodeSKills 是一个本地技能集合，用来沉淀 Codex、ChatGPT、Cursor 等编码助手可复用的工作流。每个技能独立放在一个目录中，核心入口是 `SKILL.md`，复杂技能可附带 `agents/openai.yaml`、`references/` 或 `scripts/`。

## 技能清单

| 技能 | 用途 |
|---|---|
| `code-review` | 结构化审查 GitHub Pull Request，只输出高置信度问题。 |
| `code-simplifier` | 在不改变行为的前提下精简和整理代码。 |
| `code-slim-refactor` | 执行有边界的收敛式重构，保护当前契约。 |
| `iterative-module-refactor-docs` | 按服务边界逐轮重构，并维护持续更新的重构文档。 |
| `legacy-refactor-assistant` | 理解、保护和逐步迁移陌生遗留系统。 |
| `obsidian-vault` | 搜索、创建和整理 Obsidian 笔记库。 |
| `worklog-skill` | 处理内部工时和日报相关流程。 |

## 快速使用

在支持技能调用的环境中，直接用技能名触发：

```text
Use $code-review on PR #123
Use $code-simplifier for files changed in latest commit
Use $code-slim-refactor with mode=quick on module X
Use $iterative-module-refactor-docs to refactor one service per round
Use $legacy-refactor-assistant to analyze this legacy module
Use $obsidian-vault to organize my notes
Use $worklog-skill to fill daily report
```

## 维护说明

- 新增技能时，至少提供 `SKILL.md`，说明适用场景、触发条件、执行流程和输出要求。
- 需要界面元数据时，补充 `agents/openai.yaml`。
- 需要模板、清单或长说明时，放入 `references/`。
- 需要可复用脚本时，放入 `scripts/`，并提供最小验证方式。
- README 只保留仓库概要；详细流程写在对应技能目录中。
- 不要在公开文档中写入真实账号、密码、token、密钥或敏感内部信息。
- 涉及中文内容的文件必须保持 UTF-8 编码，避免乱码。
