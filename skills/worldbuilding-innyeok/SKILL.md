---
name: worldbuilding-innyeok
description: 인역(人域) 세계관 — 사이버펑크와 선협(仙俠)이 융합된 복합 세계관의 설계, 생성, 검토를 돕는 모듈형 스킬 세트. 소설·게임·영상 등 창작 작업에서 세계관 요소를 새로 만들거나 기존 설정과의 일관성을 확인하거나, 세력·생태계·수련 체계·시각 메타데이터 등 특정 영역을 구체화할 때 반드시 이 스킬을 사용할 것. "인역", "영기", "영문", "마수", "레벨 시스템", "외부 세계", "수련 체계", "세력 설계", "건축", "영기공학", "전투", "무기", "세력", "축령정", "영원", "생물 분류", "마수 전환", "침식종", "영기 반응성", "준마수", "동식물", "생태계 분류", "영상화", "시각화", "콘티", "시네마틱", "비전 시트", "이미지 시드", "영상 메타데이터", "캐릭터 시각", "장면 설계", "도시 시각화" 등의 키워드가 등장하면 즉시 이 스킬을 참조할 것.
---

# 인역 세계관 빌더 (Worldbuilding: 人域)

이 스킬은 **인역(人域) 세계관** 창작 작업을 지원하는 모듈형 도구 세트다.

**이 스킬은 세계관 설정을 담고 있지 않다.** 설정의 유일한 출처는 캐논 저장소
`Dracloud-sys/innyeok-canon`이다. 이 스킬이 제공하는 것은 *방법*(모듈)과 *조회 규약*뿐이다.

---

## 1. 캐논 조회 (모든 작업의 첫 단계)

### 1-1. 캐논 위치 찾기

아래 순서로 찾고, 처음 성공하는 것을 쓴다.

1. **로컬 클론** — 아래 경로를 순서대로 확인
   ```bash
   for d in ./innyeok-canon ../innyeok-canon ~/innyeok-canon ~/repos/innyeok-canon; do
     [ -f "$d/CANON.md" ] && echo "CANON=$d" && break
   done
   ```
2. **없으면 클론** (공개 저장소, 기본 브랜치는 `master`)
   ```bash
   git clone --depth 1 https://github.com/Dracloud-sys/innyeok-canon
   ```
3. **네트워크·디스크가 막힌 환경이면 raw URL로 직접 읽는다**
   ```
   https://raw.githubusercontent.com/Dracloud-sys/innyeok-canon/master/CANON.md
   ```

> 어떤 경로로도 캐논에 닿지 못하면 **작업을 중단하고 사람에게 알린다.**
> 기억이나 추측으로 설정을 채우지 않는다.

### 1-2. 읽기 규약

캐논 문서는 파일당 20~110KB로 크다. **통독하지 말 것.**

1. **`CANON.md`를 먼저 읽는다.** 어떤 문서가 필요한지 여기서 정한다.
2. 필요한 문서의 **맨 위 `CANON-INDEX` 헤더**(`head -40 <파일>`)를 읽는다.
   요약과 섹션별 행 번호 목차가 있다. (헤더가 없는 문서면 목차 없이 진행)
3. 목차에서 필요한 구간만 `sed -n 'A,Bp' <파일>` 로 읽는다.
4. 문서 전체 읽기는 **마지막 수단**이다.
5. 설정 충돌이 의심되면 `CONTRADICTIONS.md`를 확인한다.

### 1-3. 캐논 규칙 (운영 매뉴얼 v1.0)

| 규칙 | 내용 |
|---|---|
| **SSOT** | 세계관의 진실은 캐논 한 곳에만 있다. 소설·게임·영상은 캐논의 "표현"일 뿐이다. |
| **AI → 캐논 금지** | 캐논 파일을 직접 수정하지 않는다. 변경은 **제안만** 가능하다. |
| **신설정은 확정 금지** | 새 설정이 필요하면 지어내지 말고 **"캐논 승격 후보"로 분리 표기**한다. |
| **구버전 참조 금지** | `world/overview-archive/`(v2·v3)는 캐논이 아니다. 절대 인용하지 않는다. |
| **정본 우선** | 다른 문서와 충돌하면 `world/overview.md`가 이긴다. |

### 1-4. ⚠️ 비공개 캐논 — 프로덕션 서술 금지

- **`world/overview.md` 9-7항 「영원의 실제 구조」** — 캐논에서는 사실로 확정되어
  있으나 인역 사회에 알려져 있지 않다. **인물이 이를 아는 것으로 서술하면 안 된다.**
  인물이 도달 가능한 최대치는 정황 종합에 의한 결론이며 직접 확인은 불가하다.
  학계 통설은 9-6항(영기 맥 집중점)이다.
