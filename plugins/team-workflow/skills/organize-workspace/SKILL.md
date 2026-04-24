---
name: organize-workspace
description: Sync completed tasks into project JSON files and update project READMEs. Use when the user asks for 정리, /정리, or wants Claude-style project cleanup applied to one project or all projects in this WorkSpace repo.
---

# Organize Workspace

1. Accept an optional project id.
2. Run `scripts/organize_workspace.py` with or without `--project-id`.
3. Summarize completed task sync results and updated README paths.

## Script

```bash
python plugins/team-workflow/scripts/organize_workspace.py
python plugins/team-workflow/scripts/organize_workspace.py --project-id AlgoNotion
```
