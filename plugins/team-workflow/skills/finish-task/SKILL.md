---
name: finish-task
description: Finish a workspace task using the existing WorkSpace logging conventions. Use when the user asks to complete a task, summarize the current workflow session log, append a member log entry, or types 작업완료 or /작업완료 in this Codex workspace.
---

# Finish Task

1. Accept a task id like `AlgoNotion-CORS`.
2. Run `scripts/finish_task.py --task <value>`.
3. Summarize duration, error count, files touched, and the log file that was updated.
4. If the workflow session log is missing, explain that task start must run first.

## Script

```bash
python plugins/team-workflow/scripts/finish_task.py --task AlgoNotion-CORS
```
