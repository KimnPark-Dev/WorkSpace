---
name: create-skill
description: Generate a new Codex skill from the latest WorkSpace analysis report. Use when the user asks for 스킬생성, /스킬생성 {이름}, or wants a repeated pattern documented as a reusable skill.
---

# Create Skill

1. Accept a skill name argument.
2. Run `scripts/create_skill.py --name "<skill-name>"`.
3. Show the generated skill path and report source.
4. If the latest analysis report is missing, ask the user to run `/분석` first.

## Script

```bash
python plugins/team-workflow/scripts/create_skill.py --name "cors-fix"
```
