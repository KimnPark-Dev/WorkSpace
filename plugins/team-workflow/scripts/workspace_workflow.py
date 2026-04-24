from __future__ import annotations

import argparse
import json
import re
import subprocess
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
LOCAL_TZ = datetime.now().astimezone().tzinfo or timezone.utc
SUBMODULE_NAMES = ["LLM_wiki", "AlgoNotion_FE", "AlgoNotion_BE", "TalkTime"]


class WorkflowError(Exception):
    pass


@dataclass
class TaskRecord:
    project: str
    project_title: str
    task: dict[str, Any]
    task_file: Path


def read_json(path: Path) -> Any:
    if not path.exists():
        raise WorkflowError(f"Missing file: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        rows.append(json.loads(line))
    return rows


def write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def load_member() -> str:
    config = read_json(ROOT / "config.local.json")
    member = config.get("member")
    if not member:
        raise WorkflowError("config.local.json must contain a 'member' value.")
    return str(member)


def today_string() -> str:
    return date.today().isoformat()


def now_iso() -> str:
    return datetime.now(LOCAL_TZ).isoformat(timespec="seconds")


def now_hhmm() -> str:
    return datetime.now(LOCAL_TZ).strftime("%H:%M")


def task_markdown_path(member: str) -> Path:
    return ROOT / "tasks" / f"today-{today_string()}-{member}.md"


def append_jsonl(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False) + "\n")


def run_command(args: list[str], cwd: Path | None = None) -> dict[str, Any]:
    try:
        completed = subprocess.run(
            args,
            cwd=str(cwd or ROOT),
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=False,
        )
    except FileNotFoundError as exc:
        return {"ok": False, "code": None, "stdout": "", "stderr": str(exc)}
    return {
        "ok": completed.returncode == 0,
        "code": completed.returncode,
        "stdout": completed.stdout.strip(),
        "stderr": completed.stderr.strip(),
    }


def load_catalog(include_archive: bool = False) -> list[TaskRecord]:
    records: list[TaskRecord] = []
    folders = ["projects", "areas"]
    if include_archive:
        folders.append("archive")
    for folder in folders:
        base = ROOT / folder
        if not base.exists():
            continue
        for path in sorted(base.glob("*.json")):
            doc = read_json(path)
            project_id = str(doc.get("id", path.stem))
            project_title = str(doc.get("title", project_id))
            for task in doc.get("tasks", []):
                task_copy = dict(task)
                task_copy["_container_status"] = doc.get("status")
                records.append(TaskRecord(project=project_id, project_title=project_title, task=task_copy, task_file=path))
    return records


def events_for_today(member: str, event_type: str) -> list[dict[str, Any]]:
    prefix = today_string()
    return [
        row
        for row in read_jsonl(ROOT / "events.jsonl")
        if row.get("member") == member and row.get("type") == event_type and str(row.get("ts", "")).startswith(prefix)
    ]


def completed_task_ids_today(member: str) -> set[str]:
    return {str(row.get("task_id")) for row in events_for_today(member, "task_done") if row.get("task_id")}


def ensure_day_start(member: str) -> None:
    existing = events_for_today(member, "day_start")
    if existing:
        return
    append_jsonl(ROOT / "events.jsonl", {"ts": now_iso(), "type": "day_start", "member": member})


def tasks_for_member(member: str) -> list[TaskRecord]:
    completed_today = completed_task_ids_today(member)
    records = []
    for record in load_catalog():
        status = str(record.task.get("status", "todo"))
        if record.task.get("member") != member:
            continue
        if status in {"done", "archived", "cancelled"}:
            continue
        if str(record.task.get("id")) in completed_today:
            continue
        records.append(record)
    return records


