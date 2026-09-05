# 09. 인역 캐논 토큰 최적화 — 실행 기록

`docs/08` 권장 순서의 **1번(요약+목차 추가 / 구버전 격리)** 을 실제로 적용한 기록.

## 문제

`worldbuilding-innyeok/references/` 는 총 **586KB**(13개 파일)인데:

1. **마크다운 헤딩이 없었다.** DOCX/PDF에서 변환된 파일이라 `**굵게**` 유사 제목과
   `+---+` 표 테두리만 있었다. → 에이전트가 섹션으로 점프할 수 없어 **통독 외에 방법이 없었다.**
2. `SKILL.md`가 *"작업 시작 전 `innyeok-v4.md`를 읽어라"* 라고 지시했다.
   → 매 작업마다 49KB 고정 비용.
3. `innyeok-v2.md`, `v3.md`가 정본과 같은 폴더에 있었다.
   → 에이전트가 구버전을 집으면 **조용히 틀린 설정으로 작업**한다. (일관성 사고 1순위)

## 조치

### ① 각 파일에 `CANON-INDEX` 헤더 주입 (원문 무손상)

파일 맨 위에 HTML 주석 블록만 추가했다. **본문은 한 바이트도 바뀌지 않았다.**

```
<!-- CANON-INDEX v1 -->
<!-- 이 블록만 읽고, 필요한 구간을 `sed -n 'A,Bp'` 로 부분 읽기 할 것. -->
<!-- SUMMARY: ★정본 기준 문서★ 인역의 수용 한계, 6대 법칙(...), 레벨 정의 3축(...) -->
<!-- STATS: 961 lines -->
<!-- TOC
  L78-108   1-1. 인역의 수용 한계
  L109-114  제1법칙 — 영기 순환의 법칙
  ...
-->
<!-- /CANON-INDEX -->
```

행 번호는 **헤더를 포함한 실제 값**이라 `sed -n '109,114p'` 가 바로 맞는다.

### ② `references/INDEX.md` 생성
13개 설정집의 요약과 크기를 담은 4.6KB 파일. **작업 시작 시 이것만 읽는다.**

### ③ 구버전 격리 + 정본 파일명 고정
- `innyeok-v2.md`, `v3.md` → `references/archive/` + 참조 금지 README.
  (사전 확인 결과 두 파일은 SKILL.md·다른 설정집 어디서도 참조되지 않아 안전했다.)
- `innyeok-v4.md` → **`innyeok.md`** 로 개명. 파일명에서 개정 번호를 뺐다.

  개정 번호가 파일명에 있으면 v5가 나올 때마다 SKILL.md와 다른 설정집의
  참조를 전부 고쳐야 하고, 하나라도 놓치면 에이전트가 구버전을 읽는다.
  이제 **파일명은 고정, 개정 번호는 문서 안에만** 있다.

  경로 참조 10곳(SKILL.md 5, ecosystem-classification.md 5, archive/README.md 1)을 갱신했다.
  본문 프로즈의 "세계관 설정집 v4" 표기는 *개정 버전*을 가리키는 것이라 그대로 뒀다.

### ④ SKILL.md 읽기 규약 교체
"시작 전 v4를 읽어라" → **INDEX.md → CANON-INDEX 헤더 → 구간 부분 읽기** 4단계 규약으로.

## 결과

| | 크기 |
|---|---|
| references 전체 | 586 KB |
| `INDEX.md` | 4.6 KB |
| 헤더 13개 전부 합쳐도 | 27.0 KB |
| **탐색 단계 절감** | **94.6%** |

이전에는 "어디를 봐야 하는지" 알아내는 데만 수십 KB를 태웠다.
이제 4.6KB를 읽고 필요한 200줄만 읽는다.

## 검증

- ✅ 헤더 제거 후 백업본과 대조 — **12개 파일 바이트 단위 일치**,
  `ecosystem-classification.md`만 의도한 경로 4칸 변경 (`innyeok-v4.md` → `innyeok.md`)
