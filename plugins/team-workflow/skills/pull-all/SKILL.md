---
name: pull-all
description: Update the WorkSpace root repository and all submodules, then summarize each repo state. Use when the user asks for 전체풀, /전체풀, or wants the whole workspace synced to the latest remote commits.
---

# Pull All

1. Run `scripts/pull_all.py`.
2. Show the repo-by-repo summary with branch, short commit, and latest commit message.
3. Surface failures per repository instead of failing silently.

## Script

```bash
python plugins/team-workflow/scripts/pull_all.py
```
