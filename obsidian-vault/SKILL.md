---
name: obsidian-vault
description: 用于搜索、创建和整理 Obsidian 笔记库，支持 wikilinks 和索引笔记，适合在需要查找、编写或组织 Obsidian 笔记时使用。
---

# Obsidian Vault

## Vault 识别规则

除非用户明确要求，否则不要把某一个操作系统的绝对路径写死成唯一来源。

按下面顺序识别当前要操作的 vault：

1. 如果当前工作区根目录包含 `.obsidian/`，就把当前工作区根目录当作 vault 根目录。
2. 否则，如果当前工作区明显就是这个笔记仓库，就使用 `git rev-parse --show-toplevel` 返回的仓库根目录。
3. 如果前两种都不成立，再去探测候选路径，并且只有在路径真实存在时才能使用。

这个笔记仓库的常见候选路径：

- macOS: `/Users/pengkang/Documents/NoteBook/GitHub/NoteBook`
- Windows: `D:\Obsidian Vault\AI Research\`
- WSL: `/mnt/d/Obsidian Vault/AI Research/`

只要条件允许，都应该在 vault 根目录执行命令，并优先使用 `.` 这样的相对路径，而不是把绝对路径硬编码进每条命令里。

当前仓库按主题目录组织，例如 `AI/`、`项目/`、`Tool/`、`dev/`、`dify/`、`量化/`、`Video/`、`Clippings/` 等。

## 命名约定

- 保留当前仓库已经存在的目录分类结构，不要强行扁平化。
- **索引笔记** 统一放在 `Indexes/` 目录下。
- 文件名优先简洁、可读，并尽量和所在目录附近的命名风格保持一致。
- 新建索引笔记时，优先使用类似 `Notebook Index.md`、`AI Index.md`、`Projects Index.md` 这样的命名。
- 尽量避免往仓库根目录堆很多新文件；总结页、导航页优先放到 `Indexes/`。

## 链接规则

- 使用 Obsidian 的 `[[wikilinks]]` 语法，例如 `[[Note Title]]`。
- 如果不同目录里存在同名笔记，优先使用带路径或别名的写法，例如 `[[AI/Codex/基本操作|Codex 基本操作]]`。
- 普通笔记在合适的时候，可以在底部补充“相关笔记”或“依赖笔记”链接。
- 索引笔记应保持轻量，通常直接列出一组 `[[wikilinks]]` 即可。
- 即使底层文件系统是 Windows，wikilink 里的路径分隔符也统一使用 `/`。

## 常用工作流

### 搜索笔记

优先从 vault 根目录开始搜索，这样命令在 macOS、Linux、WSL 下都更一致：

```bash
# Search by filename
find . -name "*.md" | grep -i "keyword"

# Search by content
grep -rl "keyword" . --include="*.md"
```

Prefer `rg` when available:

```bash
rg -l "keyword" .
rg --files . | grep "keyword"
```

如果当前环境是 PowerShell，而不是 POSIX shell，可以使用：

```powershell
Get-ChildItem -Recurse -Filter *.md | Select-String -Pattern "keyword" -List | Select-Object -ExpandProperty Path
Get-ChildItem -Recurse -Filter *.md | Where-Object { $_.Name -match "keyword" } | Select-Object -ExpandProperty FullName
```

### 新建笔记

1. 先判断应该放进哪个现有主题目录。
2. 文件名尽量和附近笔记的语言、风格保持一致。
3. 内容尽量写成可复用的知识单元，而不只是临时随手记。
4. 如果相关关系明确，就在底部补上 `[[wikilinks]]`。
5. 如果这篇新笔记形成了一个新的主题簇，就同步更新 `Indexes/` 下的索引笔记。
6. 如果只是名字略有差异，但主题已经有旧笔记，优先补充或合并，不要轻易制造重复笔记。

### 查找关联笔记

要找某篇笔记的反向链接，可以直接搜索 `[[Note Title]]`：

```bash
grep -rl "\\[\\[Note Title\\]\\]" .
```

如果用了带路径的 wikilink，也要顺手搜索完整路径版本：

```bash
grep -rl "\\[\\[AI/Codex/基本操作\\]\\]" .
```

### 查找索引笔记

```bash
find ./Indexes -name "*Index*.md"
```

### 整理笔记

- 优先通过补索引、补链接来改善导航，而不是一上来就大规模移动文件。
- 顶层目录尽量保持整洁，导航类笔记统一放在 `Indexes/`。
- 尊重当前仓库已有的主题目录，而不是强行改造成纯扁平结构。
- 当原始文件名太长或太吵时，优先在 wikilink 里使用别名。
- 如果路径里有空格、中文或 emoji，在 shell 里操作时要特别注意引用。
- 在重命名或移动笔记前，先检查是否已经有其他笔记链接到它；如果有，需要同步更新引用。
- 同一个仓库会在 Windows 和 macOS 上都编辑时，尽量避免只改大小写的重命名，这类改动在不同文件系统上容易出问题。

## 当前仓库的实用规则

- 只要当前工作区打开的是这个仓库，就把当前仓库当作事实上的唯一真源。
- 能用仓库相对路径就不要用机器相关的绝对路径。
- 所有导航型笔记优先放在 `Indexes/`。
- 保留当前仓库中英混合的命名习惯，不要强行全部改成 Title Case。
- 用户要求整理笔记时，优先做最小但有效的调整：先补链接，再补索引，最后才考虑移动文件。