def format_today_tasks(member: str, records: list[TaskRecord]) -> str:
    lines = [f"# 오늘 할 일 — {member} / {today_string()}", "", "## 작업 목록", ""]
    if not records:
        lines.append("할당된 미완료 태스크가 없습니다.")
        lines.append("")
        lines.append("`/작업시작 {순번}` 또는 `/작업시작 {task_id}` 로 시작하세요.")
        return "\n".join(lines) + "\n"

    for idx, record in enumerate(records, start=1):
        task = record.task
        lines.append(f"### {idx}. {task['id']}: {task['title']} [{task.get('priority', 'unknown')}]")
        lines.append(f"- 프로젝트: {record.project}")
        lines.append(f"- 레포: {task.get('path', '.')}")
        if task.get("background"):
            lines.append(f"- 배경: {task['background']}")
        if task.get("skills"):
            skills = ", ".join(str(item) for item in task["skills"])
            lines.append(f"- 관련 스킬: {skills}")
        if task.get("estimate_h") is not None:
            lines.append(f"- 예상 시간: {task['estimate_h']}h")
        lines.append("")

    lines.append("`/작업시작 {순번}` 또는 `/작업시작 {task_id}` 로 시작하세요.")
    return "\n".join(lines) + "\n"


def ensure_today_tasks_file() -> tuple[Path, list[TaskRecord]]:
    member = load_member()
    ensure_day_start(member)
    path = task_markdown_path(member)
    records = tasks_for_member(member)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(format_today_tasks(member, records), encoding="utf-8")
    return path, records


def read_today_tasks_text() -> tuple[Path, str]:
    path, _ = ensure_today_tasks_file()
    return path, path.read_text(encoding="utf-8")


def parse_task_id_from_markdown(path: Path, numeric_id: str) -> str:
    text = path.read_text(encoding="utf-8")
    match = re.search(rf"^### {re.escape(numeric_id)}\. ([^:]+):", text, re.MULTILINE)
    if not match:
        raise WorkflowError(f"번호 {numeric_id}에 해당하는 태스크가 없습니다.")
    return match.group(1).strip()


def resolve_task(task_ref: str) -> tuple[str, str, TaskRecord]:
    member = load_member()
    md_path = task_markdown_path(member)
    if task_ref.isdigit():
        if not md_path.exists():
            raise WorkflowError("오늘 명세서가 없습니다. 먼저 /오늘할일 을 실행해주세요.")
        task_ref = parse_task_id_from_markdown(md_path, task_ref)

    for record in load_catalog():
        if record.task.get("id") == task_ref:
            return member, task_ref, record
    raise WorkflowError(f"task_id '{task_ref}'를 찾을 수 없습니다.")


def session_log_path(task_id: str) -> Path:
    return ROOT / ".workflow-sessions" / f"{task_id}.jsonl"


def start_task(task_ref: str) -> dict[str, Any]:
    member, task_id, record = resolve_task(task_ref)
    append_jsonl(
        ROOT / "events.jsonl",
        {"ts": now_iso(), "type": "task_start", "member": member, "task_id": task_id, "project": record.project},
    )

    session_path = session_log_path(task_id)
    session_path.parent.mkdir(parents=True, exist_ok=True)
    session_payload = {
        "ts": now_hhmm(),
        "type": "session_start",
        "task_id": task_id,
        "member": member,
        "project": record.project,
    }
    session_path.write_text(json.dumps(session_payload, ensure_ascii=False) + "\n", encoding="utf-8")

    return {
        "member": member,
        "task_id": task_id,
        "project": record.project,
        "title": record.task.get("title"),
        "path": str(record.task.get("path", ".")),
        "session_log": str(session_path.relative_to(ROOT)),
    }


