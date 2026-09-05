# worldbuilding-innyeok — 캐논 참조형으로 교체된 스킬

이 폴더는 `worldbuilding-innyeok` 스킬의 **정정본**이다.

## 왜 교체했나

기존 스킬은 `references/` 아래에 세계관 설정 사본 586KB를 들고 있었다.
그런데 그 사본은 `Dracloud-sys/innyeok-canon`의 **오래된 버전**이었다
(overview 52KB vs 캐논 75KB, 그리고 law·language·currency·education·economy는 아예 없음).

운영 매뉴얼 0-1 **SSOT 위반**이며, 스킬이 트리거될 때마다 Claude가
캐논이 아닌 낡은 사본을 읽게 된다. 자세한 분석은 `docs/10-innyeok-repo-findings.md`.

## 무엇이 바뀌었나

| | 이전 | 이후 |
|---|---|---|
| 크기 | 740KB | **52KB** |
| 설정 출처 | 스킬 안의 사본 | `innyeok-canon` 저장소 |
| 캐논 조회 | 없음 | 필수 (찾기 → CANON.md → 부분 읽기) |
| 신설정 | 지어낼 수 있음 | "캐논 승격 후보"로 분리 강제 |
| 비공개 캐논 | 언급 없음 | overview 9-7항 · SOUL §6 경고 |
| 구버전 | v2·v3가 같은 폴더에 | 참조 금지 명시 |

`modules/` 5개는 그대로 유지했다. 이게 스킬의 실제 가치(방법)다.
`modules/visualization.md`의 옛 경로 참조 9건은 캐논 경로로 치환했다.

## 적용 방법

스킬 원본은 claude.ai 쪽에서 관리된다(`~/.claude/skills/synced/`는 동기화 사본).
**원본에 아래를 반영해야 영구 적용된다.**

1. `SKILL.md`를 이 폴더의 것으로 교체
2. `references/` 폴더 전체 삭제
3. `modules/` 5개는 이 폴더의 것으로 교체 (경로 치환분 반영)

반영 전까지는 동기화가 일어날 때마다 옛 사본이 되살아난다.
