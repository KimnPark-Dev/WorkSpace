---
type: inbox
created: 2026-03-29
project: "[[AlgoNotion]]"
source: ""
---

# AlgoNotion 광고 수익화 — 5초 로딩 광고 모델

문제 풀이 후 Notion 정리 처리 중 발생하는 로딩 시간(약 5초)을 수익화 기회로 활용.
사용자가 이미 기다리는 시간이므로 UX 저항이 낮음.

## 아이디어 상세

- 풀이 제출 → Notion 저장 처리 시작 → **5초 고정 로딩 화면** 노출
- 로딩 화면에 광고(배너 또는 전면) 삽입
- 처리 완료 후 자동으로 Notion 페이지 링크 표시

## 구현 고려 사항

- Chrome 확장 팝업 or content script에서 로딩 UI 구현
- 광고 네트워크: Google AdSense (Chrome 확장 정책 확인 필요), Carbon Ads 등
- **Chrome Web Store 정책 검토 필수** — 확장 내 광고 허용 범위 확인
- 5초 강제 대기 vs 실제 처리 완료 대기 선택 (처리가 5초 미만이면 인위적 딜레이)
- 광고 차단기 대응 방안 검토

## 수익화 단계

1. Chrome Web Store 심사 통과 (현재 진행 중)
2. 광고 정책 리서치 (AdSense for Chrome Extensions 가능 여부)
3. 로딩 UI 컴포넌트 설계
4. A/B 테스트: 광고 있음 vs 없음 (사용자 이탈율 비교)
5. 프리미엄 티어: 광고 제거 구독 모델 병행 검토

## 연결 가능한 노트
- [[1-Projects/AlgoNotion]] — 메인 프로젝트 노트
- (수익화 전략 관련 노트 추가 시 연결)

## 발전 방향
- [ ] Literature 노트로 정리 (Chrome Extension 광고 정책 리서치)
- [ ] Permanent 노트로 승격 (수익화 모델 확정 후)
