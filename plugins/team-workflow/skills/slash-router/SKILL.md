---
name: slash-router
description: Parse Claude-style slash commands inside this WorkSpace repository. Use when the user literally types /오늘할일, /작업시작 {id}, /작업완료 {id}, /분석, /스킬생성 {이름}, /전체클론, /전체풀, or /정리 {project_id} in chat and wants the Codex workflow to behave like the Claude command system as closely as possible.
---

# Slash Router

1. Accept the user's raw slash-style text exactly as written.
2. Run `scripts/dispatch_command.py --raw "<user text>"`.
3. If the command is `/오늘할일`, show the generated markdown content.
4. If the command mutates files or git state, summarize exactly what changed or what failed.
5. If the command is unsupported, surface the validation error directly.

## Script

```bash
python plugins/team-workflow/scripts/dispatch_command.py --raw "/오늘할일"
```
