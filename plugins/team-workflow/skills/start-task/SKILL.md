---
name: start-task
description: Start a workspace task using the existing WorkSpace JSON and markdown conventions. Use when the user asks to start a task, record task_start in events.jsonl, initialize a workflow session log, or types 작업시작 or /작업시작 in this Codex workspace.
---

# Start Task

1. Accept a task id like `AlgoNotion-CORS` or a numeric index from today's markdown task file.
2. Run `scripts/start_task.py --task <value>`.
3. If the task resolves successfully, show the task summary and the session log location.
4. If resolution fails, surface the exact validation error.

## Script

```bash
python plugins/team-workflow/scripts/start_task.py --task AlgoNotion-CORS
```
