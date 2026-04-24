from __future__ import annotations

import argparse
import json
import sys

from workspace_workflow import (
    WorkflowError,
    analyze_logs,
    clone_all,
    create_skill,
    finish_task,
    organize,
    pull_all,
    read_today_tasks_text,
    start_task,
)


ALIASES = {
    "/오늘할일": "today",
    "오늘할일": "today",
    "/작업시작": "start",
    "작업시작": "start",
    "/작업완료": "finish",
    "작업완료": "finish",
    "/분석": "analyze",
    "분석": "analyze",
    "/스킬생성": "create-skill",
    "스킬생성": "create-skill",
    "/전체클론": "clone-all",
    "전체클론": "clone-all",
    "/전체풀": "pull-all",
    "전체풀": "pull-all",
    "/정리": "organize",
    "정리": "organize",
}


def dispatch(raw: str) -> dict[str, object]:
    text = raw.strip()
    if not text:
        raise WorkflowError("명령어가 비어 있습니다.")

    parts = text.split(maxsplit=1)
    command = ALIASES.get(parts[0])
    arg = parts[1].strip() if len(parts) > 1 else ""

    if command == "today":
        path, content = read_today_tasks_text()
        return {
            "command": "today",
            "path": str(path),
            "content": content,
        }
    if command == "start":
        if not arg:
            raise WorkflowError("사용법: /작업시작 {번호|task_id}")
        result = start_task(arg)
        return {"command": "start", "result": result}
    if command == "finish":
        if not arg:
            raise WorkflowError("사용법: /작업완료 {task_id}")
        result = finish_task(arg)
        return {"command": "finish", "result": result}
    if command == "analyze":
        return {"command": "analyze", "result": analyze_logs()}
    if command == "create-skill":
        if not arg:
            raise WorkflowError("사용법: /스킬생성 {이름}")
        return {"command": "create-skill", "result": create_skill(arg)}
    if command == "clone-all":
        return {"command": "clone-all", "result": clone_all()}
    if command == "pull-all":
        return {"command": "pull-all", "result": pull_all()}
    if command == "organize":
        return {"command": "organize", "result": organize(arg or None)}

    raise WorkflowError(f"지원하지 않는 명령어입니다: {parts[0]}")


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw", required=True, help="Raw slash-style command text")
    args = parser.parse_args()
    print(json.dumps(dispatch(args.raw), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
