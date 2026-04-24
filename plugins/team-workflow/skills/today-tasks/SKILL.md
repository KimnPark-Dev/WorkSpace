---
name: today-tasks
description: Read this WorkSpace repository's task sources and generate today's task list for the configured member. Use when the user asks for 오늘할일, /오늘할일, today's tasks, daily task extraction, or wants a fresh tasks/today-YYYY-MM-DD-{member}.md file generated from projects and areas.
---

# Today Tasks

1. Read `config.local.json` from the repo root and extract `member`.
2. Run `scripts/today_tasks.py` from the plugin root.
3. Show the generated markdown path and the numbered task list.
4. If no task file was generated, explain why clearly.

## Output Contract

- Prefer the existing task markdown file when it already matches today's date and member.
- Otherwise regenerate it from `projects/*.json` and `areas/*.json`.
- Use numbered sections in the same markdown shape already used in this repo.

## Script

```bash
python plugins/team-workflow/scripts/today_tasks.py
```