- ✅ `innyeok.md` 본문은 개명 전 `innyeok-v4.md`와 바이트 단위 일치
- ✅ 잔여 `innyeok-v4.md` 경로 참조 0건 (archive 내 실제 보관본 제외)
- ✅ TOC 행 번호가 실제 섹션과 일치 (`factions.md` "7. 무흔" → L685 확인)
- ✅ 재실행 시 헤더가 쌓이지 않음 (멱등)

## 재적용 방법

스킬 파일은 `~/.claude/skills/synced/` 아래 **동기화된 사본**이다.
원본이 다시 동기화되면 이 헤더는 사라진다. 그때는 원본에 대해 스크립트를 다시 돌린다:

```bash
python3 scripts/canon_index.py <worldbuilding-innyeok>/references
python3 scripts/canon_index.py <...>/references --check   # 갱신 필요 여부만 확인
```

- 요약 문구를 고치려면 `scripts/canon-summaries.json` 만 수정하고 재실행한다.
- 설정집 내용이 바뀌면 행 번호가 어긋나므로 **재실행이 필요하다.**
  → `docs/05-scheduling.md`의 Routine으로 주 1회 자동 재생성 + PR 을 걸어두면 좋다.

## 정본 승격 절차 (v5 이후)

파일명은 언제나 `innyeok.md`다. 개정할 때 참조를 고칠 일이 없다.

```bash
cd <worldbuilding-innyeok>/references
cp innyeok.md archive/innyeok-v4.md    # 현행본을 개정 번호로 보관
#  새 원고를 innyeok.md 로 덮어쓴다 (파일명은 그대로)
python3 scripts/canon_index.py .        # 헤더·INDEX.md 재생성
```

마지막으로 `scripts/canon-summaries.json`의 `innyeok.md` 요약에서
"현재 개정: v4"를 새 번호로 고친다. 같은 안내가 `references/archive/README.md`에도 있다.

## 남은 개선 여지

- **유사 헤딩 → 진짜 마크다운 헤딩 변환**: 본문을 고쳐야 해서 하지 않았다.
  하면 `grep`으로도 섹션을 찾을 수 있어 더 좋아지지만, 원문 변경 리스크가 있다.
- **행 번호 자동 갱신**: 설정집을 고치면 목차 행 번호가 어긋난다.
  주 1회 Routine으로 `canon_index.py` 재실행 + PR 을 걸어두면 해결된다.

---

## 후속: 캐논 저장소에 적용 (2026-09-05)

`docs/10`의 발견 2를 처리했다. 대상은 스킬 사본이 아니라 **진짜 캐논**이다.

- 브랜치: `Dracloud-sys/innyeok-canon` → `claude/canon-index`
- 대상 22개: `world/` 16 · `world/economy/` 5 · `characters/` 1
- `world/overview-archive/`는 캐논이 아니므로 제외
- `CANON.md`에 읽기 규약 4단계 추가

검증: 원문 22/22 바이트 단위 동일, 행 번호 실측 일치(ATX·굵은줄 양쪽), 멱등 22/22.

운영 매뉴얼의 `AI → 캐논 = 금지` 규칙 때문에 **master에 직접 커밋하지 않고
브랜치로만 올렸다.** 머지는 사람이 판단한다.

### 스크립트 변경

문서 모음마다 요약이 다르므로 옵션을 추가했다.

```bash
python3 scripts/canon_index.py <dir> [<dir>...] \
  --summaries scripts/canon-summaries-innyeok-canon.json \
  --no-index          # CANON.md 가 이미 인덱스이므로 INDEX.md 를 만들지 않는다
```

- 디렉터리 여러 개를 한 번에 처리
- `--summaries`: 요약 파일 지정
- `--no-index`: `INDEX.md` 생성 생략
- 제목 정리: DOCX 변환 잔재(`**`, 이스케이프, 중복 공백)를 걷어낸다.
  `****"****출신지역의 레벨 무력화****"****` → `"출신지역의 레벨 무력화"`
