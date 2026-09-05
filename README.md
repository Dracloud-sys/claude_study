# claude_study — AI 모델 · 기법 · 운용 학습 저장소

AI(특히 코딩 에이전트)를 **실제 업무에 도입해서 굴리기 위한** 학습·적용 노트.
"모델을 고르는 법 → 잘 쓰는 법 → 프로젝트에 얹는 법 → 클라우드/로컬 병행 → 무인 예약 운용"
순서로 정리했다.

작성 기준일: **2026-09-05**. 모델 라인업은 분기 단위로 바뀌므로 `docs/01`은 정기 갱신 대상.

## 문서 구성

| 문서 | 내용 |
|---|---|
| [docs/01-models.md](docs/01-models.md) | 최신 모델 지형도(프론티어/오픈웨이트), 선택 기준, 비용 구조 |
| [docs/02-techniques.md](docs/02-techniques.md) | 컨텍스트 엔지니어링, 에이전트 패턴, RAG, 평가(eval) |
| [docs/03-project-management.md](docs/03-project-management.md) | AI를 얹은 프로젝트 관리: 리포지토리 구조, 리뷰 게이트, 산출물 관리 |
| [docs/04-hybrid-cloud-local.md](docs/04-hybrid-cloud-local.md) | 클라우드 ↔ 로컬 병행 운용 4가지 방식 |
| [docs/05-scheduling.md](docs/05-scheduling.md) | 자거나 PC를 꺼도 돌아가는 예약 운용 5가지 방식 |
| [docs/06-tradeoffs.md](docs/06-tradeoffs.md) | 모든 방식의 장단점 종합 비교표 |
| [docs/07-roadmap.md](docs/07-roadmap.md) | 4주 실행 로드맵 + 체크리스트 |
| [docs/08-gpt-claude-handoff.md](docs/08-gpt-claude-handoff.md) | **GPT ↔ Claude 연동 (API 없이 0원)** + 토큰 절감 |
| [templates/](templates/) | 핸드오프 계약 템플릿 · GPT 커스텀 인스트럭션 |

## 30초 요약

1. **모델**: 하나만 쓰지 말고 **3계층**으로 구성 — 프론티어(설계·난이도 높은 코딩) / 중간급(대량 반복) / 로컬 오픈웨이트(민감 데이터·오프라인). 벤치마크 순위보다 *내 작업 5~10개로 만든 자체 평가셋* 결과가 중요하다.
2. **기법**: 프롬프트가 아니라 **컨텍스트 엔지니어링**이 핵심. 도구 표면을 좁히고(MCP 최소 연결), 서브에이전트로 컨텍스트를 분리하고, 반복 작업은 **스킬(SKILL.md)로 자산화**한다.
3. **프로젝트 관리**: `CLAUDE.md`(규칙) + `.claude/skills`(반복 워크플로) + `.claude/agents`(역할) + PR 리뷰 게이트. AI 산출물은 **항상 PR로 받아서 사람이 머지**한다.
4. **클라우드+로컬**: 로컬에서 계획(plan mode) → 클라우드로 실행 위임(`claude --cloud`) → 결과를 로컬로 끌어오기(`claude --teleport`). 이 왕복이 현재 가장 실용적인 하이브리드다.
5. **예약**: PC를 꺼도 돌리려면 **Routines(클라우드)** 또는 **GitHub Actions cron**. PC가 켜져 있어야 하는 Desktop 예약작업 / `/loop`는 로컬 파일 접근이 필요할 때만.

각 방식의 장단점은 [docs/06-tradeoffs.md](docs/06-tradeoffs.md)에 한 표로 모아뒀다.

## GPT와 Claude를 같이 쓴다면

두 AI 연동에 **API는 필요 없다.** 연동의 실체는 대화를 잇는 파이프가 아니라
**둘이 같은 정본(canon)을 보고, 델타만 오가게 하는 포맷 합의**다.
방법과 토큰 비용 진실은 [docs/08-gpt-claude-handoff.md](docs/08-gpt-claude-handoff.md),
바로 쓸 템플릿은 [templates/](templates/)에 있다.
