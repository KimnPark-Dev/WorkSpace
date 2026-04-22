# WorkSpace

팀 3명(인송·도현·태호)의 Claude Code 기반 개발 협업 시스템.

프로젝트 관리, 작업 로그, 지식 위키를 하나의 레포에서 운영한다.

## 멤버

| 닉네임 | 이름 | 역할 |
|--------|------|------|
| ssong | 인송 | FE/BE 개발 |
| dohyun | 도현 | 인프라/DevOps |
| taeho | 태호 | 기능 조사/확장 |

## 프로젝트

| 프로젝트 | 상태 | 마감 |
|----------|------|------|
| [AlgoNotion](https://github.com/KimnPark-Dev/AlgoNotion_Extention) | in-progress | 2026-04-30 |
| [TalkTime](https://github.com/KimnPark-Dev/TalkTime) | in-progress | — |
| AI Hack Camp 2026 | in-progress | 2026-04-24 |
| Local Dev Dashboard | todo | 2026-05-11 |

## 디렉토리 구조

```
WorkSpace/
├── members.json          ← 팀 멤버 정의
├── events.jsonl          ← append-only 이벤트 로그
├── projects/             ← 프로젝트별 JSON (태스크 포함)
├── areas/                ← 지속적 책임 영역
├── archive/              ← 완료된 프로젝트
├── logs/                 ← 멤버별 작업 로그 (log-{member}.jsonl)
├── ideas/                ← 아이디어·조사 노트
├── tasks/                ← 오늘 명세서 (로컬 전용, gitignore)
├── analysis/             ← 팀 로그 분석 리포트
├── AlgoNotion_FE/        ← Chrome Extension (서브모듈)
├── AlgoNotion_BE/        ← FastAPI 백엔드 (서브모듈)
├── TalkTime/             ← React + Node.js 모노레포 (서브모듈)
└── LLM_wiki/             ← 개인 지식 위키 (서브모듈)
    ├── wiki/             ← 합성된 지식 페이지
    └── sources/          ← 원본 참고 문서
```

## 시작하기

```bash
# 1. 서브모듈 전체 클론
/전체클론

# 2. 개인 설정 생성
cp config.local.json.example config.local.json
# member 값을 본인 닉네임으로 수정: ssong / dohyun / taeho
```

## 일일 워크플로우

```
/작업시작 {task-id}    ← 오늘 명세서 자동 생성 + 태스크 시작
  ... 작업 ...
/작업완료 {task-id}    ← 로그 기록 + 요약 + git push
```

task-id 없이 `/작업시작`만 실행하면 오늘 할 일 목록만 출력한다.

## 커맨드

| 커맨드 | 설명 |
|--------|------|
| `/전체클론` | 모든 서브모듈 클론 |
| `/작업시작 {id}` | 오늘 명세서 생성 + 태스크 시작 |
| `/작업완료 {id}` | 태스크 완료 + 하루 요약 + git push |
| `/분석` | 팀 로그 패턴 분석 |
| `/스킬생성 {이름}` | 반복 패턴 지식 문서화 |

LLM_wiki 디렉토리에서:

| 커맨드 | 설명 |
|--------|------|
| `/인제스트 {파일/URL}` | 새 문서를 위키에 통합 |
| `/쿼리 {질문}` | 위키에서 지식 검색 |
| `/린트` | 위키 건강 상태 점검 |
