# WorkSpace

팀 3명(인송·도현·태호)이 공유하는 Claude Code 협업 시스템.

## 멤버별 담당 프로젝트

| 닉네임 | 이름 | 역할 | 담당 프로젝트 |
|--------|------|------|-------------|
| ssong | 인송 | FE/BE 개발 | AlgoNotion(FE+BE), TalkTime(FE+BE), AI-Hack-Camp, Dashboard |
| dohyun | 도현 | 인프라/DevOps | AlgoNotion(인프라), TalkTime(인프라) |
| taeho | 태호 | 기능 조사/확장 | AlgoNotion(Velog·플랫폼 확장) |

## 진행 중인 프로젝트

| 프로젝트 | 상태 | 마감 | 레포 |
|----------|------|------|------|
| AlgoNotion | in-progress | 2026-04-30 | AlgoNotion_FE / AlgoNotion_BE |
| TalkTime | in-progress | — | TalkTime/ |
| AI-Hack-Camp-2026 | **🔴 마감 임박** | 2026-04-24 | 없음 |
| local-dev-dashboard | todo | 2026-05-11 | 없음 |

## 디렉토리 구조

```
WorkSpace/
├── CLAUDE.md               ← 이 파일
├── .claude/commands/       ← 커스텀 슬래시 커맨드
├── members.json            ← 팀 멤버 정의
├── events.jsonl            ← append-only 이벤트 로그
├── config.local.json       ← 개인 설정 (gitignore)
├── projects/               ← 진행 중인 프로젝트 (프로젝트별 JSON)
│   ├── AlgoNotion.json
│   ├── TalkTime.json
│   ├── AI-Hack-Camp-2026.json
│   └── local-dev-dashboard.json
├── areas/                  ← 지속적 책임 영역 (기한 없는 관리 항목)
├── archive/                ← 완료·중단된 프로젝트
├── logs/
│   └── log-{member}.jsonl  ← 멤버별 작업 로그
├── ideas/                  ← 아이디어·Inbox 노트
├── tasks/                  ← 오늘의 명세서 (gitignore)
├── analysis/               ← 분석 리포트
├── AlgoNotion_FE/          ← Chrome Extension (Vanilla JS)
├── AlgoNotion_BE/          ← FastAPI (Python)
├── TalkTime/               ← 모노레포 (React + Node.js)
│   ├── client/
│   └── server/
└── LLM_wiki/               ← Obsidian vault (서브모듈)
```

## 초기 설정 (최초 1회)

```bash
# 1. 서브모듈 전체 클론
/전체클론

# 2. 개인 설정 생성
cp config.local.json.example config.local.json
# member를 본인 닉네임으로 수정: ssong / dohyun / taeho
```

## 일일 워크플로우

```
/작업시작 {id}     ← 명세서 자동생성 + 태스크 시작 (id 없으면 명세서만 출력)
  ... 작업 ...
/작업완료 {id}     ← 로그 기록 + 하루 요약 + git push
```

## 커스텀 커맨드 목록

| 커맨드 | 설명 | 실행 위치 |
|--------|------|----------|
| `/전체클론` | 모든 서브모듈 클론 | WorkSpace 루트 |
| `/작업시작 {id}` | 명세서 자동생성 + 태스크 시작 (id 없으면 명세서만 출력) | 프로젝트 폴더 |
| `/작업완료 {id}` | 태스크 완료 + 하루 요약 + git push | 프로젝트 폴더 |
| `/분석` | 팀 로그 패턴 분석 | WorkSpace 루트 |
| `/스킬생성 {이름}` | 반복 패턴 스킬 문서화 | WorkSpace 루트 |

## 폴더별 역할

### skills/
재사용 가능한 기술 지식 노트. 반복 에러·패턴을 해결한 검증된 방법.
- Chrome Extension 개발 원칙
- API 연동 체크리스트
- DOM/JS 패턴 등

### ideas/
아이디어 메모, 조사 노트. 아직 구체화되지 않은 것들.
- 수익화 아이디어
- 신규 프로젝트 아이디어
- 기술 조사 노트

### resources/
외부 참고 자료.
- `해커톤/` — 대회 공고 및 정보
- `데이터베이스/` — 외부 데이터 소스 정보

## 폴더별 역할

### projects/
진행 중인 프로젝트. 프로젝트별 JSON 파일로 분리 — 서로 다른 파일이므로 충돌 없음.
- 프로젝트 메타정보 + tasks 배열 포함
- 완료된 프로젝트는 `archive/`로 이동

### areas/
기한 없는 지속적 책임 영역. (예: 팀 인프라 관리, 코드 리뷰 기준 등)

### archive/
완료·중단된 프로젝트. 프로젝트 JSON을 그대로 이동, status를 "done"/"archived"로 변경.

### LLM_wiki/
개인 지식 위키 (Karpathy 스타일). 기술 원칙·디버그 패턴·참고 자료 보관.
- `wiki/` — 합성된 지식 페이지 (구 skills/)
- `sources/` — 원본 참고 문서 (구 resources/)
- `/인제스트`, `/쿼리`, `/린트` 커맨드로 운영

## 충돌 방지 규칙

| 파일 | 전략 |
|------|------|
| `projects/*.json` | 프로젝트별 파일 분리 → 충돌 없음 |
| `logs/log-{member}.jsonl` | 멤버별 파일 분리 → 충돌 없음 |
| `events.jsonl` | append-only → 충돌 없음 |
| `skills/*.md` | 브랜치 → PR → 머지 |
| `tasks/today-*.md` | .gitignore → 로컬 전용 |
| `config.local.json` | .gitignore → 로컬 전용 |
