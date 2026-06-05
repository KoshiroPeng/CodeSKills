# AGENTS.md

## 通用规则

默认使用简体中文回复；GitHub PR 评论、review comment、issue comment、代码审查结论、提交信息和新增代码注释也必须使用简体中文。代码标识符、API 名称、命令、错误信息和原文引用可保留英文。

涉及代码、中文注释或中文文案的文件必须保持 UTF-8 编码，不允许改成 ANSI、GBK 或其他容易导致乱码的编码。

需要提交代码时，必须执行完整 GitHub 流程：先检查 `git status`，再 `git add`、`git commit`，最后推送当前分支到 `origin`；若当前分支没有 upstream，则使用 `git push -u origin 当前分支名`。

不要使用 `git push --force`、`git reset --hard`、`git clean` 等可能破坏历史或删除改动的命令，除非我明确要求。远程仓库未配置、无权限、存在冲突或当前分支不明确时，先暂停并说明具体问题，不要猜测处理。
