---
name: analyze-log
description: Analyze WorkSpace member logs and generate an analysis report. Use when the user asks for 분석, /분석, repeated error patterns, bottlenecks, or skill candidates derived from logs/log-*.jsonl.
---

# Analyze Log

1. Run `scripts/analyze_logs.py`.
2. Show the generated report path and summary.
3. If skill candidates exist, mention `/스킬생성 {이름}`.

## Script

```bash
python plugins/team-workflow/scripts/analyze_logs.py
```