def finish_task(task_ref: str) -> dict[str, Any]:
    member, task_id, record = resolve_task(task_ref)
    session_path = session_log_path(task_id)
    if not session_path.exists():
        raise WorkflowError("세션 로그가 없습니다. /작업시작을 먼저 실행했는지 확인해주세요.")

    entries = [json.loads(line) for line in session_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    start_entry = next((entry for entry in entries if entry.get("type") == "session_start"), None)
    if not start_entry:
        raise WorkflowError("세션 로그에 session_start 항목이 없습니다.")

    start_ts = start_entry.get("ts", "00:00")
    try:
        started = datetime.strptime(start_ts, "%H:%M")
    except ValueError as exc:
        raise WorkflowError("session_start ts 형식이 HH:MM이 아닙니다.") from exc
    now_local = datetime.now()
    elapsed = max(
        int(
            (
                now_local
                - started.replace(year=now_local.year, month=now_local.month, day=now_local.day)
            ).total_seconds()
            // 60
        ),
        0,
    )

    errors = [entry.get("message") or entry.get("error") for entry in entries if entry.get("result") == "error"]
    files = sorted(
        {
            str(item)
            for entry in entries
            if isinstance(entry.get("files_touched"), list)
            for item in entry.get("files_touched", [])
        }
    )

    log_payload = {
        "ts": now_iso(),
        "member": member,
        "project": record.project,
        "task_id": task_id,
        "task": record.task.get("title"),
        "type": "feature",
        "tokens": 0,
        "duration_min": elapsed,
        "tags": record.task.get("tags", []),
        "error_count": len([error for error in errors if error]),
        "errors": [error for error in errors if error],
        "files_touched": files,
        "notes": "",
    }
    append_jsonl(ROOT / "logs" / f"log-{member}.jsonl", log_payload)
    append_jsonl(ROOT / "events.jsonl", {"ts": now_iso(), "type": "task_done", "member": member, "task_id": task_id})
    session_path.unlink()

    member_logs = [
        row
        for row in read_jsonl(ROOT / "logs" / f"log-{member}.jsonl")
        if str(row.get("ts", "")).startswith(today_string())
    ]
    summary_tasks = [
        {"task_id": row.get("task_id"), "task": row.get("task"), "duration_min": row.get("duration_min", 0)}
        for row in member_logs
    ]
    today_done = {str(item["task_id"]) for item in summary_tasks if item.get("task_id")}
    carry_over = []
    md_path = task_markdown_path(member)
    if md_path.exists():
        text = md_path.read_text(encoding="utf-8")
        for match in re.finditer(r"^### \d+\. ([^:]+):", text, re.MULTILINE):
            pending_id = match.group(1).strip()
            if pending_id not in today_done and pending_id != task_id:
                carry_over.append(pending_id)
    for pending_id in carry_over:
        append_jsonl(
            ROOT / "events.jsonl",
            {"ts": now_iso(), "type": "task_carry_over", "member": member, "task_id": pending_id},
        )

    return {
        "member": member,
        "task_id": task_id,
        "project": record.project,
        "duration_min": elapsed,
        "error_count": len([error for error in errors if error]),
        "files_touched": files,
        "log_path": f"logs/log-{member}.jsonl",
        "today_summary": {
            "tasks": summary_tasks,
            "total_duration_min": sum(int(row.get("duration_min", 0)) for row in member_logs),
            "total_error_count": sum(int(row.get("error_count", 0)) for row in member_logs),
            "total_files_touched": sum(len(row.get("files_touched", [])) for row in member_logs),
            "carry_over": carry_over,
        },
    }


def analyze_logs() -> dict[str, Any]:
    log_entries = []
    member_counts: Counter[str] = Counter()
    project_durations: defaultdict[str, list[int]] = defaultdict(list)
    task_type_errors: defaultdict[str, list[int]] = defaultdict(list)
    error_messages: defaultdict[str, Counter[str]] = defaultdict(Counter)

    logs_dir = ROOT / "logs"
    for path in sorted(logs_dir.glob("log-*.jsonl")):
        for row in read_jsonl(path):
            log_entries.append(row)
            member = str(row.get("member", "unknown"))
            project = str(row.get("project", "unknown"))
            task_id = str(row.get("task_id", "unknown"))
            member_counts[member] += 1
            project_durations[project].append(int(row.get("duration_min", 0)))
            task_type = task_id.split("-", 1)[0] if "-" in task_id else task_id
            task_type_errors[task_type].append(int(row.get("error_count", 0)))
            for error in row.get("errors", []):
                if error:
                    error_messages[str(error)][member] += 1

    overall_avg = (
        sum(sum(values) for values in project_durations.values()) / max(sum(len(values) for values in project_durations.values()), 1)
    )
    repeated_errors = {msg: counts for msg, counts in error_messages.items() if sum(counts.values()) >= 2}
    bottlenecks = []
    for project, values in sorted(project_durations.items()):
        avg = sum(values) / max(len(values), 1)
        if overall_avg > 0 and avg >= overall_avg * 2:
            bottlenecks.append({"project": project, "avg_duration_min": round(avg, 1), "count": len(values)})

    avg_error_by_type = {
        task_type: (sum(values) / max(len(values), 1))
        for task_type, values in sorted(task_type_errors.items())
    }
    overall_error_avg = sum(sum(values) for values in task_type_errors.values()) / max(
        sum(len(values) for values in task_type_errors.values()),
        1,
    )

    candidates = []
    for error, counts in sorted(repeated_errors.items()):
        total = sum(counts.values())
        if total >= 3:
            priority = "즉시 스킬화 추천"
        else:
            priority = "스킬화 고려"
        candidates.append({"name": slugify_skill_name(error), "reason": error, "count": total, "priority": priority})
    for task_type, avg in avg_error_by_type.items():
        if avg >= overall_error_avg and avg > 0:
            candidates.append(
                {
                    "name": slugify_skill_name(task_type),
                    "reason": f"{task_type} 유형의 평균 에러 수가 높음",
                    "count": round(avg, 2),
                    "priority": "스킬화 검토",
                }
            )

    report_path = ROOT / ".workflow-analysis" / f"{today_string()}-report.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    repeated_section = ["## 반복 패턴", ""]
    if repeated_errors:
        for msg, counts in sorted(repeated_errors.items()):
            repeated_section.append(f"- {msg}: 총 {sum(counts.values())}회 ({dict(counts)})")
    else:
        repeated_section.append("- 반복 에러 패턴 없음")

    bottleneck_section = ["", "## 병목", ""]
    if bottlenecks:
        for item in bottlenecks:
            bottleneck_section.append(
                f"- {item['project']}: 평균 {item['avg_duration_min']}분, {item['count']}건"
            )
    else:
        bottleneck_section.append("- 병목으로 분류된 프로젝트 없음")

    candidate_section = ["", "## 스킬화 후보", ""]
    if candidates:
        for item in candidates:
            candidate_section.append(
                f"- {item['priority']}: {item['name']} ({item['reason']}, {item['count']})"
            )
    else:
        candidate_section.append("- 스킬화 후보 없음")

    stats_section = [
        "",
        "## 원시 통계",
        "",
        f"- 총 기록 건수: {len(log_entries)}",
        f"- 멤버별 작업량: {dict(member_counts)}",
        f"- 프로젝트별 총 시간: { {project: sum(values) for project, values in project_durations.items()} }",
    ]

    content = "\n".join(
        [f"# 분석 리포트 — {today_string()}", ""]
        + repeated_section
        + bottleneck_section
        + candidate_section
        + stats_section
    ) + "\n"
    report_path.write_text(content, encoding="utf-8")

    return {
        "path": str(report_path.relative_to(ROOT)),
        "content": content,
        "candidates": candidates,
    }


def slugify_skill_name(text: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9가-힣]+", "-", text.strip().lower())
    slug = re.sub(r"-{2,}", "-", slug).strip("-")
    return slug or "new-skill"


def latest_analysis_report() -> Path:
    paths = sorted((ROOT / "analysis").glob("*-report.md"))
    paths.extend(sorted((ROOT / "analysis" / "generated").glob("*-report.md")))
    paths.extend(sorted((ROOT / ".workflow-analysis").glob("*-report.md")))
    if not paths:
        raise WorkflowError("analysis/ 디렉토리에 리포트가 없습니다. 먼저 /분석 을 실행해주세요.")
    return paths[-1]


def create_skill(skill_name: str) -> dict[str, Any]:
    if not skill_name.strip():
        raise WorkflowError("스킬 이름을 입력해주세요. 예) /스킬생성 CORS-fix")

    report_path = latest_analysis_report()
    report = report_path.read_text(encoding="utf-8")
    related_lines = [line for line in report.splitlines() if skill_name.lower() in line.lower()]
    related_text = "\n".join(related_lines) if related_lines else "분석 리포트에서 직접 일치하는 패턴을 찾지 못했습니다."
    task_ids = sorted({row.get("task_id") for row in read_jsonl(ROOT / "logs" / f"log-{load_member()}.jsonl") if row.get("task_id")})

    normalized = slugify_skill_name(skill_name)
    skill_dir = ROOT / "plugins" / "team-workflow" / "skills" / normalized
    agents_dir = skill_dir / "agents"
    skill_dir.mkdir(parents=True, exist_ok=True)
    agents_dir.mkdir(parents=True, exist_ok=True)

    skill_md = f"""---
name: {normalized}
description: Generated workspace skill derived from analysis patterns. Use when the user asks for {skill_name}, related repeated errors, or wants a documented fix pattern captured from this WorkSpace repository.
---

# {skill_name}

## 증상
{related_text}

## 원인
분석 리포트와 관련 로그를 바탕으로 근본 원인을 구체화하세요.

## 해결 방법

### 단계별 절차
1. 관련 로그와 재현 조건을 확인한다.
2. 원인과 수정 포인트를 코드 또는 설정 단위로 정리한다.
3. 수정 후 같은 증상이 재발하는지 검증한다.

### 코드 예시
```text
TODO: 여기에 관련 코드 예시를 추가하세요.
```

## 예방법
재발 방지 체크리스트와 사전 검증 항목을 정리하세요.

## 관련 태스크
{", ".join(str(item) for item in task_ids) if task_ids else "관련 태스크 없음"}

## 작성일
{today_string()}
"""
    openai_yaml = (
        f"display_name: {skill_name}\n"
        f"short_description: 분석 리포트를 바탕으로 생성된 {skill_name} 스킬\n"
        f"default_prompt: Use this skill when the user asks for {skill_name} or the related repeated error pattern in this WorkSpace repo.\n"
    )
    (skill_dir / "SKILL.md").write_text(skill_md, encoding="utf-8")
    (agents_dir / "openai.yaml").write_text(openai_yaml, encoding="utf-8")
    return {
        "skill_name": skill_name,
        "normalized": normalized,
        "path": str((skill_dir / "SKILL.md").relative_to(ROOT)),
        "report": str(report_path.relative_to(ROOT)),
    }


def summarize_repo_state(path: Path, label: str) -> dict[str, Any]:
    branch = run_command(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=path)
    commit = run_command(["git", "rev-parse", "--short=7", "HEAD"], cwd=path)
    message = run_command(["git", "log", "-1", "--pretty=%s"], cwd=path)
    status = all(item.get("ok") for item in (branch, commit, message))
    return {
        "name": label,
        "ok": status,
        "branch": branch.get("stdout", ""),
        "commit": commit.get("stdout", ""),
        "message": message.get("stdout", ""),
        "error": branch.get("stderr") or commit.get("stderr") or message.get("stderr"),
    }


def clone_all() -> dict[str, Any]:
    result = run_command(["git", "submodule", "update", "--init", "--recursive"])
    tree_lines = ["WorkSpace/"]
    for name in ["projects", "areas", "archive", "logs", "tasks"] + SUBMODULE_NAMES:
        suffix = "/" if (ROOT / name).is_dir() else ""
        tree_lines.append(f"├── {name}{suffix}")
    missing = [name for name in SUBMODULE_NAMES if not (ROOT / name).exists()]
    return {"command": result, "tree": "\n".join(tree_lines), "missing": missing}


def pull_all() -> dict[str, Any]:
    root_pull = run_command(["git", "pull"])
    submodule_update = run_command(["git", "submodule", "update", "--remote", "--merge"])
    repos = [summarize_repo_state(ROOT, "WorkSpace")]
    repos.extend(summarize_repo_state(ROOT / name, name) for name in SUBMODULE_NAMES if (ROOT / name).exists())
    return {"root_pull": root_pull, "submodule_update": submodule_update, "repos": repos}


def readme_paths_for_project(doc: dict[str, Any]) -> list[Path]:
    paths = []
    for value in dict(doc.get("paths", {})).values():
        base = ROOT / str(value)
        candidate = base / "README.md"
        if candidate not in paths:
            paths.append(candidate)
    return paths or [ROOT / doc.get("id", "project") / "README.md"]


def update_readme_sections(path: Path, project_doc: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    original = path.read_text(encoding="utf-8") if path.exists() else f"# {project_doc.get('title', project_doc.get('id'))}\n"
    members = ", ".join(project_doc.get("members", []))
    tags = ", ".join(project_doc.get("tags", []))
    current_rows = [
        f"| 상태 | {project_doc.get('status', '')} |",
        f"| 마감 | {project_doc.get('due') or '—'} |",
        f"| 담당 | {members} |",
        f"| 태그 | {tags} |",
    ]
    progress = [task for task in project_doc.get("tasks", []) if task.get("status") != "done"]
    done = [task for task in project_doc.get("tasks", []) if task.get("status") == "done"]
    tasks_section = [
        "## 태스크 현황",
        "",
        "### 진행 중",
        "| ID | 제목 | 담당 | 우선순위 | 예상 |",
        "|----|------|------|----------|------|",
    ]
    if progress:
        for task in progress:
            tasks_section.append(
                f"| {task.get('id')} | {task.get('title')} | {task.get('member', '')} | {task.get('priority', '')} | {task.get('estimate_h', '')}h |"
            )
    else:
        tasks_section.append("| — | 진행 중 태스크 없음 | — | — | — |")
    tasks_section.extend(["", "### 완료", "| ID | 제목 | 담당 |", "|----|------|------|"])
    if done:
        for task in done:
            tasks_section.append(f"| {task.get('id')} | {task.get('title')} | {task.get('member', '')} |")
    else:
        tasks_section.append("| — | 완료 태스크 없음 | — |")

    status_section = "\n".join(
        [
            "## 프로젝트 현황",
            "",
            "| 항목 | 내용 |",
            "|------|------|",
            *current_rows,
        ]
    )
    tasks_text = "\n".join(tasks_section)

    def replace_or_append(text: str, heading: str, replacement: str) -> str:
        pattern = re.compile(rf"(?ms)^## {re.escape(heading)}\n.*?(?=^## |\Z)")
        block = replacement.strip() + "\n\n"
        if pattern.search(text):
            return pattern.sub(block, text, count=1)
        text = text.rstrip() + "\n\n"
        return text + block

    updated = replace_or_append(original, "프로젝트 현황", status_section)
    updated = replace_or_append(updated, "태스크 현황", tasks_text)
    path.write_text(updated.rstrip() + "\n", encoding="utf-8")


def organize(project_id: str | None = None) -> dict[str, Any]:
    member = load_member()
    done_ids = {str(row.get("task_id")) for row in read_jsonl(ROOT / "events.jsonl") if row.get("type") == "task_done"}
    targets = []
    for path in sorted((ROOT / "projects").glob("*.json")):
        doc = read_json(path)
        if project_id and doc.get("id") != project_id:
            continue
        changed = []
        for task in doc.get("tasks", []):
            if task.get("id") in done_ids and task.get("status") != "done":
                task["status"] = "done"
                changed.append(task.get("id"))
        write_json(path, doc)
        incomplete = len([task for task in doc.get("tasks", []) if task.get("status") != "done"])
        readmes = []
        for readme_path in readme_paths_for_project(doc):
            update_readme_sections(readme_path, doc)
            readmes.append(str(readme_path.relative_to(ROOT)))
        targets.append(
            {
                "project_id": doc.get("id"),
                "changed": changed,
                "incomplete": incomplete,
                "readmes": readmes,
                "member": member,
            }
        )
    if project_id and not targets:
        raise WorkflowError(f"projects/{project_id}.json 를 찾을 수 없습니다.")
    return {"date": today_string(), "projects": targets}


def main() -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("today")

    start_parser = sub.add_parser("start")
    start_parser.add_argument("--task", required=True)

    finish_parser = sub.add_parser("finish")
    finish_parser.add_argument("--task", required=True)

    sub.add_parser("analyze")

    skill_parser = sub.add_parser("create-skill")
    skill_parser.add_argument("--name", required=True)

    sub.add_parser("clone-all")
    sub.add_parser("pull-all")

    organize_parser = sub.add_parser("organize")
    organize_parser.add_argument("--project-id")

    args = parser.parse_args()
    try:
        if args.command == "today":
            path, records = ensure_today_tasks_file()
            print(json.dumps({"path": str(path.relative_to(ROOT)), "count": len(records)}, ensure_ascii=False))
        elif args.command == "start":
            print(json.dumps(start_task(args.task), ensure_ascii=False))
        elif args.command == "finish":
            print(json.dumps(finish_task(args.task), ensure_ascii=False))
        elif args.command == "analyze":
            print(json.dumps(analyze_logs(), ensure_ascii=False))
        elif args.command == "create-skill":
            print(json.dumps(create_skill(args.name), ensure_ascii=False))
        elif args.command == "clone-all":
            print(json.dumps(clone_all(), ensure_ascii=False))
        elif args.command == "pull-all":
            print(json.dumps(pull_all(), ensure_ascii=False))
        elif args.command == "organize":
            print(json.dumps(organize(args.project_id), ensure_ascii=False))
    except WorkflowError as exc:
        raise SystemExit(str(exc))


if __name__ == "__main__":
    main()
