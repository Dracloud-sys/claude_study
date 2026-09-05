# 10. 인역 저장소 점검 — 발견 2건

GPT 프롬프트를 실제 저장소에 맞추려고 `innyeok-canon` / `innyeok-studio`를
읽다가 나온 것. 둘 다 운영 매뉴얼의 원칙과 직접 충돌한다.

---

## 발견 1 (심각) — 정본이 두 개 존재한다

`worldbuilding-innyeok` 스킬의 `references/`는 `innyeok-canon`의 **오래된 사본**이다.

| 문서 | innyeok-canon | 스킬 references |
|---|---:|---:|
| overview.md ↔ innyeok.md | 74,945 | 52,351 |
| factions.md | 71,290 | 62,336 |
| cities.md | 72,107 | 69,967 |
| architecture.md | 109,681 | 58,906 |
| law.md · language.md · currency.md · education.md | 있음 | **없음** |
| economy/ (part1~4 + synthesis) | 있음 | **없음** |

본문 대조 결과 `overview.md`(46,593자)와 스킬 `innyeok.md`(31,246자)는 **다른 문서**다.

### 왜 문제인가

운영 매뉴얼 0-1 **단일 소스 원칙(SSOT)** 위반이다.
스킬이 트리거되면 Claude는 **캐논이 아니라 낡은 사본을 읽는다.**
법·언어·화폐·교육·경제 5개 영역은 스킬 쪽에 아예 없으므로,
그 영역이 걸린 작업에서는 "설정이 없다"고 판단하고 새로 지어낼 위험이 있다.

### 조치 방향 (매뉴얼 4-3이 이미 정한 방향)

> "각 SKILL.md 상단에 다음 지시문 삽입 권장:
>  *생성 전 반드시 innyeok-canon/CANON.md를 조회하고, 신설정이 필요하면
>  확정하지 말고 캐논 승격 후보로 표시할 것.*"

즉 **스킬은 캐논 사본을 갖지 않아야 한다.**

- `references/` 13개 파일(586KB)을 삭제하고, 캐논 저장소를 가리키게 한다.
- 스킬에는 *방법*만 남긴다 — `modules/` (foundation · elements · consistency ·
  ecology · visualization). 이게 스킬의 실제 가치다.
- 캐논 조회 경로 두 가지:
  - 로컬 클론이 있으면 그 경로
  - 없으면 공개 raw URL
    `https://raw.githubusercontent.com/Dracloud-sys/innyeok-canon/master/CANON.md`

> **이번 세션에서 스킬에 적용한 CANON-INDEX 작업은 이 사본에 한 것이다.**
> 사본을 없애면 그 작업도 함께 사라진다. 스크립트(`scripts/canon_index.py`)는
> 남으므로, 아래 발견 2의 대상인 캐논 저장소에 다시 쓰면 된다.

---

## 발견 2 — 캐논 저장소에도 같은 구조 문제가 있다

`innyeok-canon/world/` 21개 문서 중 **10개에 마크다운 헤딩이 0개**다.
DOCX/PDF 변환본이라 `**굵게**` 유사 제목만 있다. 섹션 점프가 불가능해
에이전트가 통독할 수밖에 없다.

| 상태 | 문서 |
|---|---|
| 헤딩 없음 (통독 강제) | architecture(110KB) · overview(75KB) · cities(72KB) · factions(71KB) · history(68KB) · combat(61KB) · labor(56KB) · level-certification(43KB) · cultivation(37KB) · scenario-narrative(27KB) |
| 헤딩 있음 (정상) | currency · ecology · education · language · law · lv45-tech · economy/part1~4 · synthesis |

헤딩 없는 10개 합계가 **약 620KB**다. 여기가 캐논 조회 비용의 대부분이다.

### 조치 방향

`scripts/canon_index.py`를 그대로 쓸 수 있다. 원문을 바꾸지 않고
맨 위에 요약 + 행번호 목차만 얹는다.

```bash
python3 scripts/canon_index.py <innyeok-canon>/world
```

`scripts/canon-summaries.json`의 키를 캐논 파일명에 맞춰 다시 쓰면 된다.

### 다만 — 사람이 결정할 일이다

운영 매뉴얼 레이어 규칙:

> | AI → 캐논 | **금지** | AI는 캐논 변경 제안만 가능, 직접 수정 불가 |

헤더 주입은 내용 변경이 아니라 형식 추가지만, **캐논 파일을 건드리는 일**이다.
그래서 이 세션에서는 `innyeok-canon`에 아무것도 쓰지 않았다 (읽기만 함).
적용 여부는 사람이 판단한다. 승인하면 `add:` 커밋 한 번으로 끝난다.

---

## 부수 확인

- `innyeok-canon`은 **공개 저장소**다 → GPT가 raw URL로 직접 읽을 수 있다.
  캐논을 GPT Projects에 업로드하고 동기화할 필요가 없다.
  (기본 브랜치는 `master`. `main` 아님.)
- `innyeok-studio`는 비공개 → GPT가 못 읽는다. 스튜디오 상태는 사람이 전달한다.
- 캐논은 이미 `world/overview.md` + `world/overview-archive/`(v2·v3) 구조로
  정본 파일명 고정과 구버전 격리를 마쳤다.
  스킬 쪽에 이번에 한 작업과 같은 결론에 이미 도달해 있었다.