- **`SOUL.md` §6 (사상적 뿌리)** — 동일하게 비노출 설계다.

산출물이 이 둘을 건드리면 "비공개 캐논 주의" 항목으로 표시하고 사람 확인을 받는다.

---

## 2. 모듈 구성

| 모듈 | 파일 | 역할 |
|---|---|---|
| Foundation | `modules/foundation.md` | 세계 법칙·영기 체계·레벨 시스템 기반 설계 |
| Elements | `modules/elements.md` | 세력·정치·기술·이름·언어 요소 생성 |
| Consistency | `modules/consistency.md` | 일관성 오류 검토 및 피드백 |
| Ecology | `modules/ecology.md` | 생태계·마수·영기 지형·영원 설계 |
| Visualization | `modules/visualization.md` | 영상화 메타데이터 — 영상·이미지·콘티용 시각 슬롯 |

---

## 3. 무엇을 하려는가 → 어떤 캐논 문서를 볼까

경로는 모두 캐논 저장소 기준이다.

| 하려는 일 | 캐논 문서 | 모듈 |
|---|---|---|
| 새 설정 추가 | `world/overview.md` | Elements |
| 세력 구체화 | `world/factions.md` | Elements |
| 도시 구체화 | `world/cities.md` | Elements |
| 마수·생태계·지형 설계 | `world/ecology.md` + `world/overview.md` | Ecology |
| 생물 분류·마수 전환·침식종 | `world/ecology.md` | Ecology |
| 전투·무기·술식 | `world/combat.md` (Lv.4~5는 `world/lv45-tech.md`) | Foundation |
| 건축·인프라·도시 구조 | `world/architecture.md` + `world/cities.md` | Elements |
| 캐릭터 수련·성장 서사 | `world/cultivation.md` | Foundation |
| 캐릭터 설계·직종·소속 | `characters/archetypes.md` + `world/factions.md` | Elements |
| 노동·직종·생활 기술 | `world/labor.md` | Elements |
| 레벨 인증·사회 제도 | `world/level-certification.md` | Foundation |
| 역사·연대 배경 | `world/history.md` | Foundation |
| 소설 플롯·RPG 캠페인 | `world/scenario-narrative.md` | — |
| **사법·형벌** | `world/law.md` | Elements |
| **언어·문자(결자·통어)** | `world/language.md` | Elements |
| **화폐·영전 경제** | `world/currency.md` | Elements |
| **교육(각성당·도제)** | `world/education.md` | Elements |
| **임금·소득** | `world/economy/part1_wages.md` | Elements |
| **경기순환** | `world/economy/part2_cycles.md` | Elements |
| **레벨×계급 전이** | `world/economy/part3_mobility.md` | Elements |
| **물류·축령정 유통** | `world/economy/part4_logistics.md` | Elements |
| **생애 시뮬레이션 예시** | `world/economy/synthesis.md` | — |
| 설정 충돌 검토 | `CONTRADICTIONS.md` | Consistency |
| IP 톤·주제 확인 | `SOUL.md` | — |
| 영상·이미지 메타데이터 | (해당 영역 문서) | Visualization → `imagegen` 스킬 |

---

## 4. 공통 원칙

1. **영기 법칙 우선**: 모든 설정은 영기의 5대 성질(편재성·축적성·의식 연동성·조형성·불완전 자동화 한계)과 충돌해선 안 된다.
2. **레벨 일관성**: 캐릭터·마수·사건의 스케일은 레벨 기준에 부합해야 한다.
3. **두 장르의 융합 논리**: 사이버펑크적 요소(도시·기술·사회 계층)와 선협적 요소(수련·영기·의식 상승)는 영기공학이라는 공통 언어로 연결된다.
4. **인역의 경계**: 인역은 저영기 안정 구역이다. 설정이 이 전제를 흔들 경우 반드시 명시적 근거가 필요하다.

---

## 5. 산출물에 반드시 포함할 것

작업 결과에는 아래 두 항목을 항상 붙인다.

```markdown
## 참조한 캐논
- <파일 경로> §<섹션>  (commit: <해시 또는 "미확인">)

## 캐논 승격 후보
| 설정 | 근거 | 영향받는 캐논 문서 | 기존 설정과의 충돌 |
없으면 "없음"이라고 쓴다. **이것은 제안이며 확정이 아니다.**
```
