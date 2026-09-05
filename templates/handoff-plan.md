# 핸드오프 계약: GPT → Claude (기획 전달)

> 이 파일을 복사해 `handoff/inbox/YYYY-MM-DD-<slug>.md`로 저장한다.
> GPT에게는 `templates/gpt-custom-instructions.md`를 지침으로 걸어 이 형식으로 출력하게 한다.

```markdown
---
handoff_id: 2026-09-05-anime-ep03-plot
from: gpt
to: claude
project: innyeok-anime          # innyeok-anime | vcrp | game | 기타
task_type: plan                 # plan | draft | review-request | asset-spec
canon_version: innyeok-v4
touches:                        # ★ Claude가 읽어야 할 정본 파일만 지정 (토큰 절감 핵심)
  - references/factions.md
  - references/cities.md
status: draft                   # draft | ready
---

## 1. 목표
(한 문단. 이 작업이 끝났을 때 "무엇이 존재하는가"로 쓴다.
 "~를 개선한다" ❌ / "ep03 플롯 문서가 확정되어 있다" ⭕)

## 2. 배경
(Claude가 정본만 읽어서는 모르는 맥락만. 정본에 있는 내용은 다시 적지 않는다.)

## 3. 산출물
- [ ] `episodes/ep03/plot.md` — 3막 구성, 씬별 목표, 등장 인물
- [ ] `episodes/ep03/characters-delta.md` — 이번 화에서 새로 정해진 캐릭터 설정

## 4. 제약 / 하지 말 것
- 정본과 충돌 불가: (예) 인역 저영기 전제, Lv.3 이상 술식 등장 금지
- 이번 범위 밖: (예) 작화 스타일, 성우 캐스팅

## 5. 완료 기준 (기계적으로 판정 가능하게)
- [ ] worldbuilding-innyeok의 Consistency 모듈 검사에서 충돌 0건
- [ ] 산출물 파일이 모두 존재
- [ ] 새로 만든 설정은 `canon-delta` 섹션에 별도 기록

## 6. 열린 질문
- [Claude 판단] 도시 이름은 기존 목록에서 골라도 됨
- [사람 확인] 주인공의 레벨을 2로 낮출지 여부 — 시리즈 전체에 영향
```

## 작성 규칙 3가지

1. **`touches`를 반드시 채운다.** 비워두면 Claude가 정본 전체를 뒤지며 토큰을 태운다.
2. **정본에 있는 내용을 다시 쓰지 않는다.** 델타만 적는다.
3. **완료 기준은 검증 가능하게.** "좋은 플롯"이 아니라 "충돌 0건, 파일 3개 생성".
